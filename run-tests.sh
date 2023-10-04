#!/bin/sh
set -x -e

# ruff
ruff check .

# black
black --check --diff .

# mypy
mypy --package hyperframe

# Run tests
pytest tests
