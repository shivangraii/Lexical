FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the processing script
CMD ["python", "process_1b.py"]