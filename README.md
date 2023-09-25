# Getting to Know Zero-Knowledge

Everyone talks about zero-knowledge proofs (ZKP), but who understands them? How can a proof consist of bytes without leaking any knowledge? Why should I trust such a proof? 🤔

## What this is

This is a workshop about ZKP written in Python. We use Jupyter as our interactive learning environment. Each notebook is a chapter. The chapters cover fundamentals, applications and much more. Explore and have fun 😜

## What this _isn't_

We will not cover the latest and shiniest crypto. We will not build SNARKs, STARKs or validity rollups. The code you will see will not live up to the highest security standards _(we use insecure parameters and take shortcuts for easier learning)_ 🕵️

## Rationale

Master the basics first, then move to the advanced stuff; that is my philosophy. Let's build an intuition for how ZKP works. We start small and work our way up. Things become simpler when we break them down into their constituent parts. Divide and conquer. Once there is understanding, we can take what we learned here and apply it to real problems 💪

## Run the workshop

Run the workshop online (binder) or locally (nix or pip).

We have come a long way since this workshop Sage (1 GB). The new dependencies take up less than 50 MB 🍃

See below how to set up the workshop.

Then select a chapter to read 📖

### Use binder

Click the binder badge and wait for the workshop to be built on the server.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uncomputable/zkp-workshop/master)

### Use nix

Use the provided nix shell to set up the runtime environment.

```
nix-shell
```

Run Jupyter on the command line.

```
jupyter notebook
```

### Use pip

Create a virtual environment and use pip to install the dependencies.

```
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Run Jupyter on the command line.

```
jupyter notebook
```

## Read the chapters

Some chapters depend on lessons from other chapters.

Start with chapters that depend on nothing else and work your way down the dependency tree, towards more advanced chapters.

Skip / skim lessons you already know. Look at what interests you and ignore everything else. Have fun 🤓

![Chapter dependency tree](chapter_dependencies.svg)

## Explore extra content

### See why the discrete logarithm is hard

See how the curve points jump in 2D space as you iterate through the curve.

This is explained in more detail in the chapter on elliptic curves 🌀

```
python3 hardness_dlog.py
```

### Play Sudoku

Play the side of Victor in an interactive proof of knowledge of a Sudoku solution. Accept or reject. Peggy might be lying! 🧩

```
python3 play_sudoku.py
```

### Customize the workshop

Look at [the documentation](https://github.com/uncomputable/zkp-workshop/blob/master/customization.md) for how to further customize the workshop 🎨

## Improve the workshop

If you see errors or room for improvement, then feel free to open a Github issue.

Pull requests are also welcome.

Let's turn this workshop into the best it can be 🚀

## Continue your journey

There is a lot more to learn about ZKP.

Check out these external resources. Happy learning 🧠

- [Number theory explained from first principles](https://explained-from-first-principles.com/number-theory/)
- [Tackling bulletproofs](https://github.com/uncomputable/tackling-bulletproofs)
- [ZKP explained in 3 examples](https://www.circularise.com/blogs/zero-knowledge-proofs-explained-in-3-examples)
- [Computer scientist explains ZKP in 5 levels of difficulty](https://www.youtube.com/watch?v=fOGdb1CTu5c)
- [How to explain ZKP to your children](https://pages.cs.wisc.edu/~mkowalcz/628.pdf)
