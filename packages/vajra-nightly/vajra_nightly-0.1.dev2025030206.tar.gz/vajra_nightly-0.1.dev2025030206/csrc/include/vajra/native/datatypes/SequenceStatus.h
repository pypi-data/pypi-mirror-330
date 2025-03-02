#pragma once

#include <optional>
#include <string>

namespace vajra
{

enum class SequenceStatus
{
  Waiting,
  WaitingPreempted,
  Running,
  Paused,
  FinishedStopped,
  FinishedLengthCapped,
  FinishedIgnored
};

namespace sequence_status
{

inline bool IsFinished(SequenceStatus status)
{
  return status == SequenceStatus::FinishedStopped ||
         status == SequenceStatus::FinishedLengthCapped ||
         status == SequenceStatus::FinishedIgnored;
}

inline bool IsExecuting(SequenceStatus status)
{
  return status == SequenceStatus::Running || status == SequenceStatus::Paused;
}

inline bool IsWaiting(SequenceStatus status)
{
  return status == SequenceStatus::Waiting;
}

inline bool IsWaitingPreempted(SequenceStatus status)
{
  return status == SequenceStatus::WaitingPreempted;
}

inline bool IsPaused(SequenceStatus status)
{
  return status == SequenceStatus::Paused;
}

inline bool IsRunning(SequenceStatus status)
{
  return status == SequenceStatus::Running;
}

inline std::optional<std::string> GetFinishedReason(SequenceStatus status)
{
  switch (status)
  {
  case SequenceStatus::FinishedStopped:
    return "stop";
  case SequenceStatus::FinishedLengthCapped:
  case SequenceStatus::FinishedIgnored:
    return "length";
  default:
    return std::nullopt;
  }
}
} // namespace sequence_status
} // namespace vajra
