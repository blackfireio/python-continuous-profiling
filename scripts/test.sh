#!/bin/sh

pip install .

python -m unittest discover -vf
