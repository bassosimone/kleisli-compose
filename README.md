# Introduction to monads

![My iPhone's auto-correct likes to change monadi with monaci](docs/monks.png)

This repository contains an introduction to monads  for an internal seminar
I am going to give at [@fbk-most](https://github.com/fbk-most).

## Slides

See [slides.pdf](slides.pdf) for the slides. The objectives are:

1. to define the monad using the `>=>` Haskell operator;

2. to implement a monadic [result type](https://doc.rust-lang.org/std/result/)
in Python through incremental refactoring.

We use internet measurements as a case study because I previously
implemented monadic composition in such a specific context, so I am
already familiar with the problem space.

## Talk

Please, see [talk.md](talk.md) for the talk script.

## Architecture

The [kleisli_compose](kleisli_compose) package contains the following
files (in order of appearance in the slides):

- [mocks](kleisli_compose/mocks.py): functions mocking network I/O operations;
- [base.py](kleisli_compose/base.py): base implementation;
- [catcher.py](kleisli_compose/catcher.py): improves `base.py` to handle exceptions;
- [bettercatcher.py](kleisli_compose/bettercatcher.py): refactors `catcher.py`;
- [landing.py](kleisli_compose/landing.py): futher refactoring that is nearly monadic;
- [full.py](kleisli_compose/full.py): full monadic implementation.
- [fancy.py](kleisli_compose/fancy.py): extends `full.py` to be really fancy.

The [examples](examples) folder contains the examples mentioned in the
[slides.pdf](slides.pdf) and named in order of appearance.

## Getting Started

If you have already installed [uv](https://astral.sh/uv), run:

```bash
uv venv
source .venv/bin/activate
uv sync --dev
```

Otherwise, make sure you have Python >= 3.12 installed.

## Running examples

To run the first example, execute:

```bash
python examples/000.py
```

You can run subsequent examples by changing the file name.

## License

```
SPDX-License-Identifier: Apache-2.0
```

## Further Readings

[Category Theory for Programmers](https://github.com/hmemcpy/milewski-ctfp-pdf).
