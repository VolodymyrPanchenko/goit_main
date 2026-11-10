from confluent_kafka import Consumer, KafkaError


IDENTIFIER = "volodymyr_panchenko"
ALERT_TOPICS = [
    f"temperature_alerts_{IDENTIFIER}",
    f"humidity_alerts_{IDENTIFIER}",
]

consumer = Consumer({
    "bootstrap.servers": "127.0.0.1:9092",
    "group.id": "alerts_console_consumer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})
consumer.subscribe(ALERT_TOPICS)

print("Очікую сповіщення. Для завершення натисніть Ctrl+C.")

try:
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            if message.error().code() != KafkaError._PARTITION_EOF:
                print(f"Помилка читання: {message.error()}")
            continue

        payload = message.value().decode("utf-8")
        print(
            f"Отримано повідомлення з топіка '{message.topic()}': {payload}",
            flush=True,
        )

except KeyboardInterrupt:
    print("\nСпоживача зупинено.")

finally:
    consumer.close()
