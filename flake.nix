{
  description = "Hamlib REST API Server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "aarch64-linux" "x86_64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems f;

      makePackage = system:
        let
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };

          python313 = pkgs.python313;

          hamlib462 = pkgs.stdenv.mkDerivation {
            name = "hamlib-4.6.2";
            src = pkgs.fetchurl {
              url = "https://github.com/hamlib/hamlib/archive/refs/tags/4.6.2.tar.gz";
              sha256 = "sha256-s7Wp6HyjprXuJZmq9I0lpuVWbT6Ov6iyd6ekZ8EKe0g=";
            };
            buildInputs = [
              pkgs.autoconf
              pkgs.automake
              pkgs.libtool
              pkgs.pkg-config
              pkgs.python3
            ];
            configurePhase = ''
              autoreconf -fi
              ./configure --prefix=$out
            '';
            buildPhase = "make";
            installPhase = "make install";
          };

          hamlibPy = pkgs.runCommandLocal "python3-hamlib" {
            buildInputs = [ pkgs.dpkg pkgs.curl ];
          } ''
            ${pkgs.curl}/bin/curl -sL -o hamlib.deb "http://ftp.us.debian.org/debian/pool/main/h/hamlib/python3-hamlib_4.6.2-1+b1_arm64.deb"
            
            ${pkgs.dpkg}/bin/dpkg-deb -x hamlib.deb $out
            
            mkdir -p $out/lib/python3/dist-packages
            mv $out/usr/lib/python3/dist-packages/* $out/lib/python3/dist-packages/
            rm -rf $out/usr
          '';

          pythonEnv = python313.withPackages (pypkgs: [
            pypkgs.fastapi
            pypkgs.uvicorn
            pypkgs.pydantic
            pypkgs.httpx
            pypkgs.pytest
            pypkgs.pyserial
          ]);

          runtimeDeps = with pkgs; [
            hamlib462
          ];

          appImage = pkgs.dockerTools.buildImage {
            name = "hamlib-rest";
            tag = "latest";

            copyToRoot = pkgs.lib.concatLists [
              runtimeDeps
              [ pythonEnv ]
            ];

            config = {
              workingDir = "/code";
              exposedPorts = [ "8080" ];
              cmd = [
                "${pythonEnv}/bin/uvicorn"
                "--host" "0.0.0.0"
                "--port" "8080"
                "main:app"
              ];
            };
          };

          testImage = pkgs.dockerTools.buildImage {
            name = "hamlib-rest-test";
            tag = "latest";

            copyToRoot = pkgs.lib.concatLists [
              appImage.copyToRoot
              [ (python313.withPackages (pypkgs: [ pypkgs.httpx pypkgs.pytest ])) ]
            ];

            config = {
              cmd = [ "pytest" ];
            };
          };

          devShell = pkgs.mkShell {
            name = "hamlib-rest-dev";
            buildInputs = with pkgs; [
              pythonEnv
              bash
              curl
              jq
              hamlib462
            ];
            shellHook = ''
              export PYTHONPATH="${hamlibPy}/lib/python3/dist-packages:$PYTHONPATH"
              
              export LD_LIBRARY_PATH="${hamlib462}/lib:$LD_LIBRARY_PATH"
              
              echo "Entering hamlib-rest development environment"
              echo "Run 'uvicorn main:app --host 0.0.0.0 --port 8080' to start the server"
            '';
          };

        in {
          default = appImage;
          test = testImage;
          devShell = devShell;
        };

    in {
      devShells = forAllSystems (system: { default = (makePackage system).devShell; });

      packages = forAllSystems (system: (makePackage system));

      checks = forAllSystems (system: { test = (makePackage system).test; });
    };
}
