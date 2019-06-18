[![Travis CI](https://img.shields.io/travis/okfn-brasil/vitimas-da-intolerancia.svg)](https://travis-ci.org/okfn-brasil/vitimas-da-intolerancia)
[![Codecov](https://img.shields.io/codecov/c/github/okfn-brasil/vitimas-da-intolerancia.svg)](https://codecov.io/gh/okfn-brasil/vitimas-da-intolerancia)
[![Code Climate](https://img.shields.io/codeclimate/maintainability/okfn-brasil/vitimas-da-intolerancia.svg)](https://codeclimate.com/github/okfn-brasil/vitimas-da-intolerancia)

# #VítimasDaIntolerância

Hate crimes monitor for political motivated assaults in Brazil.

Requires a Google account, Python 3.7 with [Pipenv](https://pipenv.readthedocs.io/) and Redis.

## Settings

Basic settings are set in  a `.env` file. You can copy `.env.sample` as `.env`
and set it up according to your environment.

The repository initial setup includes a
[sample Google Sheets](https://docs.google.com/spreadsheets/d/1C73e7Lph1fNGontBodEDFZ4oqn3cC2oB_0Av3vRTiRw/edit?usp=sharing)
document with some
data. You can copy this document and create your own. To setup the application
to read a custom spreadsheet:

* The unique ID from the Google Sheet URL is the `SPREADSHEET_ID`
* The `gid` URL parameter Google generates when exporting each spreadsheet as
  CSV is the value of `CASES_SPREADSHEET_GID` and `STORIES_SPREADSHEET_GID`

## Running the server

Install the dependencies with `pipenv install` and spin up the server with:

```sh
$ python run.py
```

If you wanna clear the cache:

```sh
$ python clear_cache.py
```

## Contributing

Make yourself at home, write tests and format code with
[Black](https://github.com/ambv/black):

```sh
$ black .
```

## Tests

Run tests with:

```sh
$ pytest
$ black . --check
```
