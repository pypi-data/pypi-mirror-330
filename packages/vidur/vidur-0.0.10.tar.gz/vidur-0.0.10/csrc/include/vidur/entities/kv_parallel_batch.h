#pragma once
#include <memory>
#include <unordered_map>

#include "vidur/entities/batch.h"

namespace vidur
{
namespace entities
{

struct KVParallelBatch
{
  using BatchPtr = std::shared_ptr<Batch>;
  using BatchMap = std::unordered_map<std::size_t, BatchPtr>;

  KVParallelBatch(
      std::size_t replica_id,
      const std::vector<std::size_t>& kvp_group_ids,
      const std::vector<BatchPtr>& batches);

  std::string ToString() const;

  // Members
  const std::size_t replica_id;
  BatchMap batch_mapping;
};

} // namespace entities
} // namespace vidur
