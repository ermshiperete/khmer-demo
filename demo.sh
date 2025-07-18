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
      trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
      (
        cd pheasakhmer.com
        python3 -m http.server &
        jobs
      )
      jobs
      ARGS+=(--url http://localhost:8000)
      ;;
    *)
      ARGS+=("$1")
      ;;
  esac
  shift
done

./demo/demo.py "${ARGS[@]}"
