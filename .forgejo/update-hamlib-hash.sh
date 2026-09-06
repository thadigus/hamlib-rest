#!/usr/bin/env bash
# Recompute the Hamlib tarball hash in flake.nix after the pinned version changes.
# Run as a Renovate postUpgradeTask; safe to run by hand.
set -euo pipefail

flake="${1:-flake.nix}"
base="https://github.com/hamlib/hamlib/archive/refs/tags"

version=$(sed -n "s|.*hamlib/hamlib/archive/refs/tags/\([^\"]*\)\.tar\.gz.*|\1|p" "$flake" | head -n 1)
if [ -z "$version" ]; then
    echo "no Hamlib tarball pin found in $flake" >&2
    exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
    hex=$(curl -fsSL "$base/$version.tar.gz" | sha256sum | cut -d' ' -f1)
else
    hex=$(curl -fsSL "$base/$version.tar.gz" | shasum -a 256 | cut -d' ' -f1)
fi

sri="sha256-$(printf "$(printf '%s' "$hex" | sed 's/../\\x&/g')" | base64 | tr -d '\n')"

sed -i.bak "/hamlib\\/hamlib\\/archive/,/sha256 = / s|sha256 = \"[^\"]*\";|sha256 = \"$sri\";|" "$flake"
rm -f "$flake.bak"

echo "Hamlib $version -> $sri"
