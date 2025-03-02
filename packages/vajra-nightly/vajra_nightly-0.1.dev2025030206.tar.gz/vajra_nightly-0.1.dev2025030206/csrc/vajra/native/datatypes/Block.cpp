#include "vajra/native/datatypes/Block.h"

using namespace vajra;

void LogicalTokenBlock::AppendTokens(const std::vector<std::size_t>& token_ids)
{
  ASSERT_VALID_RUNTIME(
      token_ids.size() <= NumEmptySlots(),
      "Not enough empty slots");
  std::size_t curr_idx = num_tokens_;
  std::copy(
      token_ids.begin(),
      token_ids.end(),
      this->token_ids_.begin() + curr_idx);
  num_tokens_ += token_ids.size();
}
