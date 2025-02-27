# Bigdata Client

[![CI/CD Pipeline](https://github.com/RavenPack/bigdata-client/actions/workflows/cicd.yml/badge.svg)](https://github.com/RavenPack/bigdata-client/actions/workflows/cicd.yml)

A Python client for accessing Bigdata API (https://bigdata.com).
[Documentation (latest)](https://bigdata-python-client.readthedocs-hosted.com/en/latest/index.html)

## Troubleshooting
#### Docs: Enchant lib issue on Apple Silicon
Tasks `poetry run task docs` or `poetry run task check-docs` produces an issue:
```
Extension error:
Could not import extension sphinxcontrib.spelling (exception: The 'enchant' C library was not found and maybe needs to be installed.
```
In this situation it is necessary to set environment variable `PYENCHANT_LIBRARY_PATH=` with the pat to library
```bash
export PYENCHANT_LIBRARY_PATH=$(brew --prefix enchant)/lib/libenchant-2.dylib
poetry run task docs
```