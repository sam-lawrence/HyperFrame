#!/bin/sh
set -x -e

# ruff
flake8 .

# mypy
mypy --package hyperframe
