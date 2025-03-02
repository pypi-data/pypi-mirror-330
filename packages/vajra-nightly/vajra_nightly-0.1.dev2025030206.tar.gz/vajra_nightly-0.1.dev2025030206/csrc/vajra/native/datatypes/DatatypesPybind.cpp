#include "vajra/native/datatypes/DatatypesPybind.h"
#include "vajra/native/datatypes/Block.h"
#include "vajra/native/datatypes/SamplerOutput.h"
#include "vajra/native/datatypes/SamplingParams.h"
#include "vajra/native/datatypes/SequenceMetadata.h"
#include "vajra/native/datatypes/SequenceStatus.h"
#include <pybind11/stl_bind.h>
//==============================================================================
PYBIND11_MAKE_OPAQUE(vajra::SamplerOutputs)
void InitDatatypesPybindSubmodule(py::module_& pm)
{
  auto m = pm.def_submodule("datatypes", "Datatypes submodule");

  py::class_<vajra::SequenceMetadata>(m, "SequenceMetadata")
      .def(
          py::init<
              std::size_t,
              std::string&,
              std::size_t,
              std::size_t,
              std::vector<std::size_t>&,
              std::vector<std::size_t>&,
              bool>(),
          py::arg("schedule_id"),
          py::arg("seq_id"),
          py::arg("num_q_tokens"),
          py::arg("num_kv_tokens"),
          py::arg("block_table"),
          py::arg("kvp_group_ids"),
          py::arg("save_kv_cache"))
      .def("__str__", &vajra::SequenceMetadata::ToString)
      .def("__repr__", &vajra::SequenceMetadata::ToString)
      .def_readonly("schedule_id", &vajra::SequenceMetadata::m_nScheduleId)
      .def_readonly("seq_id", &vajra::SequenceMetadata::m_strSeqId)
      .def_readonly("num_q_tokens", &vajra::SequenceMetadata::m_nNumQTokens)
      .def_readonly("num_kv_tokens", &vajra::SequenceMetadata::m_nNumKvTokens)
      .def_readonly("block_table", &vajra::SequenceMetadata::m_vnBlockTable)
      .def_readonly("kvp_group_ids", &vajra::SequenceMetadata::m_vnKvpGroupIds)
      .def_readonly("save_kv_cache", &vajra::SequenceMetadata::m_bSaveKvCache)
      .def_readonly(
          "is_kvp_request",
          &vajra::SequenceMetadata::m_bIsKvpRequest);
  //==============================================================================
  py::class_<vajra::LogicalTokenBlock>(m, "LogicalTokenBlock")
      .def(
          py::init<std::size_t, std::size_t>(),
          py::arg("block_number"),
          py::arg("block_size"))
      .def_readonly("block_number", &vajra::LogicalTokenBlock::block_number)
      .def_readonly("block_size", &vajra::LogicalTokenBlock::block_size)
      .def_property_readonly(
          "token_ids",
          &vajra::LogicalTokenBlock::GetTokenIds)
      .def_property_readonly(
          "num_tokens",
          &vajra::LogicalTokenBlock::GetNumTokens)
      .def_property_readonly("is_empty", &vajra::LogicalTokenBlock::IsEmpty)
      .def_property_readonly(
          "num_empty_slots",
          &vajra::LogicalTokenBlock::NumEmptySlots)
      .def_property_readonly("is_full", &vajra::LogicalTokenBlock::IsFull)
      .def("append_tokens", &vajra::LogicalTokenBlock::AppendTokens)
      .def("get_last_token_id", &vajra::LogicalTokenBlock::GetLastTokenId)
      .def(py::pickle(
        [](const vajra::LogicalTokenBlock& p) { // __getstate__
            return py::make_tuple(
                p.block_number,
                p.block_size,
                p.GetTokenIdsCopy(),
                p.GetNumTokens());
        },
        [](py::tuple t) { // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 4, "Invalid pickled state for LogicalTokenBlock!");
    
            return vajra::LogicalTokenBlock(
                    t[0].cast<std::size_t>(),
                    t[1].cast<std::size_t>(),
                    t[2].cast<std::vector<std::size_t>>(),
                    t[3].cast<std::size_t>());
        }));
  //==============================================================================
  py::class_<vajra::SamplerOutput>(m, "SamplerOutput")
      .def(
          py::init<std::size_t, std::string&, std::vector<std::size_t>>(),
          py::arg("schedule_id"),
          py::arg("seq_id"),
          py::arg("output_tokens"))
      .def("__str__", &vajra::SamplerOutput::ToString)
      .def("__repr__", &vajra::SamplerOutput::ToString)
      .def_property_readonly(
          "schedule_id",
          &vajra::SamplerOutput::GetScheduleId)
      .def_property_readonly("seq_id", &vajra::SamplerOutput::GetSeqId)
      .def_property_readonly(
          "output_tokens",
          &vajra::SamplerOutput::GetOutputTokens)
          .def(py::pickle(
            [](const vajra::SamplerOutput& p) { // __getstate__
                return py::make_tuple(
                    p.GetScheduleId(),
                    p.GetSeqIdCopy(),
                    p.GetOutputTokensCopy());
            },
            [](py::tuple t) { // __setstate__
                ASSERT_VALID_RUNTIME(t.size() == 3, "Invalid pickled state for SamplerOutput!");
        
                return vajra::SamplerOutput(
                        t[0].cast<std::size_t>(),
                        t[1].cast<std::string>(),
                        t[2].cast<std::vector<std::size_t>>());
            }));
  //==============================================================================
  py::enum_<vajra::SequenceStatus>(m, "SequenceStatus")
      .value("WAITING", vajra::SequenceStatus::Waiting)
      .value("WAITING_PREEMPTED", vajra::SequenceStatus::WaitingPreempted)
      .value("RUNNING", vajra::SequenceStatus::Running)
      .value("PAUSED", vajra::SequenceStatus::Paused)
      .value("FINISHED_STOPPED", vajra::SequenceStatus::FinishedStopped)
      .value(
          "FINISHED_LENGTH_CAPPED",
          vajra::SequenceStatus::FinishedLengthCapped)
      .value("FINISHED_IGNORED", vajra::SequenceStatus::FinishedIgnored)
      .def_static("is_finished", &vajra::sequence_status::IsFinished)
      .def_static("is_executing", &vajra::sequence_status::IsExecuting)
      .def_static("is_waiting", &vajra::sequence_status::IsWaiting)
      .def_static(
          "is_waiting_preempted",
          &vajra::sequence_status::IsWaitingPreempted)
      .def_static("is_paused", &vajra::sequence_status::IsPaused)
      .def_static("is_running", &vajra::sequence_status::IsRunning)
      .def_static(
          "get_finished_reason",
          &vajra::sequence_status::GetFinishedReason);
  //==============================================================================
  py::enum_<vajra::SamplingType>(m, "SamplingType")
      .value("GREEDY", vajra::SamplingType::Greedy)
      .value("RANDOM", vajra::SamplingType::Random);
  //==============================================================================
  py::class_<vajra::SamplingParams>(m, "SamplingParams")
      .def(
          py::init<double, double, int, bool, std::size_t>(),
          py::arg("temperature") = 1.0,
          py::arg("top_p") = 1.0,
          py::arg("top_k") = -1,
          py::arg("ignore_eos") = false,
          py::arg("max_tokens") = 2048)
      .def("__str__", &vajra::SamplingParams::ToString)
      .def("__repr__", &vajra::SamplingParams::ToString)
      .def_readonly("temperature", &vajra::SamplingParams::temperature)
      .def_readonly("top_p", &vajra::SamplingParams::top_p)
      .def_readonly("top_k", &vajra::SamplingParams::top_k)
      .def_readonly("ignore_eos", &vajra::SamplingParams::ignore_eos)
      .def_readonly("max_tokens", &vajra::SamplingParams::max_tokens)
      .def_property_readonly(
          "sampling_type",
          &vajra::SamplingParams::GetSamplingType)
      .def(py::pickle(
      [](const vajra::SamplingParams& p) { // __getstate__
          return py::make_tuple(
              p.temperature,
              p.top_p,
              p.top_k,
              p.ignore_eos,
              p.max_tokens);
      },
      [](py::tuple t) { // __setstate__
          ASSERT_VALID_RUNTIME(t.size() == 5, "Invalid pickled state for SamplingParams!");
  
          return vajra::SamplingParams(
                t[0].cast<double>(),
                t[1].cast<double>(),
                t[2].cast<int>(),
                t[3].cast<bool>(),
                t[4].cast<std::size_t>());
      }));
}
//==============================================================================
