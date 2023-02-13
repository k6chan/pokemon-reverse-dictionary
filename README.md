# pokemon-reverse-dictionary

A reverse dictionary for Pokemon as a Python Flask web app.

## Setup

Change directory into `src/models` and use the following command to run the dev server:

`python -m flask --app application run`

### Docker

With approval from my TA, a `run.py` script is not necessary for this website project.

```
DockerHub repository:

https://hub.docker.com/repository/docker/k6chan/reverse-dictionary-pokemon
```

If you receive an error in the LocalProxy stating `__init__() got an unexpected keyword argument 'unbound_message'`, downgrade to an older version of Flask 2.2.x: `pip install flask==2.2.0`

Docker networking may not be compatible with the Flask app out of the box. At this moment, you may not be able to access the dev server through Docker on DSMLP.

## Contribution Statement
Solo project by Kaitlyn Chan.