# t5-service

A flask-based Docker image providing a generic pretrained T5 service.


## Installation

A conda env is provided. Simply execute:

```
conda env create -f environment.yml
```
followed by:

```
conda activate t5
```

## Model

A generic T5 model is used. For Docker deployment, it is preferable to save it to the local directory rather than repeatly downloading it.
This can be done by running the `save-t5.py` script.

## Server

The server is contained in `app.py`, so all modifications should be made there.

To run the server using flask, do:

```
export FLASK_APP=app.py
flask run
```

The Dockerfile in specifies a build using [Gunicorn](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/) for production.
You can build a docker image with e.g.:

```
docker build --tag t5-service:1.0 .
```

and run with, e.g.:

```
docker run -p 8000:8000 t5-service:1.0
```

[Postman](https://learning.postman.com/) tests are in `t5.postman_collection.json`, with different ports for flask and gunicorn (5000 for flask, 8000 for gunicorn).
These tests document how to call the server, but essentially it is POSTing JSON like this:

```json
{
    "text":"Epithelial tissue, also referred to as  <extra_id_0>, refers to the sheets of cells that cover exterior surfaces of the body, line internal cavities and passageways, and form certain glands."
}
```
