FROM python:3.11-slim

WORKDIR /app

COPY mock_wearable.py .

RUN pip install influxdb

CMD ["python", "mock_wearable.py"]
