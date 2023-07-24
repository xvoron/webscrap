FROM python:3.10-slim-buster

WORKDIR /scrapper
COPY . /scrapper

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /scrapper/scrapper
CMD ["scrapy", "crawl", "srealitybot"]
