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

2. Add CLIENT secrets to Github
3. Add CLIENT and some new DB eg 'PRODDB' as DBNAME as Heroku config variables
```

## Linking to OAuth
```bash
To-Do App is using GitHub for linking to default OAuth provider to manage user access. Users will now be redirected to github to sign and access the application. You will need to register your application with OAuth provider and populate your .env file with the enviroment variables found in the .env.template with the values taken from Github OAuth. Users with "read" access will not be allowed to add, update or delete the tasks in the app.
```
## Send logs to Loggly
```bash
- poetry add loggly-python-handler //To add the dependecy pyproject.toml
```

## CI/CD Using Github Actions & Azure
```bash
Github Actions will run builds on branches after every push command. It will run the automated tests that are configured and if they pass, will deploy a Azure container using the pushed branch on this repository.

1. Set up Azure Account
2. Install the cli
3. Setting Up Your Cloud
    a. Locate Your Resource Group
    b. Set up a Cosmos database with Mongo API
    c. Connect your app to the CosmosDB
4. Host the frontend on Azure Web App
    a. Put Container Image on DockerHub registry
    b. Create a Web App
    c. Set up environment variables from .env file
    d. Confirm the live site works
5. Set up Continuous Deployment
    a. Find your webhook URL: This can located under app services >> your app >> Deployment Center >> Settings 
    b. Test your webhook url using: curl -dH -X POST "<webhook>"
    c. Add the environment variable for webhook in github repository
    d. Reference webhook environment variable in continuous-integration.yml under the "deploy" job for Azure container release
    e. Push the code for deploy and build
    f. Check azure app and the log-stream
```

## CI/CD using Github Actions and Azure Infrastructure-as-Code (IaC) and Loggly
```bash
- Log in to Azure:
    az login
    az account list
- Select the desired subscription:
    az account set --subscription="SUBSCRIPTION_ID"
- Create Service Principal and set the environment variables in the workflow    
- Handle the infrastructure provisioning using Terraform with main.tf, variables.tf and outputs.tf files.
- Update continuous_integration.yaml 
    - To initialize Terraform:
        terraform init
    - To apply Terraform with given environment variables and auto-approve flag
        terraform apply -auto-approve
    - To trigger webhook:
        curl -dH -X POST "$(terraform output webhook_url)"
- Access Azure web-app at: http://module13-azure-terraform-sj.azurewebsites.net/
- Update Loggly provisioning using Terraform with main.tf, variables.tf by adding "LOG_LEVEL" and "LOGGLY_TOKEN"
```

## Running Kubernetes locally(Minikube)
1. Spinning up a minikube cluster
    $ minikube start
2. Build application Docker image by running:
    docker build --target production --tag todo-app:prod .
3. Load the above image into minikube's local image 
    minikube image load todo-app:prod   
4. Store following secrets into Minikube literals  
    kubectl create secret generic todo-app-secrets \
  --from-literal=LOGGLY_TOKEN=****** \
  --from-literal=SECRET_KEY=****** \
  --from-literal=DBNAME=****** \
  --from-literal=CLIENT=****** \
  --from-literal=CLIENTID=****** \
  --from-literal=CLIENTSECRET=******
  CLINENTID and CLIENTSECRET are taken from GITHUB for deploying OAUTH local host app
  For decoding the secrets, follow https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/
5.To deploy the application, setup deployment.yaml and run
    kubectl apply -f deployment.yaml
6.To deploy the service, setup service.yaml and run
    kubectl apply -f service.yaml
7. Link up minikube Service with a port, 5000 on localhost
    kubectl port-forward service/module-14 5000:5000
8. Test the application by checking the values in the mongo db     
```