#!/usr/bin/env bash
set -euo pipefail:

# Post-create script for devcontainer
# Installs Nix if needed and enters development environment

echo "=== Hamlib REST Devcontainer Setup ==="

# Check if Nix is installed
if ! command -v nix &> /dev/null; then
    echo "Nix not found, installing..."
    sh <(curl -L https://nixos.org/nix/install) --daemon
    export PATH="/nix/var/nix/profiles/default/bin:$PATH"
else
    echo "Nix already installed"
fi

# Enter development environment
cd /code
nix develop --command true

echo "=== Setup complete ==="
