# Use an official Python runtime as a parent image
FROM python:3.12.5-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --update --no-cache postgresql-client 

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend project
RUN mkdir /backend 
COPY . /backend

# Set the working directory in the container
WORKDIR /backend

RUN ls

# Expose the port that the Django app runs on
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "socialdilemma.wsgi:application"]
