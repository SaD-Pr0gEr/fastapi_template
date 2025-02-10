# Installation

## Cloning project

### SSH
```shell
git clone git@github.com:SaD-Pr0gEr/fastapi_template.git
```

### HTTPS
```shell
git clone https://github.com/SaD-Pr0gEr/fastapi_template.git
```

## Set project name
* Go to `pyproject.toml` and set project `name` to your project name


## Installing dependencies
```shell
poetry install
poetry shell
```

## Setting up environment vars
* Rename `example.envs` to `.envs`
* Remove `example` from every file name in `example.envs` (They should look like this `.envs/.env` etc.)
* Rename all example values to actual values and put other values(add these values to config class)

## Setting up config
* Rename `example.config.toml` to `config.toml`
* Rename all example values to actual values

## Alembic

* App models put in app model file, and import this file to alembic's 
`env.py` file(before BASE)
* All models must inherit from base Model class in `db/models/base/Model`
* Apply migrates with command `alembic upgrade head`

## Testings DB connection
```shell
python manage.py db test-connection
```

## Running tests
```shell
pytest
```

## Running project
```shell
python manage.py site run
```

## Pre-commit hooks

* Install pre-commit first time with command `pre-commit install`
* Run pre-commit hooks with command `pre-commit run --all-files`
