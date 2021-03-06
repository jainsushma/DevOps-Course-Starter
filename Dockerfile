FROM python:3.9-buster as base
# Perform common operations, dependency installation etc...

ENV POETRY_HOME=$HOME/.poetry
ENV PATH=$POETRY_HOME/bin:$PATH
RUN echo "--- Installing Poetry ---"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN echo "--- Installing dependencies ---"

WORKDIR /todo_app
COPY pyproject.toml poetry.lock /todo_app/

#RUN poetry install
RUN poetry config virtualenvs.create false --local && poetry install

COPY ./todo_app /todo_app/todo_app

FROM base as production 
# Configure for production
ENV FLASK_ENV=production
ENV PORT=5000
COPY ./entrypoint.sh /todo_app/
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh

FROM base as development 
# Configure for local development
ENV FLASK_ENV=development
ENTRYPOINT [ "poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5001"]
EXPOSE 5001

FROM base as test 
# Configure for local test environment
COPY ./tests /todo_app/tests
COPY ./tests_e2e /todo_app/tests_e2e
COPY .env.test /todo_app/

# Install poetry dependencies 
RUN poetry install

# Flask Server env
ENV FLASK_APP =todo_app/app
ENV FLASK_ENV=development

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip

# Install Firefox
RUN apt-get install -y firefox-esr
RUN poetry install
ENV FLASK_DEBUG=0
ENV GECKODRIVER_VERSION 0.30.0
ENV MOZ_HEADLESS=1
RUN wget --no-verbose -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz  \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf geckodriver.tar.gz \
  && rm geckodriver.tar.gz \
  && chmod 755 /opt/geckodriver \
  && ln -fs /opt/geckodriver /usr/bin/geckodriver

ENTRYPOINT [ "poetry", "run", "pytest"]
