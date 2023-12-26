#!/bin/bash
set -e

if [ "$1" == "--change" ]; then
    black_args="--skip-string-normalization"
    isort_args="--profile black"
else
    black_args="--check --diff --skip-string-normalization"
    isort_args="--check-only --diff --profile black"
fi

flake8_args="--exclude=migrations,__init__.py,apps.py,media,logs --config pyproject.toml"


echo "Black checking"
black $black_args src
echo '-----------------------------------'

echo "isort checking"
isort $isort_args src --skip migrations --skip media --skip logs
echo '-----------------------------------'

echo "flake8 checking"
flake8 $flake8_args src
echo '-----------------------------------'

echo "mypy checking"
cd src; mypy --config-file ../pyproject.toml . ; cd ..;
echo '-----------------------------------'