# Customization

You can change the parameters used in this workshop and recompute the hardcoded values.

Some of these functions require additional dependencies to work.

## Running with Scipy

Scipy can be installed via nix-shell

```
nix-shell --arg withScipy true
```

or via pip

```
pip install scipy
```

## Generate critical chi-square values (requires Scipy)

The chi-square test uses a significance which is implicitly encoded in the critical chi-square values. The default significance is the usual 5%.

There is one chi-square value for each number of degrees of freedom. We generated values up to a maximum number.

Edit [this script](https://github.com/uncomputable/zkp-workshop/blob/master/generate-chi-square.py) to change these parameters.

Run the script on the command line.

```
python3 generate-chi-square.py
```

It will directly overwrite the Python files inside the repository after asking you for confirmation.

## Generate EC lookup tables

Most elliptic curve operations use static lookup tables. It is much easier to treat curve points as literal integers instead of 2D points with arithmtic properties. The catch is that we need to know the discrete logarithm. It works for us because we use small curves.

In real life, the curves would be too large to make lookups feasible. The lookup table would be larger than the number of atoms in the universe. Keep this in mind.

Run this script to generate the static lookup tables.

This is especially useful after you changed the curve we work on (see below).

```
python3 generate-lookup-tables.py
```

It will directly overwrite the Python files inside the repository after asking you for confirmation.

## Running with Sage

Oh, no. You almost never want to run Sage :O

You can install Sage easily via nix-shell.

```
nix-shell -p sage
```

If you use pip and the package manager, I guess you can use the [official instructions](https://doc.sagemath.org/html/en/installation/index.html). Good luck :)

## Change the curve (requires Sage)

The parameters of the elliptic curve we use are defined in [the core EC implementation](https://github.com/uncomputable/zkp-workshop/blob/master/local/ec/core.py).

This is a small elliptic curve which is similar to [secp256k1](https://en.bitcoin.it/wiki/Secp256k1).

Edit [this script](https://github.com/uncomputable/zkp-workshop/blob/master/generate-curve.sage) to change these parameters.

Run the script on the command line.

```
sage generate-curve.sage
```

It will directly overwrite the Python files inside the repository after asking you for confirmation.

Make sure to update the static lookup tables (see above).
