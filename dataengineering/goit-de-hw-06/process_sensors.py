import os
import urllib.request
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    broadcast,
    col,
    current_timestamp,
    date_format,
    from_json,
    lit,
    struct,
    to_json,
    to_timestamp,
    when,
    window,
)
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


IDENTIFIER = "volodymyr_panchenko"
BOOTSTRAP_SERVERS = "127.0.0.1:9092"
SENSORS_TOPIC = f"building_sensors_{IDENTIFIER}"
TEMPERATURE_ALERTS_TOPIC = f"temperature_alerts_{IDENTIFIER}"
HUMIDITY_ALERTS_TOPIC = f"humidity_alerts_{IDENTIFIER}"
ALERTS_CSV = "alerts_conditions.csv"

# Версія Kafka-конектора має відповідати версії PySpark у requirements.txt.
# Решта залежностей конектора вже є в пакеті pyspark.
MAVEN = "https://repo1.maven.org/maven2"
CONNECTOR_JARS = [
    "org/apache/spark/spark-sql-kafka-0-10_2.13/4.2.0/spark-sql-kafka-0-10_2.13-4.2.0.jar",
    "org/apache/spark/spark-token-provider-kafka-0-10_2.13/4.2.0/spark-token-provider-kafka-0-10_2.13-4.2.0.jar",
    "org/apache/kafka/kafka-clients/3.9.2/kafka-clients-3.9.2.jar",
    "org/apache/commons/commons-pool2/2.13.1/commons-pool2-2.13.1.jar",
]
JARS_DIR = Path(__file__).resolve().parent / "jars"


def ensure_connector_jars():
    """Завантажує jar-файли конектора один раз і повертає classpath.

    Jar-и додаються через classpath драйвера, а не через spark.jars.packages:
    на Windows packages змушує Spark робити chmod, для якого потрібен winutils.exe.
    """
    JARS_DIR.mkdir(exist_ok=True)
    paths = []
    for jar in CONNECTOR_JARS:
        target = JARS_DIR / jar.rsplit("/", 1)[1]
        if not target.exists():
            print(f"Завантажую {target.name}...", flush=True)
            urllib.request.urlretrieve(f"{MAVEN}/{jar}", target)
        paths.append(str(target))
    return os.pathsep.join(paths)


spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("SensorAlertsStreaming")
    .config("spark.driver.extraClassPath", ensure_connector_jars())
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

sensor_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
])

rules_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("humidity_min", DoubleType(), True),
    StructField("humidity_max", DoubleType(), True),
    StructField("temperature_min", DoubleType(), True),
    StructField("temperature_max", DoubleType(), True),
    StructField("code", IntegerType(), True),
    StructField("message", StringType(), True),
])

# Правила — невеликий статичний набір, який читаємо один раз.
rules = (
    spark.read
    .option("header", True)
    .schema(rules_schema)
    .csv(ALERTS_CSV)
    # id правила перейменовуємо, щоб не конфліктував з id датчика після crossJoin.
    .withColumnRenamed("id", "rule_id")
)

# Читаємо потік JSON-повідомлень із Kafka.
kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
    .option("subscribe", SENSORS_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)

sensors = (
    kafka_stream
    .select(from_json(col("value").cast("string"), sensor_schema).alias("data"))
    .select("data.*")
    .withColumn("event_time", to_timestamp(col("timestamp")))
    .filter(col("event_time").isNotNull())
)

# Вікно 1 хвилина, нове вікно кожні 30 секунд, watermark 10 секунд.
averages = (
    sensors
    .withWatermark("event_time", "10 seconds")
    .groupBy(
        window(col("event_time"), "1 minute", "30 seconds"),
        col("id"),
    )
    .agg(
        avg("temperature").alias("avg_temperature"),
        avg("humidity").alias("avg_humidity"),
    )
)


def publish_alerts(batch_df, batch_id):
    """Зіставляє середні значення з CSV і записує алерти в Kafka."""
    candidates = batch_df.crossJoin(broadcast(rules))

    # -999 означає, що відповідний показник у цьому правилі не перевіряється.
    humidity_match = (
        (col("humidity_min") != -999)
        & col("avg_humidity").between(col("humidity_min"), col("humidity_max"))
    )
    temperature_match = (
        (col("temperature_min") != -999)
        & col("avg_temperature").between(
            col("temperature_min"), col("temperature_max")
        )
    )

    alerts = (
        candidates
        .withColumn("humidity_match", humidity_match)
        .withColumn("temperature_match", temperature_match)
        .filter(col("humidity_match") | col("temperature_match"))
        .withColumn(
            "alert_type",
            when(col("humidity_match"), lit("humidity")).otherwise(lit("temperature")),
        )
        .withColumn(
            "topic",
            when(
                col("alert_type") == "humidity",
                lit(HUMIDITY_ALERTS_TOPIC),
            ).otherwise(lit(TEMPERATURE_ALERTS_TOPIC)),
        )
    )

    # Формат повідомлення як у прикладі із завдання.
    # Kafka використовує колонку topic для вибору топіка кожного повідомлення.
    kafka_messages = alerts.select(
        col("id").cast("string").alias("key"),
        to_json(
            struct(
                col("window"),
                col("id"),
                col("avg_temperature").alias("t_avg"),
                col("avg_humidity").alias("h_avg"),
                col("code").cast("string").alias("code"),
                col("message"),
                date_format(
                    current_timestamp(), "yyyy-MM-dd HH:mm:ss.SSSSSS"
                ).alias("timestamp"),
            )
        ).alias("value"),
        col("topic"),
    )

    (
        kafka_messages.write
        .format("kafka")
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
        .save()
    )
    print(f"Оброблено мікропакет {batch_id}", flush=True)


query = (
    averages.writeStream
    .outputMode("append")
    .foreachBatch(publish_alerts)
    .option("checkpointLocation", "checkpoints/sensor_alerts")
    .start()
)

print(f"Очікую дані з {SENSORS_TOPIC}. Для зупинки натисніть Ctrl+C.")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\nЗупиняю потокову обробку...")
    query.stop()
finally:
    spark.stop()
