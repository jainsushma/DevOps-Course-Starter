# DevOps Apprenticeship: Project Exercise

## Setting up shell script for installing/updating dependencies

The project uses poetry and flask dependencies for python. To install required packages, run the following from a shell terminal (e.g. Git Bash on Mac):

$ ./setup.sh
Once the setup script has completed and all packages have been installed, start the Flask app by running:

Note: In order to run this application you will require the appropriate trello information in the .env file. They are as follows

BOARD_ID=<your_board_id>
SECRET_KEY=<your_key>
TOKEN=<your_token>

The board should have three lists added:
"To Do"
"Doing"
"Done"

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
Tests are added for Unit, Integration, Selenium Tests
To run the tests using Poetry and Pytest, stop the app running above and run the command below
```bash
$ poetry run pytest
```
