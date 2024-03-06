import json
import re
import scrapy
import psycopg2
import os 

class RealitySpider(scrapy.Spider):
    name = 'reality_spider'
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500']

    def start_requests(self):
        # Read database connection parameters from environment variables
        conn_params = {
            'host': os.getenv('POSTGRES_HOST'),  # Default to 'localhost' if not set
            'dbname': os.getenv('POSTGRES_DB'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD')
        }

        # Here, we establish the database connection
        self.connection = psycopg2.connect(**conn_params)
        self.cursor = self.connection.cursor()
        # We ensure the table exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS flats (
                id SERIAL PRIMARY KEY,
                title TEXT,
                image_url TEXT
            );
        """)
        self.connection.commit()

        # Then we continue with starting the requests
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # Parse the JSON response
        response_json = json.loads(response.body)
        # Iterate through each flat in the response
        for flat in response_json.get('_embedded').get('estates'):
            title = re.sub(r'\s+', ' ', flat.get('name')) # Replace multiple whitespace characters with a single space
            image_url = flat.get('_links').get('images')[0].get('href') # Extract the URL of the first image

            # Insert directly into the database
            self.cursor.execute(
                "INSERT INTO flats (title, image_url) VALUES (%s, %s)",
                (title, image_url)
            )
            self.connection.commit()

    def closed(self, reason):
        # Close the database connection
        self.connection.close()



