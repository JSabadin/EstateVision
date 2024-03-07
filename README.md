# EstateVision Project

## Overview
EstateVision is a web scraping and data display project that scrapes real estate listings from `sreality.cz` and saves the data in a PostgreSQL database. A simple Flask server serves a webpage displaying the first 500 items from the database.

## Quickstart
To run this project, you'll need Docker and Docker Compose installed on your system.

1. Clone the repository to your local machine.
2. Navigate to the project directory where the `compose.yaml` file is located.
3. Run the project using Docker Compose: docker-compose up

Docker will build the images and start the containers necessary for the Scrapy spider and Flask application. 

## Viewing Results
Once the Docker containers are running, you can view the scraped data by visiting the following URL in your web browser:
[http://localhost:8080/](http://localhost:8080/)

This page will display the first 500 scraped real estate listings with their titles and images.

## Project Structure
- `app.py`: Flask app to display scraped data.
- `run_spider.py`: Runs the Scrapy spider.
- `sreality_spider.py`: Scrapy spider for real estate listings.
- `requirements.txt`: Lists dependencies.
- `Dockerfile`: Instructions to build the app's Docker image.
- `compose.yaml`: Configures the app's services.
