#pragma once

#include "vajra/commons/Logging.h"
#include "vajra/commons/StdCommon.h"

namespace vajra
{
class SamplerOutput
{
public:
  SamplerOutput(
      std::size_t schedule_id,
      std::string& seq_id,
      std::vector<std::size_t>& output_tokens)
      : schedule_id_(schedule_id),
        seq_id_(seq_id),
        output_tokens_(output_tokens)
  {
  }

  SamplerOutput(
      std::size_t schedule_id,
      std::string seq_id,
      std::vector<std::size_t> output_tokens)
      : schedule_id_(schedule_id),
        seq_id_(seq_id),
        output_tokens_(output_tokens)
  {
  }

  inline std::size_t GetScheduleId() const { return schedule_id_; }
  inline const std::string& GetSeqId() const { return seq_id_; }
  inline const std::string GetSeqIdCopy() const { return seq_id_; }
  inline const std::vector<std::size_t>& GetOutputTokens() const
  {
    return output_tokens_;
  }
  inline const std::vector<std::size_t> GetOutputTokensCopy() const
  {
    return output_tokens_;
  }

  std::string ToString() const
  {
    return fmt::format(
        "SamplerOutput("
        "ScheduleId: {},"
        "SeqId: {},"
        "OutputTokens: {})",
        schedule_id_,
        seq_id_,
        fmt::join(output_tokens_, ", "));
  }

private:
  std::size_t schedule_id_;
  std::string seq_id_;
  std::vector<std::size_t> output_tokens_;
};

using SamplerOutputs = std::vector<std::optional<SamplerOutput>>;
} // namespace vajra
