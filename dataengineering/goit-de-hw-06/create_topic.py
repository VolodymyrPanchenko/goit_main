from confluent_kafka.admin import AdminClient, NewTopic


IDENTIFIER = "volodymyr_panchenko"
BOOTSTRAP_SERVERS = "127.0.0.1:9092"

TOPICS = [
    f"building_sensors_{IDENTIFIER}",
    f"temperature_alerts_{IDENTIFIER}",
    f"humidity_alerts_{IDENTIFIER}",
]

admin = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})
existing_topics = set(admin.list_topics(timeout=10).topics)
topics_to_create = [
    NewTopic(name, num_partitions=1, replication_factor=1)
    for name in TOPICS
    if name not in existing_topics
]

if topics_to_create:
    for name, future in admin.create_topics(topics_to_create).items():
        try:
            future.result()
            print(f"Створено топік: {name}")
        except Exception as error:
            print(f"Не вдалося створити топік {name}: {error}")
else:
    print("Усі потрібні топіки вже існують.")

print("\nТопіки проєкту:")
for name in TOPICS:
    print(name)
