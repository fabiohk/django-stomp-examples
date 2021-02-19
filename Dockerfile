FROM python:3.9-slim

WORKDIR /app

RUN useradd -m appuser \
    && chown appuser /app \
    && pip install pipenv

COPY --chown=appuser Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile \
    && pip uninstall -y pipenv

COPY --chown=appuser . /app/

USER appuser