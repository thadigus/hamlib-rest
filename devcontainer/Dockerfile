FROM ubuntu:24.04

# Install prerequisites for Nix installation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        xz-utils \
        squashfuse \
        fuse \
    && rm -rf /var/lib/apt/lists/*

# Install Nix (multi-user daemon mode)
RUN sh <(curl -L https://nixos.org/nix/install) --daemon

# Source Nix environment
ENV PATH=/nix/var/nix/profiles/default/bin:/nix/var/nix/profiles/default/sbin:$PATH

# Create workspace
WORKDIR /code

# Copy project files
COPY . .

# Expose the app port
EXPOSE 8080
