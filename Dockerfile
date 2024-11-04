FROM python:3.12

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# create directories for static and media files
RUN mkdir -p /usr/src/static && \
    mkdir -p /usr/src/media && \
    chmod 755 /usr/src/static && \
    chmod 755 /usr/src/media

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn

# copy project
COPY ./src /usr/src/