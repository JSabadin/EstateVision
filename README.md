# EstateVision Project

## Overview
EstateVision is a web scraping and data display project that scrapes real estate listings from `sreality.cz` and saves the data in a PostgreSQL database. A simple Flask server serves a webpage displaying the first 500 items from the database.

## Quickstart
To run this project, you'll need Docker and Docker Compose installed on your system.

1. Clone the repository to your local machine.
2. Navigate to the project directory where the `docker-compose.yml` file is located.
3. Run the project using Docker Compose: docker-compose up

Docker will build the images and start the containers necessary for the Scrapy spider and Flask application. 

## Viewing Results
Once the Docker containers are running, you can view the scraped data by visiting the following URL in your web browser:
[http://localhost:8080/](http://localhost:8080/)

This page will display the first 500 scraped real estate listings with their titles and images.

## Project Structure
- `app.py`: The Flask application file.
- `run_spider.py`: Script to initiate the Scrapy spider.
- `sreality_spider.py`: The Scrapy spider that scrapes the real estate data.
- `requirements.txt`: The required Python libraries.
- `Dockerfile`: Dockerfile for building the Flask application container.
- `compose.yaml`: Docker Compose file to orchestrate the containers.
