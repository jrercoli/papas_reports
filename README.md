# Papas Reports API

Builded with Python 3, Django 3.2

## What does the app?

The app must allow you to upload 3 external data files (customers, products and orders) to then build certain reports with information necessary for different areas of the company.

The reports are:
- order report with its total
- report of customers who have purchased each product
- total ranking in euros purchased by customers

All these reports must be requested through API calls.

## How to install and run
First, you will need to clone locally the remote repo (git clone repository)  
To make the execution of the app simple, it is possible to run it inside a [Docker](https://docs.docker.com/engine/install/) container, for which we must have Docker installed locally.  
First we need to build the container:
```bash
docker build -t papas-reports-app .
```
Second, you will be ready to run the dockerized app, this allow to start the Django web server in port 8000:
```bash
docker run -it -p 8000:8000 papas-reports-app
```
Then you could use the app:
- To upload csv data type http://localhost:8000/upload_data/ in your browser. The csv data are in the project's ext_data folder.
- To download the csv output reports type :
    * http://localhost:8000/api/v1/reports/order_totals/ to obtain Orders report.
    * http://localhost:8000/api/v1/reports/customers_product/ to obtain Customer who buys each Product report.
    * http://localhost:8000/api/v1/reports/customer_rank/ to obtain Customer buy ranking report.
- To watch the app business models and objects you could run the Django Admin built-in app, to login you must use a previously user created for this test purpose (user=admin, passw=admin1234)  
http://localhost:8000/admin

## On test coverage
There are some API tests in reports/tests.py.

These tests prove :
- that the urls for upload data to import and download reports, can be called correctly by returning a HTTP 200 (ApiStatusOkTest class)
- that the download reports API calls returns the specified data structure (ApiDownloadDataTest class)
- that the import processes of the uploaded external data, correctly create the specified models of the application (ApiImportDataTest class)

```bash
python3 manage.py test --verbosity 2
```

## Steps and bibliography used for development

To develop the app in Python using the Django framework, these steps have been followed:
- Create virtual environment with venv
- Install Django framework and other necessary libraries (which are described in requirements.txt)
- Create a django project along with the necessary app (reports)
- Configure the DB in settings.py, in this case the default configuration has been left using SqLite, as it's a PoC type project.
- Create the business object models, necessary to store the external data that needs to be uploaded. Then run the migrations to create DB tables. Create a superuser to allow login in Django Admin app
- Enter test data into the models using Django Admin app
- Build the business controllers (views in Django) that provide the processes to generate the 3 required reports with their corresponding API and validate their outputs using test data.
- Create a simple web form to upload external data and build the importers for each file.
- Recreate the calls to the reports' APIs and validate the output with the official project data.

Bibliography:
- [Official django site](https://www.djangoproject.com/)
- [Example of CSV upload with Django](https://djangosource.com/django-csv-upload)

## On Production Readiness

This implementation, to be production ready, requires at least the following:

* Authentication and Authorization, this API does not implement any right now. It could be helpful to use JWT tokens as a first solution.
* Database storage, this app is using Sqlite to have a simply way to manage test data, but we need a more robust DB engine like PostgreSQL in production. It could be use a Docker service who runs it and expose port to interact with the dockerized app (we'll need to use docker-compose to define the services).  
Also we need to define some useful environment variables (Postgres DB, USER, PASSW, etc), for which an env_template file must be defined and stored in the repo with the constants to use, then in PROD they are stored in a secure env file which will be accessed from the app with the [python-dotenv](https://pypi.org/project/python-dotenv/) library
* Remove secrets from `settings.py` and put them in safe storage, such as AWS Secrets Manager.
* Debug mode is on, it must be set to False in the PROD environment.
* It needs a CD pipeline to deploy to different environments, such as staging and production.  

One last Tip about manage a big data volume:  

If the volume of data to be imported was significant, we could use [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) to run each of the 3 importers in the background asynchronously.  
In this case we can execute the Product and Customer importers in parallel (using task groups) and when both finish, execute sequentially (using task then) the order importer because it is dependent on the previous ones.  
To use Celery we also need include a message transport broker like Redis or RabbitMQ to send and receive messages.

