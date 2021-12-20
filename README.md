# DevOps Apprenticeship: Project Exercise

## Setting up shell script for installing/updating dependencies

The project uses poetry and flask dependencies for python. To install required packages, run the following from a shell terminal (e.g. Git Bash on Mac):

```bash
$ ./setup.sh
```

Note: In order to run this application you will require the appropriate trello information in the .env file. They are as follows

```bash
BOARD_ID=<your_board_id>
SECRET_KEY=<your_key>
TOKEN=<your_token>
```

The board should have three lists added:
```bash
"To Do"
"Doing"
"Done"
```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests
Tests are added for Unit, Integration, Selenium Tests.

To run the tests using Poetry and Pytest, stop the app running above and run the command below
```bash
$ poetry run pytest
```

## Running the application using docker
Use following commands to run docker image todo-app

## Running the application in multi-stage docker file in production
```bash
Make sure gunicorn dependency is already added in pyproject.toml
docker build --target production --tag todo-app:prod .

Pass environment variables as a file, publish the application on port 5000 and listen on port 5000
docker run --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/todo-app todo-app:prod
```

## Running the application in multi-stage docker file in development
```bash
docker build --target development --tag todo-app:dev .

Pass environment variables as a file, publish the application on port 5001 and listen on port 5001
docker run --env-file .env -p 5001:5001 --mount type=bind,source="$(pwd)"/todo_app,target=/todo-app todo-app:prod
```

## Running the tests in multi-stage docker file in test
```bash
docker build --target test --tag todo-app:test .

Run Unit and integration tests as below
docker run todo-app:test tests

Pass environment variables as a file and run Selenium e2e tests as below
docker run --env-file .env todo-app:test tests_e2e
```

## Running the application with docker-compose
```bash
docker compose up --build
```
## Running the application with docker-compose in development/production
```bash
docker compose up todo_app_dev --build

docker compose up todo_app_prod --build
```
## CI/CD Using Github Actions & Heroku
```bash
Github Actions will run builds on branches after every push command. It will run the automated tests that are configured and if they pass, will deploy a Heroku container using the pushed branch on this repository.

## Setup Github Actions
1. Create  a .github folder at the top of your project
2. Inside there, create a workflows folder
3. Create a .yml file with basic commands
4. Go to the repository's settings page and then select the Secrets tab to set 'Environment Variables' add each of the required ENV variables - DOCKER_PASSWORD (insert your Docker account password) - SECRET_APIKEY (Trello) - SECRET_APITOKEN (Trello) - SECRET_KEY - BOARD_NAME (Trello)
5. Complete Heroku setup below
6. Add ENV to Github - HEROKU_API_KEY = Paste API Key from step 5 below or run following commands
 - heroku login
 - heroku container:login
 - heroku authorizations:create
## Setup Heroku
1. Login (or create an account) to Heroku
2. Create a new app e.g. 'heroku-app-devops'
3. Click the user icon in top right corner and select 'Account settings'
4. Scroll down to 'API Key' and generate a key if no key exists
5. Select 'Reveal' and copy the key to clip-board
6. Complete step 6 above
7. In Heroku, click 'Heroku' at top of web page and select the new app
8. In Settings, 'Config Vars', click 'Reveal Config Vars' and add the ENV Vars: - BOARD_ID, SECRET & the TOKEN for your Trello account. These values would be available in your local .env file
```

## Switching from TRELLO board to MONGO db
```bash
We are now using MongoDB in place of Trello. In order to configure this application to work with MongoDB you will need to update the following variables 

1. With the .env file:

DBNAME=[Your DB Name Here]
CLIENT=[Your Connection String Here] 

2. Add CLIENT secret to Github
3. Add CLIENT and some new DB eg 'PRODDB' as DBNAME as Heroku config variables
```