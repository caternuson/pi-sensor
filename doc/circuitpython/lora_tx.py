#--------------------------------------------------------------------
# Simple LoRa radio sensor value sender.
#
# carter nelson
# 2026/10/14
#--------------------------------------------------------------------
import time
from random import random

import board
import digitalio
import adafruit_rfm9x
import adafruit_bme680

# Radio setup
SENSOR_NODE = 2 # unique and != HOME_NODE or 0
HOME_NODE = 1   # node number for central radio
RADIO_FREQ_MHZ = 915.0
RADIO_TX_POWER = 23
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = board.SPI()
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = RADIO_TX_POWER
rfm9x.node = SENSOR_NODE
rfm9x.destination = HOME_NODE

# Sensor setup
i2c = board.I2C()
bme680 =  adafruit_bme680.Adafruit_BME680_I2C(i2c)

def make_json(sensor, value):
    return f'{{"sensor":"{sensor}","value":{value}}}'

def send_data(sensor, value):
    print(f"{sensor} = {value}")
    data = make_json(sensor, value)
    attempts = 0
    while attempts < 5:
        if not rfm9x.send_with_ack(data):
            attempts += 1
            wait_time = 0.01 * (1 + random())
            print(f"NACKd retry {attempts} in {wait_time}s...")
            time.sleep(wait_time)
        else:
            break

print("looping...")
while True:
    print("reading sensor...")
    bme680_pressure = bme680.pressure
    bme680_temperature = bme680.temperature
    bme680_humidity = bme680.relative_humidity
    bme680_gas = bme680.gas

    print("sending...")
    send_data("upstairs_bme680_pressure", bme680_pressure)
    send_data("upstairs_bme680_temperature", bme680_temperature)
    send_data("upstairs_bme680_relative_humidity", bme680_humidity)
    send_data("upstairs_bme680_gas", bme680_gas)

    print("sleeping...")
    time.sleep(60)