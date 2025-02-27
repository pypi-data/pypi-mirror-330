# FastCrawl

<p align="left">
<a href="https://github.com/ilarionkuleshov/fastcrawl/actions/workflows/code-quality.yml/?query=event%3Apush+branch%3Amain">
    <img src="https://github.com/ilarionkuleshov/fastcrawl/actions/workflows/code-quality.yml/badge.svg?event=push&branch=main">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/ilarionkuleshov/fastcrawl">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/ilarionkuleshov/fastcrawl.svg">
</a>
<a href="https://pypi.org/project/fastcrawl">
    <img src="https://img.shields.io/pypi/v/fastcrawl?color=%2334D058">
</a>
<a href="https://pypi.org/project/fastcrawl">
    <img src="https://img.shields.io/pypi/pyversions/fastcrawl.svg?color=%2334D058">
</a>
</p>

FastCrawl is a Python library for web crawling and scraping, inspired by [Scrapy](https://github.com/scrapy/scrapy) but designed to run seamlessly in asynchronous applications. Built on top of [Httpx](https://github.com/encode/httpx), it provides a lightweight foundation for creating custom crawlers based on the `BaseCrawler` class. The library supports defining custom pipelines for processing scraped items, which can be easily implemented by extending the `BasePipeline` class. While its functionality is still growing, FastCrawl offers flexible settings options for the crawler, HTTP client, requests, and more.


## Installation
FastCrawl is available on PyPI and can be installed using pip:
```bash
pip install fastcrawl
```


## Usage
Here is a simple example of how to create a custom crawler using FastCrawl:
```python
import asyncio
from typing import AsyncIterator

from pydantic import BaseModel
from fastcrawl import BaseCrawler, BasePipeline, Request, Response, CrawlerSettings


class ExampleItem(BaseModel):
    title: str


class ExamplePipeline(BasePipeline):
    allowed_items = [ExampleItem]

    async def process_item(self, item: ExampleItem) -> ExampleItem:
        self.logger.info(f"Processing item: {item}")
        return item


class ExampleCrawler(BaseCrawler):
    settings = CrawlerSettings(
        pipelines=[ExamplePipeline],
    )

    async def generate_requests(self) -> AsyncIterator[Request]:
        yield Request(url="http://example.com/", callback=self.parse)

    async def parse(self, response: Response) -> AsyncIterator[ExampleItem]:
        title = response.selector.xpath(".//h1/text()").get() or "unknown"
        yield ExampleItem(title=title)


asyncio.run(ExampleCrawler().run())
```

In this example, we define a custom `ExampleItem` model, a `ExamplePipeline` for processing scraped items, and an `ExampleCrawler` that generates requests and parses responses.

Crawler can be set up using the `settings` class attribute or by passing a `CrawlerSettings` instance to the constructor. See the model definition for all available settings.

Method `generate_requests` is executed once at the beginning of the crawl and should yield `Request` objects to start the crawl. Each request should have a callback function that will be called with the `Response` object when the request is completed.

In request callbacks, you can use the `Response` object to extract data using XPath selectors or other methods. Also you can yield another requests to follow links or scrape paginated content.

In pipelines, you can implement custom logic for processing items, such as saving them to a database, sending them to a message queue, or logging them. When defining a pipeline, you specify allowed types of items. The example specifies the `ExampleItem` pydantic model, but you can use any type you need. If the crawler returned an item of a different type, the pipeline would be skipped for that item. But if you don't specify any allowed items at all, then this check will not occur.


## License
This project is licensed under the MIT License.
