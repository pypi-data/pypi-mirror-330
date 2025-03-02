# FileLean (Demo)

[English](README.md) | [简体中文](README-zh.md)

A lightweight Python package for interacting with Lean prover. This is a demonstration package showing how to interact with Lean 4 through files.

## Installation

```bash
pip install filelean
```

## Basic Usage

### CLI Commands

```bash
# Install a specific Mathlib version
filelean mathlib install v4.15.0

# List installed versions
filelean mathlib list
```

### Simple Example
```python
from filelean import FileLean

# Initialize with the default Lean Environment
filelean = FileLean()

# Basic theorem proving
statement = 'example :1=1'
state = filelean.init_state(statement)
assert filelean.run_tac(state, "apply?").is_solved
```

### Example with Mathlib

```python
from filelean import FileLean, read_mathlib_cache

# Proving a mathematical theorem
statement = """theorem mathd_algebra_296 : 
    abs ((3491 - 60) * (3491 + 60) - 3491 ^ 2 : ℤ) = 3600"""

# Initialize with imports
state = filelean.init_state(statement, header='import Mathlib')

# Apply tactics sequentially
tactics = [
    'rw [abs_of_nonpos]',
    'norm_num',
    'norm_num'
]

# Track proof states
states = [state]
for tactic in tactics:
    state = filelean.run_tac(state, tactic)
    print(state)  # Print current goals
    states.append(state)
assert states[-1].is_solved
```

### Experimental: Sketch Proof

An experimental feature to work with proof sketches containing `sorry`:

```python
# Example of a proof sketch with holes
sketch_thm = """theorem demo (P Q R : Prop) : (P → Q) → (Q → R) → (P → R) := by
  intro h1 h2 p
  have q : Q := by
    apply h1
    sorry
  apply h2
  sorry"""

# Extract states from the sketch
states = filelean.states_from_sketch(sketch_thm)
assert len(states) == 2  # Two sorry holes to fill
```

TODO: Ability to continue proving from sketched states.

## Features


- File-based interaction with Lean 4 for theorem proving
- Consistent with compilation results, completely avoiding fake proofs  
- Extensible to any version
- Support for proof sketches (experimental)

## Note

This is a demo package and it is currently under development.

