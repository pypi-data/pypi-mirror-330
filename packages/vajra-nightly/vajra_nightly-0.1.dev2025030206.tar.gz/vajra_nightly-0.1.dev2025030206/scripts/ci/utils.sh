#!/bin/bash
set -ex

# This script contains utility functions that can be shared across different scripts
# Note: This script should be sourced from other scripts and not executed directly
# and it is only suppose to contain function definitions & not any executable code

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
_root_dir=$(dirname $(dirname $_script_dir))

assert_env() {
    local var_name="$1"
    if [ -z "${!var_name}" ]; then
        echo "Error: Environment variable '$var_name' is not set."
        exit 1
    fi
}

function switch_to_root_dir() {
    cd "$_root_dir"
}

function init_conda() {
    export PATH="${HOME}/conda/bin:${PATH}"
    mamba init bash
    mamba init zsh
    source /root/conda/etc/profile.d/conda.sh
}

function login_huggingface() {
    huggingface-cli login --token "$HUGGINGFACE_TOKEN"
}

function activate_vajra_conda_env() {
    conda activate vajra
}

function create_vajra_conda_env() {
    echo "::group::Create conda environment"
    pushd "$_root_dir"
    mamba env create -f environment-dev.yml -n vajra
    popd
    echo "::endgroup::"
}

function install_pip_dependencies() {
    assert_env VAJRA_CI_CUDA_VERSION
    assert_env VAJRA_CI_TORCH_VERSION

    CUDA_MAJOR="${VAJRA_CI_CUDA_VERSION%.*}"
    CUDA_MINOR="${VAJRA_CI_CUDA_VERSION#*.}"

    pushd "$_root_dir"

    echo "::group::Install PyTorch"
    pip install torch==${VAJRA_CI_TORCH_VERSION}.* \
        --index-url "https://download.pytorch.org/whl/cu${CUDA_MAJOR}${CUDA_MINOR}"
    echo "::endgroup::"

    echo "::group::Install other dependencies"
    pip install -r requirements.txt \
        --extra-index-url https://flashinfer.ai/whl/cu${CUDA_MAJOR}${CUDA_MINOR}/torch${VAJRA_CI_TORCH_VERSION}/
    echo "::endgroup::"

    popd
}

function build_vajra_editable() {
    pushd "$_root_dir"
    echo "::group::Build Vajra in editable mode"
    make build
    echo "::endgroup::"
    popd
}