# Simple deploy script: pull latest, build image, restart container.
# Supports Docker and Podman. Configure via environment variables.

# Defaults (can be overridden via env):
IMAGE_NAME=${IMAGE_NAME:-trustpilotpraktikpladsbackend:latest}
CONTAINER_NAME=${CONTAINER_NAME:-trustpilotpraktikplads-backend}
PORT=${PORT:-2500}
APP_DIR=${APP_DIR:-.}
BUILD_CONTEXT=${BUILD_CONTEXT:-.}
DOCKER_CMD=${DOCKER_CMD:-docker}
RECREATE=${RECREATE:-true} # if true, stop/remove old container

echo "Deploying with ${DOCKER_CMD}..."

cd "$(dirname "$0")/.." || exit 1

echo "Pulling latest code from git..."
git pull --rebase

echo "Building image ${IMAGE_NAME}..."
${DOCKER_CMD} build -t "${IMAGE_NAME}" "${BUILD_CONTEXT}"

if [ "${RECREATE}" = "true" ]; then
	if ${DOCKER_CMD} ps -a --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
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

