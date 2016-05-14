#!/bin/sh
find . -type f -name "*.pyc" -exec rm -f {} \;
find . -type d -name "__pycache__" -exec rm -rf {} \;
