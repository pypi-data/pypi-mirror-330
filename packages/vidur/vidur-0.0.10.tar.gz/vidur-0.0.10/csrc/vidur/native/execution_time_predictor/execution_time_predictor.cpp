#include "vidur/execution_time_predictor/execution_time_predictor.h"

#include <algorithm>
#include <cassert>
#include <cmath>

namespace vidur
{
namespace execution_time_predictor
{

ExecutionTimePredictor::ExecutionTimePredictor(
    config::ExecutionTimePredictorConfig config,
    config::ReplicaConfig replica_config,
    config::ModelConfig model_config,
    std::vector<std::string>& prediction_ops,
    std::vector<std::vector<PredictionKey>>& prediction_keys,
    std::vector<std::vector<double>>& prediction_values)
    : config_(config),
      replica_config_(replica_config),
      model_config_(model_config)
{
  assert(prediction_ops.size() == prediction_keys.size());
  assert(prediction_ops.size() == prediction_values.size());

  predictions_.reserve(prediction_ops.size());
  for (std::size_t i = 0; i < prediction_ops.size(); i++)
  {
    assert(prediction_keys[i].size() == prediction_values[i].size());

    predictions_[prediction_ops[i]] =
        std::unordered_map<PredictionKey, double, PairHash>();
    predictions_[prediction_ops[i]].reserve(prediction_keys[i].size());
    for (std::size_t j = 0; j < prediction_keys[i].size(); j++)
    {
      predictions_[prediction_ops[i]][prediction_keys[i][j]] =
          prediction_values[i][j];
    }
  }

  num_layers_per_pipeline_stage_ =
      model_config.num_layers / replica_config.num_pipeline_stages;
}

entities::ExecutionTime ExecutionTimePredictor::GetExecutionTimeBatch(
    const entities::Batch& batch,
    std::size_t pipeline_stage)
{
  double pipeline_parallel_communication_time = 0.0;
  if (pipeline_stage != replica_config_.num_pipeline_stages - 1)
  {
    pipeline_parallel_communication_time =
        GetPipelineParallelCommunicationTime(batch);
  }

  double tensor_parallel_communication_time = 0.0;
  if (replica_config_.tensor_parallel_size == 1)
  {
    tensor_parallel_communication_time = 0.0;
  }
  else
  {
    tensor_parallel_communication_time =
        GetTensorParallelCommunicationTime(batch);
  }

  // TODO: Add kv_parallel communication time

  return entities::ExecutionTime(
      num_layers_per_pipeline_stage_,
      GetAttentionRopeExecutionTime(batch),
      GetAttentionKvCacheSaveExecutionTime(batch),
      GetAttentionDecodeExecutionTime(batch),
      GetAttentionPrefillExecutionTime(batch),
      GetAttentionLayerPreProjExecutionTime(batch),
      GetAttentionLayerPostProjExecutionTime(batch),
      GetMlpLayerUpProjExecutionTime(batch),
      GetMlpLayerDownProjExecutionTime(batch),
      GetMlpLayerActExecutionTime(batch),
      GetAttnNormLayerActExecutionTime(batch),
      GetMlpNormLayerActExecutionTime(batch),
      GetAddLayerActExecutionTime(batch),
      tensor_parallel_communication_time,
      pipeline_parallel_communication_time);
}

entities::ExecutionTime ExecutionTimePredictor::GetExecutionTimeKVParallelBatch(
    const entities::KVParallelBatch& kvp_batch,
    std::size_t pipeline_stage)
{
  auto it = std::max_element(
      kvp_batch.batch_mapping.begin(),
      kvp_batch.batch_mapping.end(),
      [&](const auto& a, const auto& b)
      {
        return GetExecutionTimeBatch(*(a.second), pipeline_stage)
                   .GetTotalTime() <
               GetExecutionTimeBatch(*(b.second), pipeline_stage)
                   .GetTotalTime();
      });

  return GetExecutionTimeBatch(*(it->second), pipeline_stage);
}

double ExecutionTimePredictor::GetAttentionLayerPreProjExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::ATTN_PRE_PROJ]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAttentionLayerPostProjExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::ATTN_POST_PROJ]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAttentionRopeExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::ATTN_ROPE]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAttentionKvCacheSaveExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::ATTN_KV_CACHE_SAVE]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAttentionDecodeExecutionTime(
    const entities::Batch& batch)
{
  auto [decode_batch_size, decode_avg_kv_cache_size] =
      GetBatchDecodeAttentionParams(batch);

  if (decode_batch_size == 0)
  {
    return 0.0;
  }

  return predictions_[PredictionOps::ATTN_DECODE][GetPredictionKey(
             decode_batch_size,
             decode_avg_kv_cache_size)] *
         (1 + config_.attention_decode_batching_overhead_fraction *
                  (decode_batch_size > 1 ? 1 : 0));
}

