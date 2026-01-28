# Contributing

Thanks for contributing to MaxFlexSim!

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

ruff check .
mypy src/maxflexsim
pytest
```

## Pull requests

Please include tests for new functionality and update documentation where relevant.
