install:
    pip install -e .

# Build project
build: clean
    python -m build

# Upload to Text PyPI
upload-test: build
    twine upload --repository testpypi dist/*

# Upload to PyPI
upload: build
    twine upload dist/*

# Clean temporary files
clean:
    rm -fr build dist *egg* *cache*

# Open project url at PyPI
open-pypi:
    open https://pypi.org/project/pypas-cli/

# Test project
test:
    pytest -vv

# Test project with coverage
cov:
    pytest --cov src/swiftbarmenu --cov-report=term-missing

# Open IPython
sh:
    ipython
