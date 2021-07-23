FROM python:3.9-buster

ENV POETRY_HOME=$HOME/.poetry
ENV PATH=$POETRY_HOME/bin:$PATH
RUN echo "--- Installing Poetry ---"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN echo "--- Installing dependencies ---"

WORKDIR /todo_app
COPY pyproject.toml /todo_app
COPY poetry.lock /todo_app

RUN poetry install

COPY ./todo_app /todo_app/todo_app

ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

EXPOSE 5000