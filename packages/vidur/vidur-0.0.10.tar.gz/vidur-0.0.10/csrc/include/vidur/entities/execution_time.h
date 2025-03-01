#pragma once
#include <cstddef>
#include <string>

namespace vidur
{
namespace entities
{

struct ExecutionTime
{
  ExecutionTime(
      std::size_t num_layers_per_pipeline_stage,
      double attention_rope_execution_time,
      double attention_kv_cache_save_execution_time,
      double attention_decode_execution_time,
      double attention_prefill_execution_time,
      double attention_layer_pre_proj_execution_time,
      double attention_layer_post_proj_execution_time,
      double mlp_layer_up_proj_execution_time,
      double mlp_layer_down_proj_execution_time,
      double mlp_layer_act_execution_time,
      double attn_norm_time,
      double mlp_norm_time,
      double add_time,
      double tensor_parallel_communication_time,
      double pipeline_parallel_communication_time);

  // Utility methods
  double GetMlpLayerExecutionTime() const;
  double GetAttentionLayerExecutionTime() const;
  double GetBlockExecutionTime() const;
  double GetModelTime() const;
  double GetModelTimeMs() const;
  double GetTotalTime() const;

  std::string ToString() const;

  // Members
  const std::size_t num_layers;
  const double attention_rope_execution_time;
  const double attention_kv_cache_save_execution_time;
  const double attention_decode_execution_time;
  const double attention_prefill_execution_time;
  const double attention_layer_pre_proj_execution_time;
  const double attention_layer_post_proj_execution_time;
  const double mlp_layer_up_proj_execution_time;
  const double mlp_layer_down_proj_execution_time;
  const double mlp_layer_act_execution_time;
  const double attn_norm_time;
  const double mlp_norm_time;
  const double add_time;
  const double tensor_parallel_communication_time;
  const double pipeline_parallel_communication_time;
  const double kvp_group_communication_time;
};

} // namespace entities
} // namespace vidur