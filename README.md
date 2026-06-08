# gen-ui-lab

Docker-based project using C1 by Thesys ([docs](https://docs.thesys.dev/guides/what-is-thesys-c1)), a Generative UI API.

## Overview

This project simulates data from a wearable device (for example, Garmin) using a Python generator and displays the results in a React frontend.

Example flow:
- The user enters a prompt such as: `Show me my stress and heart rate today`
- The backend uses a local model through Ollama to interpret the request
- The backend queries InfluxDB
- The backend sends structured data and UI instructions to Thesys C1
- Thesys C1 generates the dashboard
- The React frontend renders the generated UI

## Requirements

Before starting, install:
- Docker Desktop

If you want to run the frontend outside Docker for local development, you can also install Node.js and run `npm install` inside `frontend/`. This is not required if you use only Docker. 

## Project Structure

- `frontend/` - React frontend source code
- `backend/` - Backend application
- `mock-wearable/` - Synthetic wearable data generator
- `docker-compose.yml` - Docker Compose configuration
- `influx-data`, `ollama-data` - Named Docker volumes for persistent data

## Getting Started

Clone the repository:

```bash
git clone https://github.com/alecsus1/gen-ui-lab.git
cd gen-ui-lab
```

Create the environment file:

```bash
cp .env.example .env
```

Start all services:

```bash
docker compose up -d --build
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

## Ollama model setup

If the project expects the `llama2` model, make sure it is available in Ollama:

```bash
docker exec -it ollama ollama pull llama2
```

## InfluxDB queries

Open the InfluxDB CLI:

```bash
docker exec -it influxdb influx -database 'garmin' -precision rfc3339
```

Useful test queries:

```sql
SELECT * FROM "wearable_metrics" ORDER BY time DESC LIMIT 5;
SELECT max("heart_rate") FROM "wearable_metrics" GROUP BY "activity";
SELECT count("heart_rate") FROM "wearable_metrics";
```

## Services

| Service | Port | Description |
|---|---:|---|
| Frontend | 3000 | React UI |
| InfluxDB | 8086 | Time-series database |
| Ollama | 11434 | Local LLM service |

---
Project by [alecsus1](https://github.com/alecsus1)

