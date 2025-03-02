// #pragma once

// #include <torch/all.h>

// #include "Logging.h"
// #include "StdCommon.h"

// #include "ParallelOps.h"
// #include "ProcessGroupWrapper.h"

// #include "FlashinferAll.h"
// //==============================================================================
// namespace vajra
// {
// //==============================================================================
// class FlashinferAttentionWrapper
// {
// public:
//   FlashinferAttentionWrapper(
//       BatchPrefillWithPagedKVCachePyTorchWrapper& wrapper,
//       const std::shared_ptr<ProcessGroupWrapper> spProcessGroupWrapper,
//       int nNumQHeads,
//       int nNumKvHeads,
//       int nHeadDim,
//       int nCacheParallelRank,
//       unsigned int nLayout = 0,
//       float nSoftmaxScale = 1,
//       unsigned int nPosEncodingMode = 0,
//       bool bAllowFp16QKReduction = false,
//       int nWindowLeft = -1,
//       float nLogitsSoftCap = 0.0,
//       float nRopeScale = 1.0,
//       float nRopeTheta = 10000.0,
//       bool bSkipAttentionReduction = false);

//   void BeginForward(
//       bool bContainsMultiGroupPrefillSeq /*[in]*/,
//       bool bContainsMultiGroupDecodeSeq /*[in]*/,
//       unsigned int nMultiGroupSeqPrefillLen /*[in]*/,
//       const std::set<int>& vMultiGroupSeqGroupIds /*[in]*/,
//       const torch::Tensor& qoIndptr /*[in]*/,
//       const torch::Tensor& kvIndptr /*[in]*/,
//       const torch::Tensor& kvIndices /*[in]*/,
//       const torch::Tensor& kvLastPageLen /*[in]*/
//   );

//   void EndForward();

//   std::vector<torch::Tensor> Forward(
//       float nSoftmaxScale /*[in]*/,
//       const torch::Tensor& q /*[in]*/,
//       const torch::Tensor& kvCache /*[inout]*/,
//       bool bCausal = true /*[in]*/
//   );

//   torch::Tensor GatherTensor(
//       const torch::Tensor& output,
//       const torch::Tensor& S,
//       bool bContainsMultiGroupPrefillSeq,
//       bool bContainsMultiGroupDecodeSeq,
//       unsigned int nMultiGroupSeqPrefillLen,
//       const std::set<int>& vMultiGroupSeqGroupIds);

// private:
//   // Initialization parameters
//   BatchPrefillWithPagedKVCachePyTorchWrapper& m_wrapper;
//   std::shared_ptr<ProcessGroupWrapper> m_spProcessGroupWrapper;
//   int m_nNumQHeads;
//   int m_nNumKvHeads;
//   int m_nHeadDim;
//   int m_nCacheParallelRank;
//   unsigned int m_nLayout;
//   float m_nSoftmaxScale;
//   unsigned int m_nPosEncodingMode;
//   bool m_bAllowFp16QKReduction;
//   int m_nWindowLeft;
//   float m_nLogitsSoftCap;
//   float m_nRopeScale;
//   float m_nRopeTheta;
//   bool m_bSkipAttentionReduction;
//   bool bShouldPrintLog;

//   // Runtime parameters
//   bool m_bBeginForwardCalled = false;
//   bool m_bContainsMultiGroupPrefillSeq;
//   bool m_bContainsMultiGroupDecodeSeq;
//   unsigned int m_nMultiGroupSeqPrefillLen;
//   std::set<int> m_vMultiGroupSeqGroupIds;
//   torch::Tensor m_qoIndptr;
//   torch::Tensor m_kvIndptr;
//   torch::Tensor m_kvIndices;
//   torch::Tensor m_kvLastPageLen;
// };
// //==============================================================================
// } // namespace vajra
// //==============================================================================