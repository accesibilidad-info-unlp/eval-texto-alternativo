#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PYTHONPATH="$PROJECT_ROOT" python "$PROJECT_ROOT/scripts/inspect_build_document.py" "$@"