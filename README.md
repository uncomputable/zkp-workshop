# Zero-Knowledge Proof Workshop

Everyone talks about zero-knowledge proofs (ZKP), but who understands them? How can a proof consist of bytes, information, without leaking any knowledge? Why should I trust such a proof?

## What this is

This is a workshop where we go over the fundamentals and build small ZKP systems in Python. There will a hint of math, but I made a point of explaining the background in everyday language and as simple as I can. There is also code for everything we do here.

## What this _isn't_

We will not learn how to build the latest and shiniest crypto. We will not build SNARKs, STARKs or validity rollups. You will not be able to use the code in security-critical areas (we intentionally use insecure parameters to facilitate the learning process).

## Rationale

To build intuition, we must start small and work our way up. This stuff is hard, but there is a method to the madness. My goal is to make ZKP seem less like magic and more like trustworthy math. Once there is understanding, you can take what you learned here and apply it to real problems.
  
## Building

We have come a long way since this workshop used sagemath (1 GB). The new dependencies should not take more than 50 MB :)

### Using nix

Use the provided nix shell to set up the runtime environment.

```
nix-shell
```

### Using pip and package manager

Create a virtual environment and use pip to install the dependencies.

```
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Running

Run jupyter on the command line which will open a browser window. Then select a chapter to read.

```
jupyter notebook
```

## Structure

There are many ways through this workshop.

Look at what interests you, what is new to you, and skip the rest.

Chapters 01 to 09 are foundations of elliptic curves and interactive proof systems. We also cover what zero-knowledge and other terms mean. This is a good place to start.

Chapters 10 to 19 are about how ZKP can be applied to graph problems. These problems are pretty simple compared to other applications.

## Extras

### Hardness of discrete logarithm

See how the curve points jump in 2D space as you iterate through the curve.

```
python3 hardness_dlog.py
```

### Generate critical chi-square values

Generate critical chi-square values for a range of degrees of freedom and a given significance level.

Edit the script to change settings.

Use this to update the constant `CRITICAL_CHI_SQUARE_VALUES` in stats.py.

```
python3 generate-chi-square.py
```

The script requires scipy, which can be installed via nix-shell

```
nix-shell --arg withScipy true
```

or via pip

```
pip install scipy
```

### Generate EC lookup tables

Generate the lookup tables we use to speed up EC operations.

```
python3 ec/generate-lookup-tables.py
```

### Generate curves

Generate parameters of elliptic curves that are similar to secp256k1.

Edit the script to change settings.

```
sage ec/generate-curve.sage
```

This script requires sage (oh no), but you almost never want to run it anyway.

You can install sage easily via nix-shell.

```
nix-shell -p sage
```

If you use pip and the package manager, I guess you can use the [official instructions](https://doc.sagemath.org/html/en/installation/index.html). Good luck :)

## Further reading

- [Number theory explained from first principles](https://explained-from-first-principles.com/number-theory/)
- [Tackling bulletproofs](https://github.com/uncomputable/tackling-bulletproofs)
- [From zero (knowledge) to bulletproofs](https://github.com/AdamISZ/from0k2bp)
- [Lecture on graph problems](https://resources.mpi-inf.mpg.de/departments/d1/teaching/ss13/gitcs/lecture9.pdf)
