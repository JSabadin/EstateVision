# Use the official Python 3.11.4 image as a parent image
FROM python:3.11.4  

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY sreality_spider.py ./
COPY app.py ./
COPY run_spider.py ./

# Expose the port the app runs on
EXPOSE 8080

# Command to run when the container starts
CMD ["sh", "-c", "python run_spider.py && python app.py"]
