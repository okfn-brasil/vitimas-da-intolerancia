# #ViolênciaNãoTemPartido

Hate crimes monitor for political motivated assaults in Brazil.

Requires Python 3.7 and Redis.

1. Install the dependencies with `pip install -r requirements.txt`
2. Copy `.env.sample` as `.env` and setup Redis access and the Google
Spreadsheet IDs (the main one and the `gid` Google uses to identify each sheet)

Spin up the server with:

```sh
$ python run.py
```

Run tests with:

```sh
$ pytest
```
