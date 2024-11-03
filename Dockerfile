# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies directly into the container's Python environment
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies and only the Chromium browser
RUN playwright install-deps && playwright install chromium

# Copy the application code into the container
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
