{
  description = "ZKP Workshop";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils
  }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;
      coreDeps = with python.pkgs; [
        matplotlib
        numpy
        notebook
        networkx
        ipywidgets
        pygame
      ];
      scipyDeps = with python.pkgs; coreDeps ++ [
        scipy
      ];
      corePython = python.withPackages (_: coreDeps);
      scipyPython = python.withPackages (_: scipyDeps);
    in
    {
      devShells = {
        default = pkgs.mkShell {
          packages = [ corePython ];
        };
        scipy = pkgs.mkShell {
          packages = [ scipyPython ];
        };
        sage = pkgs.mkShell {
          # Sage is not available on macOS
          packages = pkgs.lib.optionals (!pkgs.stdenv.isDarwin) [ pkgs.sage ];
        };
      };
      packages = {
        default = pkgs.writeShellScriptBin "jupyter" ''
          ${corePython}/bin/python -m notebook
        '';
      };
    }
  );
}
