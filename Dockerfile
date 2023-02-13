# Python Docker image
FROM python:3.8-slim-buster

RUN apt-get -y update

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR src/models

CMD ["python", "-m", "flask", "--app", "application", "run", "--host=0.0.0.0"]