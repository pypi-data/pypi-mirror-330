#include "vajra/native/datatypes/SamplingParams.h"

using namespace vajra;

void SamplingParams::VerifyArgs() const
{
  ASSERT_VALID_ARGUMENTS(
      temperature >= 0.0,
      fmt::format("temperature must be non-negative, got {}.", temperature));
  ASSERT_VALID_ARGUMENTS(
      top_p > 0.0 && top_p <= 1.0,
      fmt::format("top_p must be in (0, 1], got {} {}.", top_p, temperature));
  ASSERT_VALID_ARGUMENTS(
      !(top_k < -1 || top_k == 0),
      fmt::format("top_k must be -1 (disable) or at least 1, got {}.", top_k));
  ASSERT_VALID_ARGUMENTS(
      max_tokens >= 1,
      fmt::format("max_tokens must be at least 1, got {}.", max_tokens));
}

void SamplingParams::VerifyGreedySampling() const
{
  ASSERT_VALID_ARGUMENTS(
      !(top_p < 1.0 - SAMPLING_EPS),
      "top_p must be 1 when using greedy sampling.");
  ASSERT_VALID_ARGUMENTS(
      top_k == -1,
      "top_k must be -1 when using greedy sampling.");
}
