FROM python:3.11.3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install python-dotenv for loading environment variables
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the app with python-dotenv for loading .env file
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]