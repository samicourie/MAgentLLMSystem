# Use Python 3.13.5 slim image
FROM python:3.13.5-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project source code into the container
COPY src/ ./src/
COPY assets/ ./assets/

# Copy the .env file into the container
COPY src/.env ./src/.env 

# Command to run your app
CMD ["python", "src/main.py"]
