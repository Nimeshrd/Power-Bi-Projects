# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the Python script and requirements file into the Docker image
COPY .env /app/.env
COPY bolt_fullload_candidates.py /app/bolt_fullload_candidates.py
COPY requirements.txt /app/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Run the Python script when the container starts
CMD ["python3", "bolt_fullload_candidates.py"] 