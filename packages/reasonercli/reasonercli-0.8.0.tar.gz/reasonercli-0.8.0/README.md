
# Reasoner CLI

## Local development

To run locally:
```
uv run python -m src.reasoner.cli upload --path=/path/to/docs
```

## Building for pip
```
uv pip sync pyproject.toml
uv run python -m build
uv run pip install --editable .

# this will install into a temporary location e.g. /Users/username/.pyenv/versions/3.12.7/bin/reasoner
```

## Publishing to pypi
```
python3 -m build

# publish onto pypi
python3 -m twine upload dist/*

# publish onto testpypi
python3 -m twine upload --repository testpypi dist/*

# to install via testpypi
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple reasonercli
```

## Building standalone executable
```
uv pip sync pyproject.toml
uv run pyinstaller --clean --onefile --name reasoner entry.py

cd dist
./reasoner
```

## Testing with older versions of python
```
pipenv --python 3.8 shell
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple reasonercli
reasonercli auth
```

## Automated Testing

### Unit Tests
To run the unit tests locally, run the following command 
```python
pytest
```

You can also run the unit tests in docker container, which emulates what happens when you push a branch
```bash
./scripts/build_test_image.sh
./scripts/run_test_suite.sh
```

### Smoke Tests
Smoke tests take a long time to run, so it's recommended to run them when you make major changes and when you are cutting a new version of the SDK.

To add your version new version to the smoke test rotation, built a wheel following the the instructions above and add it to `tests/integration/sdk_versions`.

Then run the following commands to create a smoketest docker container and run the smoke tests. Warning: smoke tests can take longer than 10 minutes to run!

You will need to point to a specific environment determined by the environment variables you set when running the scripts

```bash
./scripts/build_smoketest_image.sh

REASONER_API_KEY=<your-api-key> REASONER_BASE_URL=<api-environment-url> ./scripts/run_smoke_test_suite.sh
```


