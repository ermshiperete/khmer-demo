#!/bin/bash
set -eu

SCRIPT_DIR=$(realpath "$(dirname "$0")")
cd "${SCRIPT_DIR}"

if [[ ! -d venv ]]; then
  ./install.sh "$@"
fi

. venv/bin/activate

ARGS=()
if [[ -f venv/usesnap ]]; then
  ARGS+=(--snap)
fi

while [[ $# -gt 0 ]]; do
  case $1 in
    --help|-h)
      echo "Usage: $0 [--help] [--snap] [--local]"
      echo ""
      echo "Run demo"
      echo ""
      echo "Options:"
      echo "  -h, --help  show this help message and exit"
      echo "  --snap      Use Snap Firefox"
      echo "  --local     use local copy of pheasakhmer.com"
      echo "  --loop      run in a loop"
      exit 0
      ;;
    --snap) ARGS+=(--snap) ;;
    --local)
      ARGS+=(--local)
      ;;
    --loop)
      ARGS+=(--loop)
      ;;
    *)
      ARGS+=("$1")
      ;;
  esac
  shift
done

# Start webserver for demo
echo "Starting webserver for demo..."
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
python3 -m http.server --bind 127.0.0.1 8050 &
jobs

# Start demo
echo "Starting demo..."
./demo/demo.py "${ARGS[@]}"
