#--------------------------------------------------------------------
# Simple MQTT to SQLite bridge for logging sensor values.
#
# carter nelson
# 2026/10/01
#--------------------------------------------------------------------

import sqlite3
import paho.mqtt.client as mqtt

DB_NAME = "sensor_data.db"      # the DB file
MQTT_BROKER = "localhost"       # the MQTT server is running locally
MQTT_TOPIC = "home/sensors/#"   # subscribe to anything under this topic

def init_db():
    """Create the DB if it does not already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
            sensor TEXT,
            value FLOAT
        )
    ''')
    conn.commit()
    conn.close()

def on_message(client, userdata, message):
    """Parse the MQTT message and save to DB."""
    try:
        print(message.topic)

        # strip out the sensor name
        sensor = message.topic.lstrip(MQTT_TOPIC[:-1])

        # sensor value
        value = float(message.payload)

        print(f"{sensor} = {value}")

        # add to DB
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO readings (sensor, value) VALUES (?, ?)",
            (sensor, value)
        )
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"oops on_message: {e}")

#===================
# M A I N
#===================
if __name__ == "__main__":
    print("DB setup...")
    init_db()

    print("MQTT setup...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message

    print("Connecting...")
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)

    print("Listening...FOREVER!!!!!")
    client.loop_forever()

