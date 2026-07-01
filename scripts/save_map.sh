#!/bin/bash
set -euo pipefail

MAPS_DIR="${HOME}/maps"
if [[ ! -d "${MAPS_DIR}" ]]; then
	echo "==> Creating ${MAPS_DIR}..."
	mkdir -p "${MAPS_DIR}"
fi

MAP_NAME="my_map_${date +%Y%m%d_%H%M}"
MAP_PATH="${MAPS_DIR}/${MAP_NAME}"

echo "==> Saving map to ${MAP_PATH}.{pgm,yaml}..."
ros2 run nav2_map_server map_saver_cli -f "${MAP_PATH}"

echo "==> Done. Saved:"
echo "      ${MAP_PATH}.pgm"
echo "      ${MAP_PATH}.yaml"
