#include "vidur/execution_time_predictor/execution_time_predictor_pybind.h"

#include <pybind11/stl.h>

#include "vidur/execution_time_predictor/execution_time_predictor.h"

namespace vidur
{
namespace execution_time_predictor
{
namespace py = pybind11;

void InitExecutionTimePredictor(pybind11::module_& m)
{
  py::class_<ExecutionTimePredictor>(m, "ExecutionTimePredictor")
      .def(
          py::init<
              config::ExecutionTimePredictorConfig,
              config::ReplicaConfig,
              config::ModelConfig,
              std::vector<std::string>&,
              std::vector<std::vector<std::pair<int, int>>>&,
              std::vector<std::vector<double>>&>(),
          py::arg("config"),
          py::arg("replica_config"),
          py::arg("model_config"),
          py::arg("prediction_ops"),
          py::arg("prediction_keys"),
          py::arg("prediction_values"))
      .def(
          "get_execution_time_batch",
          &ExecutionTimePredictor::GetExecutionTimeBatch,
          py::arg("batch"),
          py::arg("pipeline_stage"))
      .def(
          "get_execution_time_kv_parallel_batch",
          &ExecutionTimePredictor::GetExecutionTimeKVParallelBatch,
          py::arg("kvp_batch"),
          py::arg("pipeline_stage"));
}

} // namespace execution_time_predictor
} // namespace vidur
