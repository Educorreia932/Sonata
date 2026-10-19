{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      pyproject-nix,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        project = pyproject-nix.lib.project.loadPyproject {
          projectRoot = ./.;
        };

        python = pkgs.python312.override {
          packageOverrides = final: _prev: {
            anyio = _prev.anyio.overridePythonAttrs { doCheck = false; };
            discord-py = final.discordpy;
            lyricsgenius = import ./nix/lyricsgenius.nix {
              inherit (pkgs) lib;
              python3Packages = final;
            };
          };
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            (python.withPackages (
              project.renderers.withPackages {
                inherit python;
                extras = [
                  "dev"
                  "docs"
                ];
              }
            ))
            just
            ruff
            ty
          ];
        };

        packages =
          let
            attrs = project.renderers.buildPythonPackage { inherit python; };
          in
          {
            default = python.pkgs.buildPythonPackage (attrs);
          };
      }
    );
}
