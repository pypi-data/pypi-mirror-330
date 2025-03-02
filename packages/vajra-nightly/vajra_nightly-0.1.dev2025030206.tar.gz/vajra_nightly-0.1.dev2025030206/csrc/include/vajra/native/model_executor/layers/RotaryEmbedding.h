#pragma once

#include <torch/all.h>

#include "vajra/commons/Logging.h"
#include "vajra/commons/StdCommon.h"
//==============================================================================
namespace vajra
{
//==============================================================================
class RotaryEmbedding
{
public:
  RotaryEmbedding(
      int nHeadSize,
      int nRotaryDim,
      long nMaxPositionEmbeddings,
      long nBase,
      bool bIsNeoxStyle,
      const torch::Tensor& cosSinCache);

  void Forward(
      const torch::Tensor& positions /*[in]*/,
      torch::Tensor& query /*[inout]*/,
      torch::Tensor& key /*[inout]*/
  ) const;

private:
  int m_nHeadSize;
  int m_nRotaryDim;
  long m_nMaxPositionEmbeddings;
  long m_nBase;
  bool m_bIsNeoxStyle;
  const torch::Tensor m_cosSinCache;
};
//==============================================================================
} // namespace vajra
//==============================================================================
