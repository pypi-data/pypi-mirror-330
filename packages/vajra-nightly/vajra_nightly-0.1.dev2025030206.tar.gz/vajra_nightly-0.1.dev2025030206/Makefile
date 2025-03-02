.PHONY: help lint lint/black lint/isort lint/autoflake lint/pyright lint/clang lint/codespell \
       format format/black format/isort format/autoflake format/clang \
       docs docs/build docs/clean \
       build build/native build/native_test \
       test test/performance test/correctness test/functional test/pyunit test/ctest test/unit

.DEFAULT_GOAL := help

CPP_FILES := $(shell find csrc -type f \( -name "*.cpp" -o -name "*.h" \) -not -path "*/third_party/*")

# Use environment variables if defined, otherwise use defaults
ifdef VAJRA_CI_CUDA_VERSION
  CUDA_MAJOR := $(shell echo $(VAJRA_CI_CUDA_VERSION) | cut -d. -f1)
  CUDA_MINOR := $(shell echo $(VAJRA_CI_CUDA_VERSION) | cut -d. -f2)
  CUDA_VERSION := cu$(CUDA_MAJOR)$(CUDA_MINOR)
else
  CUDA_VERSION := cu124
endif

TORCH_VERSION ?= $(if $(VAJRA_CI_TORCH_VERSION),$(VAJRA_CI_TORCH_VERSION),2.4)

lint/black: ## check style with black
	black --check vajra test

lint/isort: ## check style with isort
	isort --check-only --profile black vajra test

lint/autoflake: ## check for unused imports
	autoflake --recursive --remove-all-unused-imports --check vajra test

lint/pyright: ## run type checking
	pyright

lint/clang:
	clang-tidy $(CPP_FILES) \
		-checks='-*,readability-*,modernize-*,cppcoreguidelines-*,performance-*,\
		-modernize-use-trailing-return-type,-readability-identifier-length' \
		-- -std=c++20
	cpplint --filter=-legal/copyright,-build/include_order,-readability/braces $(CPP_FILES)
	clang-format --dry-run -Werror -i $(CPP_FILES)

lint/codespell:
	codespell --skip './csrc/third_party/**,./build/**,*.log,./env/**,./docs/_build/**' -L inout

# TODO(Amey, Mayank, Hieu): Enable clang linting
lint: lint/isort lint/black lint/autoflake lint/codespell lint/pyright

format/black: ## format code with black
	black vajra test

format/isort: ## format code with isort
	isort --profile black vajra test

format/autoflake: ## remove unused imports
	autoflake --in-place --recursive --remove-all-unused-imports vajra test

format/clang:
	clang-format -i $(CPP_FILES)

format: format/isort format/autoflake format/black format/clang ## format code

docs: docs/build ## build documentation

docs/build: ## build documentation
	make -C docs html

docs/clean: ## clean documentation
	make -C docs clean

build/native:
	mkdir -p build \
	&& cd build \
	&& cmake -G Ninja -DVAJRA_PYTHON_EXECUTABLE=`which python3` -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=../vajra .. \
	&& cmake --build . --target default

build/native_test:
	mkdir -p build \
	&& cd build \
	&& cmake -G Ninja -DVAJRA_PYTHON_EXECUTABLE=`which python3` -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=../vajra .. \
	&& cmake --build . --target all_tests

build: ## build the project
	pip install -r requirements.txt --extra-index-url https://flashinfer.ai/whl/$(CUDA_VERSION)/torch$(TORCH_VERSION)/ \
	&& pip install -e . --extra-index-url https://flashinfer.ai/whl/$(CUDA_VERSION)/torch$(TORCH_VERSION)/

# Pytest commands use configuration from pytest.ini
test/performance: ## run performance tests
	pytest -m performance

test/correctness: ## run correctness tests
	@echo "correctness tests not yet implemented!\n"

test/functional: test/performance test/correctness ## run all functional tests

test/pyunit: ## run python unit tests
	pytest -m "unit or integration"

test/ctest: build/native_test ## run ctest tests
	cd build && ctest -R "kernel_tests|native_tests"

test/unit: test/pyunit test/ctest

test: test/unit test/functional ## run all tests

help: ## show this help
	@grep -E '^[a-zA-Z_/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
