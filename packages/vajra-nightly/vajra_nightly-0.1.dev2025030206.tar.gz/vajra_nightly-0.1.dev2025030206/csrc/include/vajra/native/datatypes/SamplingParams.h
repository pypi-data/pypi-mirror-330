#pragma once

#include "vajra/commons/Logging.h"
#include "vajra/commons/StdCommon.h"

namespace vajra
{
constexpr double SAMPLING_EPS = 1e-5;

enum class SamplingType
{
  Greedy,
  Random
};

class SamplingParams
{
public:
  SamplingParams(
      double temperature = 1.0,
      double top_p = 1.0,
      std::size_t top_k = -1,
      bool ignore_eos = false,
      std::size_t max_tokens = 2048)
      : temperature(temperature),
        top_p(top_p),
        top_k(top_k),
        ignore_eos(ignore_eos),
        max_tokens(max_tokens)
  {
    VerifyArgs();
    if (temperature < SAMPLING_EPS)
      VerifyGreedySampling();
  }

  inline SamplingType GetSamplingType() const
  {
    return (temperature < SAMPLING_EPS) ? SamplingType::Greedy
                                        : SamplingType::Random;
  }

  std::string ToString() const
  {
    return fmt::format(
        "SamplingParams("
        "Temperature: {},"
        "TopP: {},"
        "TopK: {},"
        "IgnoreEos: {},"
        "NumMaxtokens: {})",
        temperature,
        top_p,
        top_k,
        ignore_eos,
        max_tokens);
  }

  const double temperature;
  const double top_p;
  const int top_k;
  const bool ignore_eos;
  const std::size_t max_tokens;

private:
  void VerifyArgs() const;
  void VerifyGreedySampling() const;
};
} // namespace vajra
