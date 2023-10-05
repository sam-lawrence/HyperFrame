#!/bin/sh
set -x -e

# ruff
ruff check .

# black
black --check --diff .

# mypy
mypy

# Run tests
pytest
