# Simple deploy script: pull latest, build image, restart container.
# Supports Docker and Podman. Configure via environment variables.

# Defaults (can be overridden via env):
IMAGE_NAME=${IMAGE_NAME:-trustpilotpraktikpladsbackend:latest}
CONTAINER_NAME=${CONTAINER_NAME:-trustpilotpraktikplads-backend}
PORT=${PORT:-2500}
BUILD_CONTEXT=${BUILD_CONTEXT:-.}
# If DOCKER_CMD is set externally, use it; otherwise auto-detect docker or podman.
DOCKER_CMD=${DOCKER_CMD:-}
RECREATE=${RECREATE:-true} # if true, stop/remove old container

if [ -z "${DOCKER_CMD}" ]; then
	if command -v docker >/dev/null 2>&1; then
		DOCKER_CMD=docker
	elif command -v podman >/dev/null 2>&1; then
		DOCKER_CMD=podman
	else
		echo "Error: neither 'docker' nor 'podman' found in PATH. Install one or set DOCKER_CMD." >&2
		exit 1
	fi
fi

echo "Deploying with ${DOCKER_CMD}..."

cd "$(dirname "$0")/.." || exit 1

echo "Pulling latest code from git..."
git pull --rebase || git pull || true

echo "Building image ${IMAGE_NAME}..."
${DOCKER_CMD} build -t "${IMAGE_NAME}" "${BUILD_CONTEXT}"

if [ "${RECREATE}" = "true" ]; then
	# Check for existing container by exact name
	if ${DOCKER_CMD} ps -a --format '{{.Names}}' 2>/dev/null | grep -Fxq "${CONTAINER_NAME}"; then
		echo "Stopping container ${CONTAINER_NAME}..."
		${DOCKER_CMD} stop "${CONTAINER_NAME}" || true
		echo "Removing container ${CONTAINER_NAME}..."
		${DOCKER_CMD} rm "${CONTAINER_NAME}" || true
	fi
fi

echo "Starting container ${CONTAINER_NAME} on port ${PORT}..."
# Run in detached mode and map port
${DOCKER_CMD} run -d \
	--name "${CONTAINER_NAME}" \
	-p ${PORT}:${PORT} \
	--restart unless-stopped \
	"${IMAGE_NAME}"

echo "Deploy finished."

exit 0

