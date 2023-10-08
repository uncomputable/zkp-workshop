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
      makePythonShell = deps: pkgs.mkShell {
        packages = [
          (python.withPackages (ps: deps))
        ];
      };
      makeSageShell = deps: pkgs.mkShell {
        packages = pkgs.lib.optionals (!pkgs.stdenv.isDarwin) [
          pkgs.sage
        ];
      };
    in
    {
      devShells = {
        default = makePythonShell coreDeps;
        scipy = makePythonShell scipyDeps;
        sage = makeSageShell [];
      };
    }
  );
}
