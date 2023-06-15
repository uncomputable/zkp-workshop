# Zero-Knowledge Proof Workshop

Everyone talks about zero-knowledge proofs (ZKP), but who understands them? How can a proof consist of bytes, information, without leaking any knowledge? Why should I trust such a proof? In this workshop we go over the fundamentals and build a small ZKP system in Python. We will cover some math, but no PhD is required 😁 Everything will be explained in code.

We will _not_ learn how to build the latest SNARKs / STARKs or how to do on-chain validity rollups. To build intuition, we must start small and work our way up. This stuff is hard, but there is a method to the madness. My goal is to make ZKP seem less like magic and more like trustworthy math.  
  
## Building

### Using nix

Install nix [via the official instructions](https://nixos.org/download.html).

```
nix-shell
```

### Using pip and package manager

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```
jupyter notebook
```

## Structure

First we go over [elliptic curve basics](https://github.com/uncomputable/zkp-workshop/blob/master/01-elliptic_curves.ipynb).

Second is an [introduction to interactive proofs](https://github.com/uncomputable/zkp-workshop/blob/master/02-interactive_proofs.ipynb).

Finally [we look at Schnorr](https://github.com/uncomputable/zkp-workshop/blob/master/03-schnorr.ipynb) which is a ZKP that exists on Bitcoin today!

So far there are no other chapters, but there are plans for more if there is demand.

## Recommended reading

- [Number theory explained from first principles](https://explained-from-first-principles.com/number-theory/)
- [Tackling bulletproofs](https://github.com/uncomputable/tackling-bulletproofs)
- [From zero (knowledge) to bulletproofs](https://github.com/AdamISZ/from0k2bp)
