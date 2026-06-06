import time
import random
from datetime import datetime, timezone
import os
from influxdb import InfluxDBClient

# ============================
# CONFIGURAZIONE INFLUXDB 1.x
# ============================
INFLUX_HOST = os.getenv("INFLUX_HOST", "influxdb")  # nome servizio Docker
INFLUX_PORT = int(os.getenv("INFLUX_PORT", "8086"))
INFLUX_DB   = os.getenv("INFLUX_DB", "garmin")
INFLUX_USER = os.getenv("INFLUX_USER") or None
INFLUX_PWD  = os.getenv("INFLUX_PWD") or None

client = InfluxDBClient(
    host=INFLUX_HOST,
    port=INFLUX_PORT,
    username=INFLUX_USER,
    password=INFLUX_PWD,
    database=INFLUX_DB,
)

# crea database se non esiste
dbs = [d["name"] for d in client.get_list_database()]
if INFLUX_DB not in dbs:
    client.create_database(INFLUX_DB)
    print(f"Creato database '{INFLUX_DB}'")

# ============================
# PARAMETRI ATTIVITÀ
# ============================
activity_params = {
    "running": {"hr_min": 120, "hr_max": 180, "step_range": (1, 3), "calorie_factor": 0.05},
    "walking": {"hr_min": 80,  "hr_max": 120, "step_range": (1, 2), "calorie_factor": 0.03},
    "cycling": {"hr_min": 100, "hr_max": 160, "step_range": (0, 0), "calorie_factor": 0.07},
}

# puoi cambiare activity da qui o con futura variabile d'ambiente
current_activity = os.getenv("MOCK_ACTIVITY", "walking")
if current_activity not in activity_params:
    current_activity = "walking"

# NB: per aggiornare lo script in Docker:
# docker compose up -d --build mock-wearable

# ============================
# STATO INIZIALE
# ============================
params = activity_params[current_activity]

hr = random.randint(params["hr_min"] + 5, params["hr_max"] - 5)
steps = 0
calories = 0.0
distance = 0.0

stress_prev = (hr - params["hr_min"]) / (params["hr_max"] - params["hr_min"]) * 100
STEP_LENGTH = 0.78  # metri

print(f"Simulatore avviato: activity={current_activity}, device=simulated_garmin_265")

# ============================
# LOOP SIMULAZIONE
# ============================
try:
    while True:
        # --- aggiorna HR
        hr += random.choice([-1, 0, 1])
        hr = max(params["hr_min"], min(params["hr_max"], hr))

        # --- passi, calorie, distanza
        step_inc = random.randint(*params["step_range"])
        steps += step_inc
        calories += params["calorie_factor"] * (step_inc / 2)
        distance += step_inc * STEP_LENGTH

        # --- stress
        base_stress = (hr - params["hr_min"]) / (params["hr_max"] - params["hr_min"]) * 100
        stress_raw = base_stress + random.uniform(-5, 5)
        stress_raw = max(0, min(100, stress_raw))
        stress = 0.8 * stress_prev + 0.2 * stress_raw
        stress_prev = stress

        # --- timestamp
        timestamp = datetime.now(timezone.utc)

        # --- point unico "wearable_metrics" (compatibile con data-api e ai-backend)
        json_body = [
            {
                "measurement": "wearable_metrics",
                "tags": {
                    "device": "simulated_garmin_265",
                    "activity": current_activity,
                },
                "time": timestamp,
                "fields": {
                    "heart_rate": int(hr),
                    "steps": int(steps),
                    "stress": float(round(stress, 2)),
                    "calories": float(round(calories, 2)),
                    "distance": float(round(distance, 2)),
                },
            }
        ]

        # --- scrittura su InfluxDB
        client.write_points(json_body)

        # --- debug console
        print(
            f"[{timestamp.isoformat()}] activity: {current_activity} "
            f"HR: {hr} bpm | Steps: {steps} | "
            f"Calories: {calories:.2f} kcal | Distance: {distance:.2f} m | "
            f"Stress: {stress:.2f}"
        )

        time.sleep(1)

except KeyboardInterrupt:
    print("Simulazione interrotta dall'utente")
