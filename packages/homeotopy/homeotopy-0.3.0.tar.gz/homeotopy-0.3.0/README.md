# Homotopy

[![build](https://github.com/erikbrinkman/homeotopy/actions/workflows/python-package.yml/badge.svg)](https://github.com/erikbrinkman/homeotopy/actions/workflows/python-package.yml)
[![pypi](https://img.shields.io/pypi/v/homeotopy)](https://pypi.org/project/homeotopy/)
[![docs](https://img.shields.io/badge/api-docs-blue)](https://erikbrinkman.github.io/homeotopy)

A python library for computing homeomorphisms between some common continuous
spaces.

## Installation

```sh
pip install homeotopy
```

## Usage

```py
import homeotopy

points = ...
# create a mapping from the simplex to the surface of the sphere
mapping = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.sphere())
sphere_points = mapping(points)

rev_mapping = reversed(mapping)
duplicate_points = rev_mapping(sphere_points)
```

## Development

```sh
uv run pytest --cov
uv run ruff format homeotopy/*.py tests/*.py
uv run ruff check homeotopy/*.py tests/*.py
uv run mypy homeotopy
```
