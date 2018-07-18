# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POSTGRES_DB postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres

# Create and set working directory
RUN mkdir /code
WORKDIR /code

# Copy contents of current directory into working directory
ADD . /code/

# Install
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
