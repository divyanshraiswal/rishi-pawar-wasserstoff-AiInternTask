# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Download the SpaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code into the container
COPY . .

# Expose the MongoDB port (if needed)
EXPOSE 27017

# Command to run your script
CMD ["python", "app.py"]
