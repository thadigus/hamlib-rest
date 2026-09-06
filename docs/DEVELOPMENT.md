# Hamlib REST - Development Setup

This document describes the development environment setup using Nix and devcontainer.

## Quick Start

### Option 1: Using Nix directly (recommended for developers)

```bash
nix develop
# Now in the dev shell
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Option 2: Using devcontainer CLI (works on any machine)

```bash
# Requires Docker and devcontainer CLI
devcontainer up --workspace-folder .
```

The devcontainer will:
1. Install Nix inside the container
2. Run `nix develop` to set up the Python environment
3. Make VS Code extensions available

### Option 3: Traditional Docker

```bash
# Build the runtime image
docker build --target runtime -t hamlib-rest:latest .

# Run the server
docker run -p 8080:8080 hamlib-rest:latest
```

## Project Structure

```
.
├── flake.nix          # Nix flake defining the development and runtime environments
├── nix/               # Nix-specific files (auto-generated from flake)
│   └── default.nix    # Backward compatibility wrapper
├── devcontainer/      # Devcontainer configuration
│   ├── Dockerfile     # Base image that installs Nix
│   └── nix-dev.sh     # Post-create script
└── .devcontainer/
    └── devcontainer.json
```

## Running the Server

Once in the development environment:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

Access the API docs at: http://localhost:8080/docs

## Building the Nix-based Runtime Container

```bash
# Build the app image
nix build .#default

# The result is at ./result/image.tar.gz
```

## Testing

```bash
# Run tests in the dev shell
pytest

# Or build and run the test image
nix build .#test
```

## Troubleshooting

### Nix installation fails in devcontainer

The devcontainer Dockerfile installs Nix during container creation. If this fails:
1. Check Docker has sufficient privileges
2. Verify internet connectivity
3. Try rebuilding: `devcontainer rebuild`

### Package not found error

The Nix flake pins `nixos-unstable`. To update packages:

```bash
nix flake update
```

## Migration Notes

This setup replaces the previous pure Docker approach with:

1. **Development**: Nix for reproducible Python environment
2. **Runtime**: Nix-built container (still a standard Docker image)
3. **Devcontainer**: Works with or without Nix on host machine

The existing `Dockerfile` still works for non-Nix users who prefer traditional Docker workflows.
