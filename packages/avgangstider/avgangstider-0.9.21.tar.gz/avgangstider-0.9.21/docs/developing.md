# Developing

If you haven't done so already, install
[uv](https://docs.astral.sh/uv/getting-started/installation/).

## Setting up your development environment

```bash
# Set up development environment
uv sync

# Start a debugging server
uv run python src/avgangstider/flask_app.py
```

## Run all tests and code checks

After having made changes: Make sure all tests are still OK, test coverage is still 100%
and that linters and formatters are happy:

```bash
uv run pre-commit run --all-files
uv run pytest
```

## Build documentation

```bash
uv sync --group docs
uv run mkdocs serve
```

## Build new docker image

If you want to build your own docker image:

```bash
docker build -t avgangstider .
docker run -d -p 5000:5000 avgangstider
```
