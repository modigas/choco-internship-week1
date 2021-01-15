FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/django-scraper

COPY ./requirments.txt ./
RUN pip install -r ./requirments.txt 
COPY ./ /usr/src/django-scraper


EXPOSE 8000