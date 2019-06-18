FROM python:3.7.3-alpine

ENV PYTHONBREAKPOINT=ipdb.set_trace
WORKDIR /code

COPY Pipfile* /code/

RUN apk update && \
    apk add --virtual .build-deps build-base && \
    python -m pip --no-cache install -U pip && \
    python -m pip --no-cache install -U black pipenv && \
    pipenv install --dev && \
    apk --purge del .build-deps && \
    rm -rfv /var/cache/apk/*

COPY .coveragerc .coveragerc
COPY pytest.ini pytest.ini
COPY clear_cache.py clear_cache.py
COPY run.py run.py
COPY victims/ victims/

CMD ["pipenv", "run", "python", "run.py"]
