// Copyright (c) Sleipnir contributors

#include "sleipnir/util/pool.hpp"

namespace sleipnir {

PoolResource& global_pool_resource() {
  thread_local PoolResource pool{16384};
  return pool;
}

}  // namespace sleipnir
