# Use an official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (allows for better caching)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# The command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
