#!/usr/bin/env bash
set -e

pip install --upgrade pip setuptools wheel
pip install --only-binary=:all: -r requirements.txt
