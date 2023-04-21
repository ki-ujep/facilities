#pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /src

# prevents Python from writing pyc files to disc and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .