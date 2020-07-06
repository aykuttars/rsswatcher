FROM python:3.8
ENV PYTHONUNBUFFERED  1

WORKDIR /usr/src/app/backend
COPY . /usr/src/app/backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt