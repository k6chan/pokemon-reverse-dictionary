# pokemon-reverse-dictionary

A reverse dictionary for Pokemon as a Python Flask web app.

## Setup

*With approval from my TA, a `run.py` script is not necessary for this website project.*

### Without Docker

First, clone the repository to your device with `git clone`.

Install the Python libraries in `requirements.txt` with `pip install --no-cache-dir -r requirements.txt`.

Change directory into `src/models` and use the following command to run the dev server:

`python -m flask --app application run`

Access the server in your browser, usually `http://127.0.0.1:5000/`.

### With Docker (automatically installs libraries and starts the dev server)

**The Flask server hosting is not compatible with Docker on DSMLP. This Docker image can only be run locally, not on DSMLP.**

```
DockerHub repository:

https://hub.docker.com/repository/docker/k6chan/reverse-dictionary-pokemon
```

Run the Docker image using `docker run -it --rm -p 5000:5000 k6chan/reverse-dictionary-pokemon:latest`.

The Flask server should automatically start up. Access the server in your browser, usually `http://127.0.0.1:5000/`.

If you receive an error in the LocalProxy stating `__init__() got an unexpected keyword argument 'unbound_message'`, downgrade to an older version of Flask 2.2.x: `pip install flask==2.2.0`

## Contribution Statement
Solo project by Kaitlyn Chan.
