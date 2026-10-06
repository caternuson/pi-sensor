#--------------------------------------------------------------------
# Webserver for plotting sensor data.
#
# carter nelson
# 2026/10/06
#--------------------------------------------------------------------

import os
import sqlite3
import json
import asyncio
import tornado

DB_NAME = "sensor_data.db"      # the DB file

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("data_plotter.html")

    def post(self):
        request_info = json.loads(self.request.body)
        sensor = request_info["sensor"]
        date = request_info["date"]
        SQL = f"SELECT * FROM {sensor} WHERE timestamp BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'"
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        data = [ [row[0], row[1]] for row in cursor.execute(SQL) ]
        conn.close()
        self.write(json.dumps(data))

async def main():
    handlers = [
        (r"/", MainHandler),
    ]
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    app = tornado.web.Application(handlers, **settings)
    app.listen(8888)
    print("Server started.")
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    asyncio.run(main())