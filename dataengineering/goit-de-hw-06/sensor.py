import json
import random
import time
from datetime import datetime, timezone

from confluent_kafka import Producer


IDENTIFIER = "volodymyr_panchenko"
TOPIC = f"building_sensors_{IDENTIFIER}"
BOOTSTRAP_SERVERS = "127.0.0.1:9092"
INTERVAL_SECONDS = 5

sensor_id = random.randint(100000, 999999)
producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS})


def delivery_report(error, message):
    if error is not None:
        print(f"Помилка надсилання: {error}", flush=True)
        return

    payload = message.value().decode("utf-8")
    print(f"Надіслано до {message.topic()}: {payload}", flush=True)


print(f"Датчик запущено. ID: {sensor_id}. Для зупинки натисніть Ctrl+C.")

try:
    while True:
        data = {
            "id": sensor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": round(random.uniform(25, 45), 1),
            "humidity": round(random.uniform(15, 85), 1),
        }

        producer.produce(
            topic=TOPIC,
            key=str(sensor_id),
            value=json.dumps(data).encode("utf-8"),
            on_delivery=delivery_report,
        )
        producer.poll(0)
        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\nЗупиняю датчик...")

finally:
    remaining = producer.flush(10)
    if remaining:
        print(f"Не вдалося надіслати повідомлень: {remaining}")
