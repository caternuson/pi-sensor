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

def add_sensor_value(sensor, value):
    """Add sensor value"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute(f"INSERT INTO {sensor} (value) VALUES ({value})")
    conn.commit()
    conn.close()

def add_table(sensor):
    """Add new table"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute(f"""
        CREATE TABLE {sensor} (
            timestamp DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
            value FLOAT
        )
    """)
    conn.commit()
    conn.close()

def on_message(client, userdata, message):
    """Parse the MQTT message and save to DB."""
    try:
        sensor = message.topic.lstrip(MQTT_TOPIC[:-1])
        value = float(message.payload)
        print(f"{sensor} = {value}")
        add_sensor_value(sensor, value)
    except sqlite3.OperationalError as e:
        print(f"adding new table: {sensor}")
        add_table(sensor)
        add_sensor_value(sensor, value)
    except Exception as e:
        print(f"oops on_message: {e}")

#===================
# M A I N
#===================
if __name__ == "__main__":
    print("MQTT setup...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message

    print("Connecting...")
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)

    print("Listening...FOREVER!!!!!")
    client.loop_forever()

