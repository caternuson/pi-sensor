# pi-sensor
Raspberry Pi based sensor data logger and web viewer.

# Overview
Sensor data logging is done via MQTT. Sensor data plotting is done via chart.js
with Tornado as the web server.

# Dependencies
* [Eclipse Mosquitto](https://mosquitto.org/)
* These are included in the repo:
  * [jQuery](https://jquery.com/)
  * [Chart.js](https://www.chartjs.org/)
  * [date-fns](https://date-fns.org/)
  * [chartjs-adapter-date-fns](https://github.com/chartjs/chartjs-adapter-date-fns)
* These are needed in the Python venv:
  * [Tornado Web Server](https://pypi.org/project/tornado/)
  * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html) is used, but is part of Python standard library

# Mosquitto Setup
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

# Python Setup
Create a venv and install deps:
```
pip install tornado
pip install paho-mqtt
```
