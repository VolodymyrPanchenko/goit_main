import json

from confluent_kafka import Consumer, Producer
from confluent_kafka import KafkaError

IDENTIFIER = "volodymyr_panchenko"

SENSORS_TOPIC = f"building_sensors_{IDENTIFIER}"
TEMPERATURE_ALERTS_TOPIC = f"temperature_alerts_{IDENTIFIER}"
HUMIDITY_ALERTS_TOPIC = f"humidity_alerts_{IDENTIFIER}"

consumer = Consumer({
    "bootstrap.servers": "127.0.0.1:9092",
    "group.id": f"sensor-alert-processor-{IDENTIFIER}",
    "auto.offset.reset": "earliest",
})

producer = Producer({
    "bootstrap.servers": "127.0.0.1:9092",
})


def delivery_report(error, message):
    alert_type = "HUMIDITY" if message.topic() == HUMIDITY_ALERTS_TOPIC else "TEMPERATURE"
    marker = f"!!!!ALERT-{alert_type}!!!!"
    if error is not None:
        print(f"{marker} Помилка надсилання до {message.topic()}: {error}", flush=True)
    else:
        print(
            f"{marker} Переслано до {message.topic()}: "
            f"{message.value().decode('utf-8')}",
            flush=True,
        )


def send_alert(topic, data, alert_type, alert_message):
    alert = {
        "sensor_id": data["sensor_id"],
        "timestamp": data["timestamp"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "alert_type": alert_type,
        "message": alert_message,
    }

    producer.produce(
        topic=topic,
        key=str(data["sensor_id"]),
        value=json.dumps(alert, ensure_ascii=False).encode("utf-8"),
        on_delivery=delivery_report,
    )
    print(
        f"!!!!ALERT-{alert_type.upper()}!!!! Очікує доставки до {topic}: {alert_message}",
        flush=True,
    )
    producer.poll(0)


consumer.subscribe([SENSORS_TOPIC])
print(f"Очікую дані з топіка {SENSORS_TOPIC}. Для зупинки натисніть Ctrl+C.")

try:
    while True:
        producer.poll(0)
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            if message.error().code() != KafkaError._PARTITION_EOF:
                print(f"Помилка читання: {message.error()}")
            continue

        try:
            sensor_data = json.loads(message.value().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"Не вдалося розібрати повідомлення: {error}")
            continue

        temperature = sensor_data["temperature"]
        humidity = sensor_data["humidity"]

        print(
            f"Отримано з {message.topic()}. Датчик {sensor_data['sensor_id']}: "
            f"{temperature}°C, вологість {humidity}%"
        )

        if temperature > 40:
            send_alert(
                TEMPERATURE_ALERTS_TOPIC,
                sensor_data,
                "temperature",
                f"Температура {temperature}°C перевищує поріг 40°C.",
            )

        if humidity > 80:
            send_alert(
                HUMIDITY_ALERTS_TOPIC,
                sensor_data,
                "humidity",
                f"Вологість {humidity}% перевищує поріг 80%.",
            )
        elif humidity < 20:
            send_alert(
                HUMIDITY_ALERTS_TOPIC,
                sensor_data,
                "humidity",
                f"Вологість {humidity}% нижча за поріг 20%.",
            )

        remaining = producer.flush(10)
        if remaining:
            print(
                f"За 10 секунд не підтверджено доставку {remaining} сповіщень; "
                "очікується підтвердження Kafka.",
                flush=True,
            )

except KeyboardInterrupt:
    print("\nЗупиняю обробник...")

finally:
    consumer.close()
    producer.flush(10)
