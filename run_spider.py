from scrapy.crawler import CrawlerProcess
from sreality_spider import RealitySpider

def run_spider():
    # CrawlerProcess instance with any optional configurations you need
    process = CrawlerProcess({
        # Any specific settings are defined here
    })

    # Add your RealitySpider to the process
    process.crawl(RealitySpider)

    # Start the crawling process
    process.start()

if __name__ == "__main__":
    run_spider()
