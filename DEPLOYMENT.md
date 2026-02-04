# Deployment with Docker

This guide shows how to build and run the project using Docker (recommended for consistent environments).

## Build the image

```powershell
# From project root
docker build -t realtime-monitoring:latest .
```

## Run the container

```powershell
# Map local port 8501 to container port 8501
docker run -p 8501:8501 realtime-monitoring:latest
```

Open your browser to `http://localhost:8501` to view the dashboard.

## Optional: Use Docker Compose

Create a `docker-compose.yml` (example):

```yaml
version: '3.8'
services:
  monitoring:
    image: realtime-monitoring:latest
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
```

Then run:

```powershell
docker-compose up --build -d
```

## Notes
- The Dockerfile disables Streamlit telemetry by creating `/root/.streamlit/config.toml` with `gatherUsageStats = false`.
- If you want to run the app on a different port, set the port mapping accordingly (e.g., `-p 8080:8501`) and visit `http://localhost:8080`.
- For production deployments, consider using a minimal reverse proxy and enabling a production-ready server environment.
