########################################################################################################################################################
###
### Copyright (C) 2025 by Georgia Institute of Technology
###
### This file is part of the vajra project.
###
########################################################################################################################################################
### @file                       src/CMakeLists.txt
### @author                     Vajra Team <agawalamey12@gmail.com>
### @date                       25th Jan 2025
########################################################################################################################################################
# Derived from vLLM's CMakeLists.txt
########################################################################################################################################################
cmake_minimum_required(VERSION 3.22)

project(vajra_extensions LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "-g -O3")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
########################################################################################################################################################
# Supported python versions.  These versions will be searched in order, the
# first match will be selected.  These should be kept in sync with setup.py.
set(PYTHON_SUPPORTED_VERSIONS "3.8" "3.9" "3.10" "3.11")
# Supported NVIDIA architectures.
set(CUDA_SUPPORTED_ARCHS "7.0;7.5;8.0;8.6;8.9;9.0")
# Should be kept in sync with the version in requirements.txt and pyproject.toml.
set(TORCH_SUPPORTED_VERSION_CUDA "2.4")
set(gflags_DIR "${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/gflags")
set(GTest_DIR "${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/googletest")
set(glog_DIR "${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/glog")
########################################################################################################################################################
include(${CMAKE_CURRENT_LIST_DIR}/cmake/utils.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/cmake/FindFlashinfer.cmake)
########################################################################################################################################################
# Add third_party libraries
add_subdirectory(csrc/third_party/gflags)

# Configure GTest
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
add_subdirectory(csrc/third_party/googletest)

add_subdirectory(csrc/third_party/glog)
add_subdirectory(csrc/third_party/fmt)

# Try to find python package with an executable that exactly matches
# `VAJRA_PYTHON_EXECUTABLE` and is one of the supported versions.
if (VAJRA_PYTHON_EXECUTABLE)
  find_python_from_executable(${VAJRA_PYTHON_EXECUTABLE} "${PYTHON_SUPPORTED_VERSIONS}")
else()
  message(FATAL_ERROR
    "Please set VAJRA_PYTHON_EXECUTABLE to the path of the desired python version"
    " before running cmake configure.")
endif()
# Update cmake's `CMAKE_PREFIX_PATH` with torch location.
# This allows us to pick torch directly from the environment.
append_cmake_prefix_path("torch" "torch.utils.cmake_prefix_path")
# Import torch cmake configuration.
# Torch also imports CUDA languages with some customizations,
# so there is no need to do this explicitly with check_language/enable_language, etc.
find_package(Torch REQUIRED)
########################################################################################################################################################
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

execute_process(
        COMMAND python3 -c "import torch; print(torch._C._PYBIND11_COMPILER_TYPE, end='')"
        OUTPUT_VARIABLE _PYBIND11_COMPILER_TYPE
)
execute_process(
        COMMAND python3 -c "import torch; print(torch._C._PYBIND11_STDLIB, end='')"
        OUTPUT_VARIABLE _PYBIND11_STDLIB
)
execute_process(
        COMMAND python3 -c "import torch; print(torch._C._PYBIND11_BUILD_ABI, end='')"
        OUTPUT_VARIABLE _PYBIND11_BUILD_ABI
)

message(STATUS "PYBIND11_COMPILER_TYPE:" ${_PYBIND11_COMPILER_TYPE})
message(STATUS "PYBIND11_STDLIB:" ${_PYBIND11_STDLIB})
message(STATUS "PYBIND11_BUILD_ABI:" ${_PYBIND11_BUILD_ABI})

add_compile_definitions(PYBIND11_COMPILER_TYPE="${_PYBIND11_COMPILER_TYPE}" PYBIND11_STDLIB="${_PYBIND11_STDLIB}" PYBIND11_BUILD_ABI="${_PYBIND11_BUILD_ABI}" C10_USE_GLOG="ON")
########################################################################################################################################################
# Normally `torch.utils.cpp_extension.CUDAExtension` would add
# `libtorch_python.so` for linking against an extension. Torch's cmake
# configuration does not include this library (presumably since the cmake
# config is used for standalone C++ binaries that link against torch).
# The `libtorch_python.so` library defines some of the glue code between
# torch/python via pybind and is required by VAJRA extensions for this
# reason. So, add it by manually using `append_torchlib_if_found` from
# torch's cmake setup.
append_torchlib_if_found(torch_python)
########################################################################################################################################################
# Set up GPU language and check the torch version and warn if it isn't
# what is expected.
if (CUDA_FOUND)
  set(VAJRA_GPU_LANG "CUDA")

  if (NOT Torch_VERSION VERSION_EQUAL ${TORCH_SUPPORTED_VERSION_CUDA})
    message(WARNING "Pytorch version ${TORCH_SUPPORTED_VERSION_CUDA} "
      "expected for CUDA build, saw ${Torch_VERSION} instead.")
  endif()
