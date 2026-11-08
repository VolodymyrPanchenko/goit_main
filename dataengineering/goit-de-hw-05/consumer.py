from confluent_kafka import Consumer, KafkaError

topics = [
    "temperature_alerts_volodymyr_panchenko",
    "humidity_alerts_volodymyr_panchenko",
]

consumer = Consumer({
    "bootstrap.servers": "127.0.0.1:9092",
    "group.id": "alerts_console_consumer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})
consumer.subscribe(topics)

print("Очікування сповіщень. Для завершення натисніть Ctrl+C.")

try:
    while True:
        message = consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            if message.error().code() != KafkaError._PARTITION_EOF:
                print(f"Помилка читання: {message.error()}")
            continue

        print(
            f"Отримано повідомлення з топіка "
            f"'{message.topic()}': {message.value().decode('utf-8')}"
        )

except KeyboardInterrupt:
    print("\nСпоживача зупинено.")

finally:
    consumer.close()
