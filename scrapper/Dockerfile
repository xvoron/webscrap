FROM python:3.10-alpine

WORKDIR /scrapper
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy", "crawl", "scrapper"]
