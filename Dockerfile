# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file (outside of app folder) into the container
COPY requirements.txt /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the entire project directory (including app) into the container
COPY . /app

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.app

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]