else()
    message(FATAL_ERROR "Can't find CUDA installation.")
endif()
########################################################################################################################################################
# Override the GPU architectures detected by cmake/torch and filter them by
# the supported versions for the current language.
# The final set of arches is stored in `VAJRA_GPU_ARCHES`.
override_gpu_arches(VAJRA_GPU_ARCHES
  ${VAJRA_GPU_LANG}
  "${${VAJRA_GPU_LANG}_SUPPORTED_ARCHS}"
)

# Query torch for additional GPU compilation flags for the given
# `VAJRA_GPU_LANG`.
# The final set of arches is stored in `VAJRA_GPU_FLAGS`.
get_torch_gpu_compiler_flags(VAJRA_GPU_FLAGS ${VAJRA_GPU_LANG})
########################################################################################################################################################
# Set nvcc parallelism.
if(NVCC_THREADS AND VAJRA_GPU_LANG STREQUAL "CUDA")
  list(APPEND VAJRA_GPU_FLAGS "--threads=${NVCC_THREADS}")
endif()
########################################################################################################################################################
# Define extension targets
########################################################################################################################################################
# glob all files in csrc/kernels
file(GLOB_RECURSE VAJRA_KERNEL_COMMONS_EXT_SRC "csrc/vajra/kernels/*.cu")

define_gpu_static_target(
  _kernels_common
  DESTINATION vajra
  LANGUAGE ${VAJRA_GPU_LANG}
  SOURCES ${VAJRA_KERNEL_COMMONS_EXT_SRC}
  COMPILE_FLAGS ${VAJRA_GPU_FLAGS}
  ARCHITECTURES ${VAJRA_GPU_ARCHES}
)
########################################################################################################################################################
file(GLOB_RECURSE VAJRA_KERNELS_EXT_SRC "csrc/vajra/kernels/*.cpp")

define_gpu_extension_target(
  _kernels
  DESTINATION vajra
  LANGUAGE ${VAJRA_GPU_LANG}
  SOURCES ${VAJRA_KERNELS_EXT_SRC}
  COMPILE_FLAGS ${VAJRA_GPU_FLAGS}
  ARCHITECTURES ${VAJRA_GPU_ARCHES}
  LIBRARIES _kernels_common
  WITH_SOABI
)
########################################################################################################################################################
file(GLOB_RECURSE VAJRA_NATIVE_SRC "csrc/vajra/native/**/*.cpp")


define_gpu_extension_target(
  _native
  DESTINATION vajra
  LANGUAGE ${VAJRA_GPU_LANG}
  SOURCES ${VAJRA_NATIVE_SRC} "csrc/vajra/native/pybind.cpp"
  COMPILE_FLAGS ${VAJRA_GPU_FLAGS}
  ARCHITECTURES ${VAJRA_GPU_ARCHES}
  LIBRARIES _kernels_common Flashinfer::Flashinfer
  WITH_SOABI
)
########################################################################################################################################################
# Add the `default` target which detects which extensions should be
# built based on platform/architecture.  This is the same logic that
# setup.py uses to select which extensions should be built and should
# be kept in sync.
#
# The `default` target makes direct use of cmake easier since knowledge
# of which extensions are supported has been factored in, e.g.
#
# mkdir -p build && cd build
# cmake -G Ninja -DVAJRA_PYTHON_EXECUTABLE=`which python3` -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=../vajra ..
# cmake --build . --target default
add_custom_target(default)
add_dependencies(default _kernels)
add_dependencies(default _native)
########################################################################################################################################################
# Add individual test suites
add_test_suite(kernel "csrc/test/kernels")
add_test_suite(native "csrc/test/native")

add_custom_target(all_tests)
add_dependencies(all_tests default)
add_dependencies(all_tests kernel_tests native_tests)

# Enable CTest
enable_testing()
########################################################################################################################################################
