# prolog-env
[![PyPI version](https://badge.fury.io/py/prolog-env.svg)](https://badge.fury.io/py/prolog-env)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python package providing an environment for AI agents to test their Prolog code.

## Installation

The package depends on SWI-Prolog, to [install SWI-Prolog from PPA](https://www.swi-prolog.org/build/PPA.html):

```bash
sudo apt-add-repository ppa:swi-prolog/stable
sudo apt-get update
sudo apt-get install swi-prolog libpython3-dev
```

Install the package using pip:

```bash
pip install prolog-env
```

## Get started

This guide provides a quick introduction to using the `prolog_env` package. It demonstrates how to create and interact with the `SimpleEvaluator` environment.

```py
from prolog_env import SimpleEvaluator

env = SimpleEvaluator()

code = """
train('Amsterdam', 'Haarlem').
train('Amsterdam', 'Schiphol').
"""

observation, reward, terminated, truncated, info = env.step(code)

print("Observation:")
print(observation)
print("Reward:", reward)

tests = """
:- begin_tests(test).

test(a) :-
        A is 2^3,
        assertion(float(A)),
        assertion(A == 9).

:- end_tests(test).
"""

observation, reward, terminated, truncated, info = env.step(code, tests)

print("Observation:")
print(observation)
print("Reward:", reward)
```