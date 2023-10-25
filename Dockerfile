# pull official base image
FROM rayproject/ray:2.7.0

# set work directory
WORKDIR /serve_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY main.py /serve_app/main.py

# install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install fastapi==0.103.1 pydantic==1.10.13