with (import <nixpkgs> {});
let
  my-python-packages = python-packages: with python-packages; [
    matplotlib
    numpy
    notebook
    networkx
    ipywidgets
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in
  mkShell {
    buildInputs = [
      my-python
    ];
  }
