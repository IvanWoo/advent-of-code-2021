#!/user/bin/env bash
set -eu -o pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${BASE_DIR}/../config.sh"

if [ -z "${1:-}" ]; then
    printf "Usage: ${0} 42 \n"
    exit 1
fi

DAY="${1}"
DAY_DIR="${PROJECT_DIR}/${DAY}"

main() {
    echo "Creating new day ${DAY}"
    mkdir -p "${DAY_DIR}"
    touch "${DAY_DIR}/main.py"
    touch "${DAY_DIR}/input.txt"
}

main
