Docker-based project using C1 by Thesys (https://docs.thesys.dev/guides/what-is-thesys-c1), a Generative UI API. 
* Copy and rename the .env.example file to .env,
* inserting your Thesys API key into the frontend folder.
* Run "npm install" to create the node_modules folder.
* Run "docker compose up -d" to create the node_modules folder.
# gen-ui-lab


This project uses a Python script that generates synthetic data to simulate a wearable device (e.g., Garmin).
1. Displays a React UI
2. Has a prompt field
3. The user writes:
"Show me my stress and heart rate today"
4. The backend:
* Uses llama2 to figure out what to do
* Queries InfluxDB
* Sends data + instructions to Thesys C1
5. Thesys C1 generates the dashboard
6. React renders it
7. Conversational memory maintained





## Requirements

Before you begin, make sure you have installed on your computer.:
* **Docker desktop** 
* run the command in the frontend folder
```bash
npm install
```
to create the node_modules folder 


## Project Structure


* `frontend/` - UI source code (React/Vue/Next.js)
* `docker-compose.yml` - Docker services configuration
* `influx-data` & `ollama-data` - Named volumes automatically managed by Docker


## How to Start the Project

Follow these steps to start the entire local environment:

1. **Clone the repository:**
```bash
git clone https://github.com/alecsus1/gen-ui-lab.git
cd nome-repo
```


2. **Configure environment variables:**
Create a .env file from the example file:
```bash
cp .env.example .env
```
*(Enter your InfluxDB tokens or other configurations here.)*


3. **Launch Docker containers:**
```bash
docker compose up -d
```


The frontend will be accessible at `http://localhost:3000`.

**Terminal commands to query influxdb:**
* Enter the interactive CLI:
```bash
docker exec -it influxdb influx -database 'garmin' -precision rfc3339
```
**Ready-to-test queries:
* Check for data (shows the last 5 entries):
```bash
SELECT * FROM "wearable_metrics" ORDER BY time DESC LIMIT 5
```
* Display the maximum heart rate recorded for each activity type:
```bash
SELECT max("heart_rate") FROM "wearable_metrics" GROUP BY "activity"
```
* Count how many total records have been saved to the table so far:
```bash
SELECT count("heart_rate") FROM "wearable_metrics"
```

## Included Services

| Service | Port | Description |
| :--- | :--- | :--- |
| **Frontend** | `3000` | Node.js UI |
| **InfluxDB** | `8086` | Time Series Database |
| **Ollama** | `11434` | Local AI Models |


---
Project by [alecsus1](https://github.com/alecsus1)

