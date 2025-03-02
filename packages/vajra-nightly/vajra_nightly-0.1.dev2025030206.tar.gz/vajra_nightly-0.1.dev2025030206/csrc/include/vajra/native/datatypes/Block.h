#pragma once

#include "vajra/commons/Logging.h"
#include "vajra/commons/StdCommon.h"

namespace vajra
{
constexpr int BLANK_TOKEN_ID = -1;

struct LogicalTokenBlock
{
  LogicalTokenBlock(
      std::size_t block_number,
      std::size_t block_size,
      std::vector<std::size_t> token_ids = std::vector<std::size_t>(),
      std::size_t num_tokens = 0)
      : block_number(block_number),
        block_size(block_size),
        token_ids_(token_ids),
        num_tokens_(num_tokens)
  {
    token_ids_.resize(block_size, BLANK_TOKEN_ID);
  }

  inline bool IsEmpty() const { return num_tokens_ == 0; }

  inline std::size_t NumEmptySlots() const { return block_size - num_tokens_; }

  inline bool IsFull() const { return num_tokens_ == block_size; }

  void AppendTokens(const std::vector<std::size_t>& token_ids);

  inline std::size_t GetLastTokenId()
  {
    ASSERT(num_tokens_ > 0);
    return token_ids_[num_tokens_ - 1];
  }

  inline const std::vector<std::size_t>& GetTokenIds() const
  {
    return token_ids_;
  }

  inline const std::vector<std::size_t> GetTokenIdsCopy() const
  {
    return token_ids_;
  }

  inline size_t GetNumTokens() const { return num_tokens_; }

  const std::size_t block_number;
  const std::size_t block_size;

private:
  std::vector<std::size_t> token_ids_;
  std::size_t num_tokens_;
};
} // namespace vajra
