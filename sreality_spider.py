import json
import re
import scrapy
import psycopg2
import os

class RealitySpider(scrapy.Spider):
    """
    A spider to scrape flat listings from the Sreality API and store them in a PostgreSQL database.
    """
    name = 'reality_spider'
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500']
    batch_size = 100  # Desired batch size

    def start_requests(self):
        """
        Start the spider and establish the database connection.
        """
        # Read database connection parameters from environment variables
        conn_params = {
            'host': os.getenv('POSTGRES_HOST'), 
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
        self.items_buffer = []  # Initialize a buffer for the batched items

        # Continue with starting the requests
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        Parse the JSON response and extract the flat titles and image URLs.
        """
        # Parse the JSON response
        response_json = json.loads(response.text)
        # Iterate through each flat in the response
        for flat in response_json.get('_embedded').get('estates'):
            title = re.sub(r'\s+', ' ', flat.get('name'))  # Clean the title
            image_url = flat.get('_links').get('images')[0].get('href')  # Extract the URL of the image
            self.items_buffer.append((title, image_url))  # Add the item to the buffer

            # If the buffer size reaches our batch size, insert the items
            if len(self.items_buffer) >= self.batch_size:
                self.insert_batch()
                self.items_buffer = []  # Reset the buffer after insertion

    def closed(self, reason):
        """
        Close the database connection and insert any remaining items in the buffer when the spider closes.
        """
        # Insert any remaining items in the buffer when the spider closes
        if self.items_buffer:
            self.insert_batch()

        # Close the cursor and database connection
        self.cursor.close()
        self.connection.close()

    def insert_batch(self):
        """
        Insert the batch of items into the database.
        """
        # Insert the batch of items into the database
        self.cursor.executemany(
            "INSERT INTO flats (title, image_url) VALUES (%s, %s)",
            self.items_buffer
        )
        self.connection.commit()
