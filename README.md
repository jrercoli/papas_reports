# Papas Reports API

Builded with Python 3, Django 3.2

## What does the app?

The app must allow you to upload 3 external data files (customers, products and orders) to then build certain reports with information necessary for different areas of the company.

The reports are:
- order report with its total
- report of customers who have purchased each product
- total ranking in euros purchased by customers

All these reports must be requested through API calls.

## How to install


## On test coverage


## Steps and bibliography used for development

To develop the app in Python using the Django framework, these steps have been followed:
- Create virtual environment with venv
- Install Django framework and other necessary libraries (which are described in requirements.txt)
- Create a django project along with the necessary app (reports)
- Configure the DB in settings.py, in this case the default configuration has been left using SqLite, as it's a PoC type project.
- Create the business object models, necessary to store the external data that needs to be uploaded. Then run the migrations to create DB tables.
- Enter test data into the models using Django Admin 
- Build the business controllers (views in Django) that provide the processes to generate the 3 required reports with their corresponding API and validate their outputs using test data.
- Create a simple web form to upload external data and build the importers for each file.
- Recreate the calls to the reports' APIs and validate the output with the official project data.

Bibliography:
- Official django site - https://www.djangoproject.com/
- Example of CSV upload with Django - https://djangosource.com/django-csv-upload

