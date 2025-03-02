# Vajra Development Container Makefile

# Default values - can be overridden when calling make
CUDA_VERSION ?= 12.4.1
PYTORCH_VERSION ?= 2.4
ORGANIZATION ?= $(shell git config --get remote.origin.url | sed -E 's/.*[:/]([^/]+)\/[^/]+\.git/\1/')
IMAGE_NAME ?= vajra-dev
REGISTRY ?= ghcr.io
TAG ?= cuda$(CUDA_VERSION)-torch$(PYTORCH_VERSION)
CONTAINER_NAME ?= vajra-dev-container-manual
GPU_FLAG ?= all
SHM_SIZE ?= 12gb

# Path configurations
REPO_ROOT := $(shell git rev-parse --show-toplevel)
HOME := $(shell echo ~)
DOCKERFILE_PATH := $(REPO_ROOT)/docker/containers/dev/Dockerfile
SSH_AUTH_SOCK ?= $(shell echo $$SSH_AUTH_SOCK)
SSH_AGENT_MOUNT ?= $(if $(SSH_AUTH_SOCK),-v $(SSH_AUTH_SOCK):/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent,)

.PHONY: help build run clean

help:
	@echo "Vajra Development Container Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help                 - Show this help message"
	@echo "  build                - Build container with specific versions"
	@echo "                         Usage: make build CUDA_VERSION=11.8 PYTORCH_VERSION=2.0"
	@echo "  start                - Start the container with specific versions"
	@echo "                         Usage: make start CUDA_VERSION=11.8 PYTORCH_VERSION=2.0"
	@echo "  stop                 - Stop the running container"
	@echo "  run                  - Run the container with repo root mounted"
	@echo "                         Usage: make run [CUDA_VERSION=11.8] [PYTORCH_VERSION=2.0]"
	@echo "  clean                - Remove the container and image"
	@echo ""
	@echo "Environment variables:"
	@echo "  CUDA_VERSION         - CUDA version (default: 12.4.1)"
	@echo "  PYTORCH_VERSION      - PyTorch version (default: 2.4)"
	@echo "  ORGANIZATION         - GitHub organization name (default: derived from git)"
	@echo "  IMAGE_NAME           - Image name (default: vajra-dev)"
	@echo "  REGISTRY             - Container registry (default: ghcr.io)"
	@echo "  TAG                  - Image tag (default: cuda<version>-torch<version>)"
	@echo "  CONTAINER_NAME       - Running container name (default: vajra-dev-container)"
	@echo "  GPU_FLAG             - GPU flag for docker run (default: all)"
	@echo "  SHM_SIZE             - Shared memory size (default: 12gb)"

# Build with specific CUDA and PyTorch versions
build:
	@echo "Building container with CUDA $(CUDA_VERSION) and PyTorch $(PYTORCH_VERSION)..."
	docker build \
		--build-arg CUDA_VERSION=$(CUDA_VERSION) \
		--build-arg PYTORCH_VERSION=$(PYTORCH_VERSION) \
		-t $(REGISTRY)/$(ORGANIZATION)/$(IMAGE_NAME):$(TAG) \
		-f $(DOCKERFILE_PATH) \
		$(REPO_ROOT)

# Run the container with the repository root mounted
run:
	@echo "Running container with CUDA $(CUDA_VERSION) and PyTorch $(PYTORCH_VERSION)..."
	@echo "Mounting repository root to /repo in the container"
	docker run -it --rm \
		--name $(CONTAINER_NAME) \
		--gpus $(GPU_FLAG) \
		--shm-size=$(SHM_SIZE) \
		-v $(REPO_ROOT):/repo \
		-v /tmp/.zsh_history_vajra:/root/.zsh_history \
		-w /repo \
		$(SSH_AGENT_MOUNT) \
		$(REGISTRY)/$(ORGANIZATION)/$(IMAGE_NAME):$(TAG)

# Start the container with specific versions
start:
	@echo "Starting long-running container with CUDA $(CUDA_VERSION) and PyTorch $(PYTORCH_VERSION)..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		--gpus $(GPU_FLAG) \
		--shm-size=$(SHM_SIZE) \
		-v $(REPO_ROOT):/repo \
		-v /tmp/.zsh_history_vajra:/root/.zsh_history \
		-w /repo \
		$(SSH_AGENT_MOUNT) \
		$(REGISTRY)/$(ORGANIZATION)/$(IMAGE_NAME):$(TAG) \
		sleep infinity

# Stop the running container
stop:
	@echo "Stopping container..."
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true

# Clean up container and image
clean:
	@echo "Cleaning up container and image..."
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true
	-docker rm $(CONTAINER_NAME) 2>/dev/null || true
	-docker rmi $(REGISTRY)/$(ORGANIZATION)/$(IMAGE_NAME):$(TAG) 2>/dev/null || true
	-docker rmi $(IMAGE_NAME):latest 2>/dev/null || true
