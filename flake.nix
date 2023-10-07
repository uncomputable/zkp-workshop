{
  description = "ZKP Workshop";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
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
      packages = [
        pkgs.sage
      ];
    };
  in
  {
    devShells.x86_64-linux = {
      default = makePythonShell coreDeps;
      scipy = makePythonShell scipyDeps;
      sage = makeSageShell [];
    };
  };
}
