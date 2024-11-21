# Use Python 3.13.0 as the parent image (if available)
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed dependencies (including all packages listed in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the bot will run on (optional, typically for web apps)
EXPOSE 8080

# Run the bot when the container launches
CMD ["python", "main.py"]
