# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY . /app
WORKDIR /app

# Install the dependencies
RUN uv sync --frozen --no-cache

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]