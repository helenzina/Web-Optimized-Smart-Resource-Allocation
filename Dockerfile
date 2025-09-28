# Use the official Python runtime image
FROM python:3.11-slim

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Copy the Django project and install dependencies
COPY requirements.txt /app/

# Install system dependencies
RUN apt-get update

# Upgrade pip
RUN pip install --upgrade pip 


# Run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY web_allocation_project/ /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn command with correct path
CMD ["gunicorn", "web_allocation_project.wsgi:application", "--bind", "0.0.0.0:8000"]
