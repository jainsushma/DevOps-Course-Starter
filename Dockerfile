FROM python:3.9-buster as base
# Perform common operations, dependency installation etc...

ENV POETRY_HOME=$HOME/.poetry
ENV PATH=$POETRY_HOME/bin:$PATH
RUN echo "--- Installing Poetry ---"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN echo "--- Installing dependencies ---"

WORKDIR /todo_app
COPY pyproject.toml poetry.lock /todo_app/

RUN poetry install

COPY ./todo_app /todo_app/todo_app

FROM base as production 
# Configure for production
#Implement as CMD, Gunicorn, is it necessary to have brackets in ENTRYPOINT, how to differentiate between ENTRYPOINT & CMD
ENTRYPOINT [ "poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EXPOSE 5000

FROM base as development 
# Configure for local development
ENTRYPOINT [ "poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000

FROM base as test
# Configure for test
ENTRYPOINT poetry run pytest