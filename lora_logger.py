#--------------------------------------------------------------------
# Simple LoRa radio to SQLite bridge for logging sensor values.
#
# carter nelson
# 2026/10/11
#--------------------------------------------------------------------

import time
import json
import sqlite3

import board
from digitalio import DigitalInOut
import adafruit_rfm9x

DB_NAME = "sensor_data.db"      # the DB file

# Radio setup
RADIO_FREQ_MHZ = 915.0
HOME_NODE = 1
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = board.SPI()
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.node = HOME_NODE

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

#===================
# M A I N
#===================
if __name__ == "__main__":
    print("looping...")
    while True:
        packet = rfm9x.receive(with_ack=True)
        if packet is not None:
            try:
                json_data = json.loads(packet.decode("utf-8"))
                sensor = json_data.get('sensor')
                value = float(json_data.get('value'))
                print(f"{sensor} = {value}")
                add_sensor_value(sensor, value)
            except sqlite3.OperationalError as e:
                print(f"adding new table: {sensor}")
                add_table(sensor)
                add_sensor_value(sensor, value)
            except Exception as e:
                print(f"Oops!!! {e}")
