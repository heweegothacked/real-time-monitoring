# Docker Instructions

This document explains how to run the project using Docker.

## Build the image

```bash
# From project root
docker build -t realtime-monitoring-ai:latest .
```

## Run the container

```bash
docker run -p 8501:8501 --rm realtime-monitoring-ai:latest
```

Then open your browser at http://localhost:8501

## Using docker-compose

```bash
docker-compose up --build
```

## Notes
- The image installs dependencies from `requirements.txt`.
- Streamlit runs on port 8501 and is exposed to the host.
- For production, consider building without mounting the host volume and configure secrets/environment variables securely.
