#! /usr/bin/env bash
set -u

if ! black -l 120 --check modules/ *.py
then
    black -l 120 --diff modules/ *.py
fi
