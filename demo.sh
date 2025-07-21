#!/bin/bash
set -eu

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
      exit 0
      ;;
    --snap) ARGS+=(--snap) ;;
    --local)
      echo "Starting local webserver for pheasakhmer.com..."
      trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
      python3 -m http.server --directory pheasakhmer.com --bind 127.0.0.1 8051 &
      jobs
      ARGS+=(--url http://localhost:8051)
      ;;
    *)
      ARGS+=("$1")
      ;;
  esac
  shift
done

# Start webserver for Keyman presentation
echo "Starting webserver for Keyman presentation..."
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
python3 -m http.server --directory keyman --bind 127.0.0.1 8050 &
jobs

# Start demo
echo "Starting demo..."
./demo/demo.py "${ARGS[@]}"
