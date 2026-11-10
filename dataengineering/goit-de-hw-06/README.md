# Kafka sensor alerts with Spark Structured Streaming

The project generates sensor readings, calculates averages in sliding windows,
checks those averages against `alerts_conditions.csv`, and writes matching
alerts to Kafka.

## Files

- `create_topic.py` creates the input topic and two alert topics.
- `sensor.py` sends a JSON reading every five seconds.
- `process_sensors.py` reads the Kafka stream, applies a one-minute window
  sliding every 30 seconds with a 10-second watermark, checks the CSV rules,
  and writes alerts to the temperature or humidity topic.
- `consumer.py` prints messages from both alert topics.
- `alerts_conditions.csv` contains the alert rules.

The sensor JSON uses `id`, `timestamp`, `temperature`, and `humidity`.

## Requirements

- Kafka must be running and reachable at `127.0.0.1:9092`.
- Java 17 or newer (tested with Java 24 and PySpark 4.2.0).
- Install Python packages from this directory:

```powershell
python -m pip install -r requirements.txt
```

On the first start, `process_sensors.py` downloads the Spark Kafka connector
jars from Maven Central into `jars\` and adds them to the driver classpath.
The machine needs access to Maven Central for that first download.

## Windows setup

- Spark Streaming needs `winutils.exe` and `hadoop.dll` to write its
  checkpoint files on Windows. Put both files in `hadoop\bin` in this
  directory, for example from
  https://github.com/kontext-tech/winutils/tree/master/hadoop-3.4.0-win10-x64/bin
  and set `HADOOP_HOME` to that `hadoop` folder (`start.bat` does this).
- Run the processor with `python process_sensors.py`, not `spark-submit`.
  The pip version of `spark-submit` looks for `python3`, which Windows doesn't
  have.

## Run

You can start the project with `start.bat`. It creates/checks the topics,
opens the alert consumer and Spark processor in separate windows, then waits
for you to confirm Spark is ready before opening the sensor producer.
Run `start.bat 2` to open two sensor producers at the same time.

Alternatively, open separate terminals in this directory and start the scripts
in this order:

```powershell
python create_topic.py
```

```powershell
python consumer.py
```

```powershell
python process_sensors.py
```

```powershell
python sensor.py
```

Stop a running script with `Ctrl+C`. Start the consumer and Spark processor
before the sensor so they are ready to receive new data.

Spark stores its streaming offsets and state in `checkpoints/sensor_alerts`.
To make a fresh local run from the latest Kafka messages, stop Spark and remove
that checkpoint directory before restarting it. Do not remove it when you want
Spark to resume from its previous position.
