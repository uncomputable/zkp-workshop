{ pkgs ? import <nixpkgs> {}
, withScipy ? false
}:
let
  optional = pkgs.lib.optional;
  my-python-packages = python-packages: with python-packages; [
    matplotlib
    numpy
    notebook
    networkx
    ipywidgets
  ] ++ optional withScipy scipy;
  my-python = pkgs.python3.withPackages my-python-packages;
in
  pkgs.mkShell {
    buildInputs = [
      my-python
    ];
  }
