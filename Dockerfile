FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/django-test

COPY ./requirments.txt ./
RUN pip install -r ./requirments.txt 
COPY ./ /usr/src/django-test


EXPOSE 8000
# CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
