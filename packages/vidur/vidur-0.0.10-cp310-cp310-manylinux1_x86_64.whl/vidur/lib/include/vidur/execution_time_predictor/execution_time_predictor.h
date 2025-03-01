#pragma once
#include <memory>
#include <numeric>
#include <unordered_map>
#include <utility>

#include "vidur/config/config.h"
#include "vidur/entities/batch.h"
#include "vidur/entities/execution_time.h"
#include "vidur/entities/kv_parallel_batch.h"
#include "vidur/execution_time_predictor/prediction_keys.h"

namespace vidur
{
namespace execution_time_predictor
{

class ExecutionTimePredictor
{
public:
  struct PairHash
  {
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2>& pair) const
    {
      auto h1 = std::hash<T1>{}(pair.first);
      auto h2 = std::hash<T2>{}(pair.second);
      return h1 ^ (h2 << 1);
    }
  };

  using PredictionKey = std::pair<int, int>;
  using PredictionMap = std::unordered_map<
      std::string,
      std::unordered_map<PredictionKey, double, PairHash>>;

  static inline PredictionKey GetPredictionKey(int x)
  {
    return std::make_pair(x, -1);
  }
  static inline PredictionKey GetPredictionKey(int x, int y)
  {
    return std::make_pair(x, y);
  }

  ExecutionTimePredictor(
      config::ExecutionTimePredictorConfig config,
      config::ReplicaConfig replica_config,
      config::ModelConfig model_config,
      std::vector<std::string>& prediction_ops,
      std::vector<std::vector<PredictionKey>>& prediction_keys,
      std::vector<std::vector<double>>& prediction_values);

  // Main prediction method
  entities::ExecutionTime GetExecutionTimeBatch(
      const entities::Batch& batch,
      std::size_t pipeline_stage);
  entities::ExecutionTime GetExecutionTimeKVParallelBatch(
      const entities::KVParallelBatch& kvp_batch,
      std::size_t pipeline_stage);

private:
  // Helper methods for timing predictions
  double GetAttentionLayerPreProjExecutionTime(const entities::Batch& batch);
  double GetAttentionLayerPostProjExecutionTime(const entities::Batch& batch);
  double GetAttentionRopeExecutionTime(const entities::Batch& batch);
  double GetAttentionKvCacheSaveExecutionTime(const entities::Batch& batch);
  double GetAttentionDecodeExecutionTime(const entities::Batch& batch);
  double GetAttentionPrefillExecutionTime(const entities::Batch& batch);
  double GetMlpLayerUpProjExecutionTime(const entities::Batch& batch);
  double GetMlpLayerDownProjExecutionTime(const entities::Batch& batch);
  double GetMlpLayerActExecutionTime(const entities::Batch& batch);
  double GetTensorParallelCommunicationTime(const entities::Batch& batch);
  double GetPipelineParallelCommunicationTime(const entities::Batch& batch);
  double GetMlpNormLayerActExecutionTime(const entities::Batch& batch);
  double GetAttnNormLayerActExecutionTime(const entities::Batch& batch);
  double GetAddLayerActExecutionTime(const entities::Batch& batch);
  double GetKvParallelCommunicationTime(const entities::Batch& batch);
  PredictionKey GetBatchDecodeAttentionParams(const entities::Batch& batch);
  std::vector<PredictionKey>
  GetBatchPrefillAttentionParams(const entities::Batch& batch);

  config::ExecutionTimePredictorConfig config_;
  config::ReplicaConfig replica_config_;
  config::ModelConfig model_config_;
  PredictionMap predictions_;
  std::size_t num_layers_per_pipeline_stage_;
};

} // namespace execution_time_predictor
} // namespace vidur
