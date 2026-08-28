Hashtag Brews
=============

[![GitHub Actions](https://github.com/talaniz/hashtagbrews/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/talaniz/hashtagbrews/actions/workflows/tests.yml)

A Django based site that will contain the following applications:
* An open source beer database containing a catalogue of hops, grains and yeasts
* A homebrew planner and timer to track the stages of a brewing process
* A vendor site where homebrew supply vendors can track their inventories
* A homebrew recipe creator that will allow brewers to create a recipe with the options to use ingredients based on a vendor's inventory and choose a pre-planned recipe from a vendor

## Local Test Setup

The legacy Django 2.0 stack runs locally with Python 3.9 and requires
PostgreSQL plus Elasticsearch. Docker Desktop is the supported local service
runtime.

```sh
uv venv --python 3.9 .venv
uv pip install --python .venv/bin/python --requirement requirements.txt
docker compose -f docker-compose.test.yml up -d
```

Run the deterministic application suite with isolated local test credentials:

```sh
DJANGO_SETTINGS_MODULE=hashtagbrews.settings.test \
SECRET_KEY=local-test-secret-key \
DB_PASSWORD=hashtagbrews-test \
.venv/bin/python manage.py test homebrewdatabase.tests accounts.tests --noinput
```

The legacy Selenium functional suite additionally requires Firefox and
`geckodriver` on `PATH`:

```sh
DJANGO_SETTINGS_MODULE=hashtagbrews.settings.test \
SECRET_KEY=local-test-secret-key \
DB_PASSWORD=hashtagbrews-test \
.venv/bin/python manage.py test functional_tests --noinput
```

Stop disposable test services when finished:

```sh
docker compose -f docker-compose.test.yml down
```

## Planning

1. Homebrew Materials Database

    * Finish functional test to add hops (includes unit tests to save to db, etc.) - Completed
    * Refactor to use templating - Completed
    * Add grains and yeasts code - Completed
    * Test Suites: tests for all 3 models - Completed
    * Add error handling - Completed
    * Move to class based views - Completed
    * Add update and delete views - Completed
    * Add user authentication - Completed
    * Add user registration - Completed

2. Homebrew Planner and Timer
    * Needs planning

3. Vendor/Inventory Site
    * Needs planning

4. Hombrew Recipe Creator
    * Needs planning

## To Do
* Homebrew database and hops pages need additional formatting
* Sprint planning for homebrew planner, inventory site and homebrew recipe creator
