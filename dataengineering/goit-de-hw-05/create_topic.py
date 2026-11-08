from confluent_kafka.admin import AdminClient, NewTopic

identifier = "volodymyr_panchenko"

topic_names = [
    f"building_sensors_{identifier}",
    f"temperature_alerts_{identifier}",
    f"humidity_alerts_{identifier}",
]

admin_client = AdminClient({"bootstrap.servers": "127.0.0.1:9092"})

existing_topics = set(admin_client.list_topics(timeout=10).topics)
topics_to_create = [
    NewTopic(name, num_partitions=1, replication_factor=1)
    for name in topic_names
    if name not in existing_topics
]

if topics_to_create:
    for name, future in admin_client.create_topics(topics_to_create).items():
        future.result()
        print(f"Створено топік: {name}")
else:
    print("Усі три топіки вже існують.")

print("\nПеревірка топіків:")
metadata = admin_client.list_topics(timeout=10)
for topic in metadata.topics:
    if identifier in topic:
        print(topic)
