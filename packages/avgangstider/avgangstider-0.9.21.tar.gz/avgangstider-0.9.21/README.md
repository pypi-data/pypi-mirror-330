!["Build status"](https://github.com/marhoy/flask-entur-avgangstider/actions/workflows/main.yml/badge.svg)
!["Docs build"](https://readthedocs.org/projects/avgangstider/badge/)
!["Latest version"](https://img.shields.io/pypi/v/avgangstider)
![Supported Python versions](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmarhoy%2Favgangstider%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)

# About

Avgangstider gir deg avgangstider og potensielle forsinkelser for all
kollektivtrafikk som `Entur <https://en-tur.no/>`\_ har oversikt over.
Pakka består av to deler:

- Et Python-API for å hente avgangstider og forsinkelser fra Entur.
- En Flask app som viser de neste avgangene fra et stoppested.

# Dokumentasjon

`Dokumentasjon <https://avgangstider.readthedocs.io>`\_ finnes på rtd.io.

# Setting up a development environment

Install [uv](https://docs.astral.sh/uv/). To set up the development environment:

```bash
uv sync --group docs
pre-commit install
```

# Making a new release

- Make sure all tests are ok by running `nox`
- Make sure all pre-commit hooks are ok by running `pre-commit run --all-files`
- Make a pull requst on GitHub
- Merge the PR to the `main` branch
- Create a new tag nameed `vX.Y.Z` where `X.Y.Z` is the new version number
- The new version of the package will be published to PyPi automatically
- Optionally create a new release on GitHub, based on the new tag