double ExecutionTimePredictor::GetAttentionPrefillExecutionTime(
    const entities::Batch& batch)
{
  std::vector<std::pair<int, int>> prefill_params =
      GetBatchPrefillAttentionParams(batch);

  if (prefill_params.empty())
  {
    return 0.0;
  }

  double total_time = 0.0;
  for (const auto& [kv_cache_size, prefill_chunk_size] : prefill_params)
  {
    std::size_t prefill_chunk_size_rounded =
        ((prefill_chunk_size + 31) / 32) * 32;
    total_time += predictions_[PredictionOps::ATTN_PREFILL][GetPredictionKey(
        kv_cache_size,
        prefill_chunk_size_rounded)];
  }

  return total_time;
}

double ExecutionTimePredictor::GetMlpLayerUpProjExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::MLP_UP_PROJ]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetMlpLayerDownProjExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::MLP_DOWN_PROJ]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetMlpLayerActExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::MLP_ACT]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetTensorParallelCommunicationTime(
    const entities::Batch& batch)
{
  return (
      predictions_[PredictionOps::ALL_REDUCE]
                  [GetPredictionKey(batch.total_num_q_tokens_rounded)] +
      config_.nccl_cpu_launch_overhead_ms +
      config_.nccl_cpu_skew_overhead_per_device_ms *
          pow(replica_config_.tensor_parallel_size, 1.25));
}

double ExecutionTimePredictor::GetPipelineParallelCommunicationTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::SEND_RECV]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetMlpNormLayerActExecutionTime(
    const entities::Batch& batch)
{
  if (!model_config_.post_attn_norm)
  {
    return 0.0;
  }

  return predictions_[PredictionOps::POST_ATTENTION_LAYERNORM]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAttnNormLayerActExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::INPUT_LAYERNORM]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetAddLayerActExecutionTime(
    const entities::Batch& batch)
{
  return predictions_[PredictionOps::ADD]
                     [GetPredictionKey(batch.total_num_q_tokens_rounded)];
}

double ExecutionTimePredictor::GetKvParallelCommunicationTime(
    const entities::Batch& batch)
{
  if (!config_.disable_kvp_communication)
  {
    return 0.0;
  }

  double total_comm_time = 0.0;

  for (std::size_t i = 0; i < batch.num_requests; i++)
  {
    std::size_t num_q_tokens = batch.num_q_tokens[i];
    std::size_t num_groups = batch.num_active_kvp_groups[i];

    if (num_q_tokens == 0)
    {
      continue;
    }

    // round up to the nearest multiple of 8
    num_q_tokens = ((num_q_tokens + 7) / 8) * 8;

    total_comm_time +=
        (predictions_[PredictionOps::ALL_REDUCE_KVP]
                     [GetPredictionKey(num_q_tokens, num_groups)] +
         config_.nccl_cpu_launch_overhead_ms +
         config_.nccl_cpu_skew_overhead_per_device_ms * pow(num_groups, 1.25));
  }

  return total_comm_time;
}

ExecutionTimePredictor::PredictionKey
ExecutionTimePredictor::GetBatchDecodeAttentionParams(
    const entities::Batch& batch)
{
  std::vector<std::size_t> decode_kv_cache_sizes;

  for (std::size_t i = 0; i < batch.num_requests; i++)
  {
    std::size_t num_q_tokens = batch.num_q_tokens[i];
    std::size_t num_kv_tokens = batch.num_kv_tokens[i];

    if (num_q_tokens != 1)
    {
      continue;
    }

    decode_kv_cache_sizes.push_back(num_kv_tokens);
  }

  if (decode_kv_cache_sizes.size() == 0)
  {
    return GetPredictionKey(0, 0);
  }

  std::size_t decode_batch_size = decode_kv_cache_sizes.size();
  std::size_t decode_avg_kv_cache_size = std::accumulate(
                                             decode_kv_cache_sizes.begin(),
                                             decode_kv_cache_sizes.end(),
                                             0) /
                                         decode_batch_size;

  decode_avg_kv_cache_size = ((decode_avg_kv_cache_size +
                               config_.kv_cache_prediction_granularity - 1) /
                              config_.kv_cache_prediction_granularity) *
                             config_.kv_cache_prediction_granularity;

  return GetPredictionKey(decode_batch_size, decode_avg_kv_cache_size);
}

std::vector<ExecutionTimePredictor::PredictionKey>
ExecutionTimePredictor::GetBatchPrefillAttentionParams(
    const entities::Batch& batch)
{
  std::vector<ExecutionTimePredictor::PredictionKey> prefill_params;

  for (std::size_t i = 0; i < batch.num_requests; i++)
  {
    std::size_t num_q_tokens = batch.num_q_tokens[i];
    std::size_t num_kv_tokens = batch.num_kv_tokens[i];

    if (num_q_tokens == 1)
    {
      continue;
    }

    num_kv_tokens =
        ((num_kv_tokens + config_.kv_cache_prediction_granularity - 1) /
         config_.kv_cache_prediction_granularity) *
        config_.kv_cache_prediction_granularity;

    prefill_params.push_back(GetPredictionKey(num_kv_tokens, num_q_tokens));
  }

  return prefill_params;
}

} // namespace execution_time_predictor
} // namespace vidur