#!/bin/bash
set -e
rm -r dist/* || echo "No distributions to delete"
git diff --exit-code
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*

