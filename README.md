# PrisonerDataAnalysis

## About the project

A Python application that processes prisoner data, provides a REST API for accessing the data, and displays the data as interactive charts in a web browser.

### Built with

- Python 3.10
  - PyMuPDF
  - Pandas
  - Fast API
  - Python_dotenv

## Getting started

To get a local copy up and running, follow these steps:

### Prerequisites

You should have the following installed on your machine:

- [Python 3](https://www.python.org/) (3.10 was used during development)
- [pip](https://pypi.org/project/pip/)

If you are using GitHub codespaces, these should be available by default.

Make sure you run `pip install -r requirements.txt` first from the `src` folder.

### load_data script usage

> [!IMPORTANT]  
> Run this script before you start the API up so it is populated with data

This script will load and manipulate the dataset using Pandas, outputting it as an SQLite file. Run it from the `src` folder.

```shell

python .\load_data.py

```

### API and dashboard usage

Before you get started, create a file called `.env` in the src folder so you can configure some authentication credentials for the API. Within the file, set an API_USERNAME and API_PASSWORD value like so:

```
API_USERNAME=joebloggs
API_PASSWORD=a-very-secure-password
```

> [!IMPORTANT]  
> Make sure you have ran `load_data.py` first so your API has data to access

Once set, run the following command within the `src` folder:

```shell

uvicorn main:app --reload

```

The front dashboard should then be accessible from <http://127.0.0.1:8000> and you can access the Swagger documentation for interacting with the API at <http://127.0.0.1:8000/docs>. When using Swagger, make sure that you click the **Authorise** button first and put in your pre-configured database credentials for HTTP Basic Auth before you try to use any of the endpoints.

If using another method of HTTP requests e.g. Postman, cURL or Invoke-WebRequests, make sure you set the Authorization header with a value of `Basic`, followed by your credentials concatenated with a colon and base 64 encoded afterwards e.g.

```http

GET /api/helloworld/joe HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Basic am9lYmxvZ2dzOmEtdmVyeS1zZWN1cmUtcGFzc3dvcmQ=

```
