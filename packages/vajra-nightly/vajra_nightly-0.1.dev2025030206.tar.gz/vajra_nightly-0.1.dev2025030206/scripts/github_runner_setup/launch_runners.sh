#!/bin/bash
set -e

# Configuration
SPEC_FILE="${1}"
GITHUB_URL="${2}"
GITHUB_ORG="${3}"
# Accept token from multiple possible sources with credential directory being highest priority
GITHUB_TOKEN="${4}"
DOCKER_IMAGE="myoung34/github-runner:latest"
LOG_FILE="/var/log/github-runners.log"

# Function to log messages with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Validate token
if [ -z "$GITHUB_TOKEN" ]; then
    log "ERROR: No GitHub token provided. Set token via systemd credential, environment variable, or command argument."
    exit 1
fi

# Token validation and obscuring in logs
TOKEN_LENGTH=${#GITHUB_TOKEN}
MASKED_TOKEN="${GITHUB_TOKEN:0:4}...${GITHUB_TOKEN: -4}"
log "Using GitHub token: $MASKED_TOKEN (length: $TOKEN_LENGTH)"

# Trap signals for clean shutdown
trap 'log "Received shutdown signal. Exiting..."; exit 0' SIGTERM SIGINT

# Create log file if it doesn't exist
touch "$LOG_FILE"
log "Starting GitHub Actions Runner service"

# Check dependencies
command -v docker >/dev/null 2>&1 || { log "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { log "jq is required but not installed. Aborting." >&2; exit 1; }
command -v nvidia-smi >/dev/null 2>&1 || { log "nvidia-smi is required but not installed. Aborting." >&2; exit 1; }

# Check if spec file exists
if [ ! -f "$SPEC_FILE" ]; then
    echo "Spec file not found: $SPEC_FILE" >&2
    exit 1
fi

# Check if spec file is valid JSON
if ! jq empty "$SPEC_FILE" 2>/dev/null; then
    echo "Invalid JSON in spec file: $SPEC_FILE" >&2
    exit 1
fi

# Get total number of GPUs in system
GPU_COUNT=$(nvidia-smi --list-gpus | wc -l)
echo "Detected $GPU_COUNT GPUs in the system"

# Initialize GPU allocation tracking
declare -A GPU_ALLOCATION
for ((i=0; i<$GPU_COUNT; i++)); do
    GPU_ALLOCATION[$i]=0
done

# Function to allocate GPUs
allocate_gpus() {
    local required_gpus=$1
    local result=""
    local count=0
    
    if [ $required_gpus -eq 0 ]; then
        echo ""
        return
    fi
    
    for gpu_id in "${!GPU_ALLOCATION[@]}"; do
        if [ ${GPU_ALLOCATION[$gpu_id]} -eq 0 ]; then
            if [ -z "$result" ]; then
                result="$gpu_id"
            else
                result="$result,$gpu_id"
            fi
            GPU_ALLOCATION[$gpu_id]=1
            ((count++))
            
            if [ $count -eq $required_gpus ]; then
                break
            fi
        fi
    done
    
    if [ $count -lt $required_gpus ]; then
        echo "Warning: Requested $required_gpus GPUs but only $count available" >&2
    fi
    
    echo "$result"
}

# Read the spec file and create runners
echo "Reading runner specification from $SPEC_FILE"
jq -c '.[]' "$SPEC_FILE" | while read -r spec; do
    num_gpus=$(echo "$spec" | jq -r '.num_gpus')
    num_instances=$(echo "$spec" | jq -r '.num_instances')
    runner_name_prefix=$(echo "$spec" | jq -r '.runner_name_prefix')
    runner_tags=$(echo "$spec" | jq -r '.tags | join(",")')

    echo "Configuring runner group: $runner_name_prefix with $num_instances instances, each with $num_gpus GPUs"

    for ((i=1; i<=$num_instances; i++)); do
        runner_name="${runner_name_prefix}-${i}"
        allocated_gpus=$(allocate_gpus $num_gpus)
        
        # Container name
        container_name="gh-runner-${runner_name}"
        
        # Check if container already exists
        if docker ps -a --filter "name=$container_name" --format '{{.Names}}' | grep -q "^$container_name$"; then
            log "WARNING: Container $container_name already exists. Removing it first..."
            docker rm -f "$container_name" || log "Failed to remove existing container $container_name"
        fi
        
        # Prepare Docker run command
        docker_cmd="docker run -d --restart always --name $container_name"
        
        # Add GPU configuration if GPUs are allocated
        if [ ! -z "$allocated_gpus" ]; then
            gpu_env="--env NVIDIA_VISIBLE_DEVICES=$allocated_gpus"
        else
            gpu_env="--env NVIDIA_VISIBLE_DEVICES="
        fi

        # Add GitHub Actions runner configuration
        docker_cmd="$docker_cmd $gpu_env \
            --env ORG_NAME=$GITHUB_ORG \
            --env RUNNER_SCOPE=org \
            --env RUNNER_NAME=$runner_name \
            --env ACCESS_TOKEN=$GITHUB_TOKEN \
            --env LABELS="self-hosted,$runner_tags" \
            --env RUNNER_WORKDIR=/tmp/github-runner-$runner_name \
            --volume /var/run/docker.sock:/var/run/docker.sock \
            --volume /tmp/github-runner-$runner_name:/tmp/github-runner-$runner_name \
            $DOCKER_IMAGE"

        log "Launching container for runner: $runner_name with GPUs: $allocated_gpus"
        eval $docker_cmd || {
            log "ERROR: Failed to start container $container_name"
            # Release allocated GPUs on failure
            for gpu_id in $(echo "$allocated_gpus" | tr ',' ' '); do
                GPU_ALLOCATION[$gpu_id]=0
            done
        }
        
        echo "Runner $runner_name started successfully"
    done
done

log "All runner containers have been started"
log "GPU Allocation Summary:"
for gpu_id in "${!GPU_ALLOCATION[@]}"; do
    if [ ${GPU_ALLOCATION[$gpu_id]} -eq 1 ]; then
        status="Allocated"
    else
        status="Available"
    fi
    log "GPU $gpu_id: $status"
done

# Check for unallocated GPUs
unallocated=$(printf "%s\n" "${GPU_ALLOCATION[@]}" | grep -c "0")
if [ $unallocated -gt 0 ]; then
    log "Warning: $unallocated GPUs remain unallocated"
fi

# Add health monitoring loop
log "Entering monitoring mode to ensure containers remain running..."
while true; do
    sleep 300  # Check every 5 minutes
    
    # Get list of expected runner container names
    expected_containers=$(docker ps --filter "name=gh-runner-" --format "{{.Names}}" | sort)
    expected_count=$(echo "$expected_containers" | wc -l)
    
    # Check if any containers stopped
    running_containers=$(docker ps --filter "name=gh-runner-" --format "{{.Names}}" | sort)
    running_count=$(echo "$running_containers" | wc -l)
    
    if [ "$running_count" -lt "$expected_count" ]; then
        log "Warning: Some containers are not running. Expected $expected_count, found $running_count"
        
        # Restart any stopped containers
        for container in $expected_containers; do
            if ! docker ps --filter "name=$container" --format "{{.Names}}" | grep -q "$container"; then
                log "Restarting container: $container"
                docker start "$container" || log "Failed to restart container: $container"
            fi
        done
    else
        log "Health check: All $running_count containers are running"
    fi
done
