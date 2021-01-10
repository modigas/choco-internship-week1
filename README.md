# Simple WEB crawler

Simple Django projects that scrapes data from four websites:
* www.sulpak.kz
* www.shop.kz
* www.technodom.kz
* www.mechta.kz

Requirments
* PostgreSQL 13
* Google Chrome 87 opened (for Selenium)

For web scraping, this project utilizes Scrapy together with Selenium (headless chrome). The project is pushed together with an virtual environment.
You can launch the project by firstly utilizing the following command (on Linux or Mac OS):
```
source env/bin/activate
```
At this stage. Not all websites are handled (Mechta and Technodom). The crawling can be launched manually by executing the following command:
```
python manage.py scrape
```
scrape is the command that launches scrapy spiders, that writes all data in the PostgreSQL database.
