from scrapy.crawler import CrawlerProcess
from sreality_spider import RealitySpider

def run_spider():
    """
    Run the RealitySpider to scrape flat listings from the sreality.cz and store them in a PostgreSQL database.
    """
    # CrawlerProcess instance with any optional configurations you need
    process = CrawlerProcess({
        # Any specific settings are defined here
    })

    # Crawl the spider
    process.crawl(RealitySpider)

    # Start the crawling process
    process.start()

if __name__ == "__main__":
    run_spider()
