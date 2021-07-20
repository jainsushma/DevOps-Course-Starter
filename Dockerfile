FROM alpine:3.14

RUN echo "--- Installing Poetry ---"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN echo "--- Installing dependencies ---"
RUN poetry install

COPY . .

ENTRYPOINT poetry run flask run --h 127.0.0.0 --p 5000

EXPOSE 5000