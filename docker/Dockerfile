FROM python:3.8-slim

WORKDIR /app

# Copy the rest of the application code into the image
COPY . /app/

ENV KAFKA_BROKER=kafka:9093 

# Install dependencies
RUN pip install -r requirements.txt

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
