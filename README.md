# #ViolênciaNãoTemPartido

Hate crimes monitor for political motivated assaults in Brazil.

Requires Python 3.7 and Redis.

1. Install the dependencies with `pip install -r requirements.txt`
2. Copy `.env.sample` as `.env` and setup Redis access and the Google
Spreadsheet ID

Spin up the server with:

```sh
$ gunicorn violence:app --worker-class sanic.worker.GunicornWorker
```

Run tests with:

```sh
$ pytest
```
