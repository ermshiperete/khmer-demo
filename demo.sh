#!/bin/bash
set -eu

if [[ ! -d venv ]]; then
  ./install.sh "$@"
fi

. venv/bin/activate

if [[ -f venv/usesnap ]]; then
  SNAP="--snap"
else
  SNAP=""
fi

URL=()
while [[ $# -gt 0 ]]; do
  case $1 in
    --snap) SNAP="--snap" ;;
    --local)
      trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
      (
        cd pheasakhmer.com
        python3 -m http.server &
        jobs
      )
      jobs
      URL=(--url http://localhost:8000)
      ;;
  esac
  shift
done

./demo.py "${URL[@]}" ${SNAP}
