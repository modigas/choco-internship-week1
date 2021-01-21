FROM python:3.7.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/django-scraper

COPY ./requirments.txt ./
RUN pip install -r ./requirments.txt 
COPY ./ /usr/src/django-scraper

RUN chmod +x launch_script.sh
# RUN export GOOGLE_APPLICATION_CREDENTIALS="/usr/src/django-scraper/Choco-Products-Scraper-94e179d2134a.json"

EXPOSE 8000

# CMD ["./launch_script.sh"]
