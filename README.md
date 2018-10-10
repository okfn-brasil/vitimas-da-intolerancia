# #VítimasDaIntolerância

Hate crimes monitor for political motivated assaults in Brazil.

## Install

Requires a Google account, Python 3.7 and Redis.

1. Install the dependencies with `pip install -r requirements.txt`
1. Create a [Google Sheets](https://docs.google.com/spreadsheets/) file
1. Create two spreadsheets (tabs) in this file
1. Use the files from [`tests/fixtures`](victims/tests/fixtures/) to fill in
   these spreadsheets
1. Then copy `.env.sample` as `.env` and setup Redis access and the Google
   Sheets data
    1. The unique ID from the Google Sheet URL is the `SPREADSHEET_ID`
    1. The `gid` URL parameter Google generates when exporting each spreadsheet
       as CSV is the value of `CASES_SPREADSHEET_GID` and
       `STORIES_SPREADSHEET_GID`

## Running the server

Spin up the server with:

```sh
$ python run.py
```

## Tests

Run tests with:

```sh
$ pytest
```
