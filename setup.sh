#!/usr/bin/env bash
#
# One-time setup for doing working-in-python homework in a Codespace (cs50.dev or
# similar). Creates a wip/ folder with its own Python virtual environment, kept
# separate from anything else in the codespace so VS Code can auto-detect it as a
# kernel and so it never interferes with submit50 (a venv sitting in the same
# folder you submit50 from can trip its file-count safety check).
#
# Usage:
#   curl -L -o setup.sh https://raw.githubusercontent.com/porttack/working-in-python/v3/setup.sh
#   bash setup.sh
#
# Safe to run again later -- it won't recreate an already-existing venv, and
# reinstalling the same packages is a no-op.

set -euo pipefail

# Capture this script's own path before cd'ing anywhere, so it can be copied into
# wip/ at the end -- kept there so it's easy to find and re-run later, and so
# what this setup actually does stays documented right alongside the venv itself.
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"

if [ "$(basename "$(pwd)")" = "wip" ]; then
  echo "Already inside wip/, using this directory."
else
  echo "Setting up wip/ ..."
  mkdir -p wip
  cd wip
fi

if [ -d .venv ]; then
  echo ".venv already exists -- skipping creation."
else
  echo "Creating .venv ..."
  python3 -m venv .venv
fi

echo "Installing packages into .venv (ipykernel, matplotlib, pyyaml, notebook) ..."
.venv/bin/pip install ipykernel matplotlib pyyaml notebook

if [ "$SCRIPT_PATH" != "$(pwd)/setup.sh" ]; then
  cp -- "$SCRIPT_PATH" ./setup.sh
fi

echo
echo "Done. Your environment is in wip/.venv"
echo "Next: open a chapter notebook (in this wip/ folder) and select wip/.venv as the kernel."
