FROM python:3.7.3-slim

ENV PYTHONBREAKPOINT=ipdb.set_trace
ENV FLASK_ENV development
ENV FLASK_APP victims/__init__.py
ENV FLASK_SKIP_DOTENV 1

WORKDIR /code
COPY Pipfile* /code/

RUN python -m pip --no-cache install -U pip && \
    python -m pip --no-cache install -U black pipenv && \
    pipenv install --dev

COPY .coveragerc .coveragerc
COPY pytest.ini pytest.ini
COPY victims/ victims/

CMD ["pipenv", "run", "flask", "run"]
