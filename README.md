# pi-sensor
Raspberry Pi based sensor data logger and web viewer.

# Overview
Sensor data logging is done via MQTT and/or LoRa. Sensor data plotting
is done via chart.js with Tornado as the web server.

# Dependencies
* These are included in the repo:
  * [jQuery](https://jquery.com/)
  * [Chart.js](https://www.chartjs.org/)
  * [date-fns](https://date-fns.org/)
  * [chartjs-adapter-date-fns](https://github.com/chartjs/chartjs-adapter-date-fns)
* Python libs to install into a venv:
  * [Tornado Web Server](https://pypi.org/project/tornado/)
* MQTT logging support requires:
  * [Eclipse Mosquitto](https://mosquitto.org/)
  * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* LoRa logging support requires:
  * [Blinka](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
  * [adafruit-circuitpython-rfm9x](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html) is used, but is part of Python standard library

# MQTT Setup
This option generally requires no additional hardware.
## Mosquitto Server
Install system packages:
```
sudo apt install mosquitto mosquitto-clients
```
Edit `/etc/mosquitto/mosquitto.conf` to allow external access (add to bottom):
```
listener 1883 0.0.0.0
allow_anonymous true
```
Restart service:
```
sudo systemctl restart mosquitto
```

## Python
With venv active:
```
pip install paho-mqtt
```

# LoRa Setup
Enable SPI via raspi-config or some other means. A suitable LoRa radio
module is expected to be connected to SPI.
## Blinka
Create a venv, activate it, and manual install:
```
pip install adafruit-blinka
```
## Python
With the Blinka venv active:
```
pip install adafruit-circuitpython-rfm9x
```

# systemd
Systemd unit files that can be placed in `/etc/systemd/system`.
## Logger
`/etc/systemd/system/lora-logger.service`
```
[Unit]
Description=LoRa Logger

[Service]
ExecStart=/home/pi/blinka/bin/python3 /home/pi/pi-sensor/lora_logger.py

[Install]
WantedBy=multi-user.target
```
## Web Server
`/etc/systemd/system/sensor-web.service`
```
[Unit]
Description=Pi Sensor Web Server

[Service]
ExecStart=/home/pi/blinka/bin/python3 /home/pi/pi-sensor/sensor_web.py

[Install]
WantedBy=multi-user.target
```
