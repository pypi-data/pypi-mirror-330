# Use a small base image like Alpine
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the Python requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python file
COPY app.py .

# Expose the port for the REST API
EXPOSE 5000

# Run the Python file serving the REST API
CMD ["python", "app.py", "--host", "0.0.0.0"]