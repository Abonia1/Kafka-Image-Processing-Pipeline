# Image Processing Pipeline

The Image Processing Pipeline is a microservices-based application designed to efficiently process images. It leverages Kafka for asynchronous messaging, Zookeeper for managing Kafka brokers, and a scalable Python-based API for executing image processing tasks. The system is built with modularity and extensibility in mind, making it ideal for large-scale processing pipelines.

The pipeline can:

    Ingest image processing requests via RESTful APIs.
    Publish and consume events using Kafka.
    Execute customizable image processing workflows.
    Handle concurrency and scalability with ease.

## Requirements
- Python 3.8+
- Docker (optional)
- Kafka CLI Tools (Optional)

## Setup

1. Clone the repository
2. Set up the virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Option 1:Run the FastAPI server:
    ```bash
    uvicorn api.app:app --reload
    ```
    
    or

    Option 2: Run in Docker
    To build and run the server in a Docker container:

    Build the Docker image:

    ```
    docker build -f docker/Dockerfile . --no-cache
    ````

    Run the container:
    ```
    docker run -p 8000:8000 image_processing_service
    ```

## Docker Setup (Optional)

To spin up the services (API + Kafka), use Docker:

```bash
docker-compose up --build
```
### API Endpoints

POST /process-images/
Input: JSON payload with a list of image URLs.

Example request:
```
{
  "images": ["https://i.ibb.co/RNKnqMh/algea.jpg", "https://i.ibb.co/0cCYDLF/burger.jpg"]
}
```
    Output: Processing status.
    Kafka Topics
    image-processing-start: Triggered when image processing starts.
    background-removal-start: Triggered after background removal.
    background-replacement-start: Triggered after background replacement.
    hyper-resolution-start: Triggered after image upscaling.
    image-processing-end: Final message indicating the completion of the pipeline.

# Test running in docker

1. Run docker compose up to start all services.
2. Use test_api_call.py to trigger the API and verify 3. the pipeline's response.
4. Monitor Kafka topics and tasks using Kafka CLI or Kafka UI.
5. Verify processed images in the app/static folder.
6. Automate the verification of output images for consistency and correctness.

## 1. Build and Start the Docker Compose Setup
To build and run all services (Kafka, Zookeeper, and the image processing application) in Docker:

```bash
docker compose -f docker/docker-compose.yml up --build
```

This will start Kafka, Zookeeper, and the image processing service. Logs will be streamed in the terminal for debugging and progress tracking.

---

## 2. Test the API
To test the image processing API, use the provided `test_api_call.py` file:

```bash
python test_api_call.py
```

This script initiates an asynchronous call to the image processing pipeline. During execution, you can track the progress and logs in the terminal where Docker Compose is running.

---

## 3. Kafka Commands for Monitoring Tasks and Processing Status
To monitor Kafka and track processing tasks, you can use the following commands:

### a. **Check Topics**
List all topics in Kafka to ensure tasks are being published correctly:
```bash
docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --list
```

### b. **Inspect Messages in a Topic**
Read messages from a specific Kafka topic to verify task progress:
```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic <topic-name> --from-beginning
```

---

## 4. Processing Details
The image processing pipeline consists of the following steps:
1. **Background Removal**: The dish is cut out from its original background.
2. **New Background Generation**: The dish is placed on a sample background image.
3. **Hyper Resolution**: The image is upscaled and enhanced to improve resolution.

The processed images are saved in the following location:
```
app/static
```

## 5. Debugging Tips
- Use Kafka commands to monitor the flow of tasks between producers and consumers.
- Track logs in the Docker Compose terminal for real-time updates.
- Ensure the `KAFKA_BROKER` environment variable is set correctly based on runtime setup.

# Additions

1. **CI/CD**: A minimal GitHub Actions pipeline is included to lint the code and run the tests, ensuring code quality and reliability. The pipeline is located in `.github/workflows/ci_pipeline.yml`.

2. **Scalability**: Detailed documentation discussing how the image processing pipeline can be extended for higher throughput and cloud deployment is provided. [Read more here](docs/scalability_design.md).

3. **Demo**:A demo video showcasing the pipeline running Kafka locally and processing images is included. 

Demo videos:
You can view the demo videos for the project here:

[Demo Videos - Google Drive](https://drive.google.com/drive/folders/10C9xD9K8J7K-fsanbIhFu0d_JyrIf1gM?usp=drive_link)

4. **Processed images**: 
Image stored in:
```
static/processed
```
