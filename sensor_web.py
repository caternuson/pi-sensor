import os
from datetime import datetime, timedelta
import sqlite3
import json
import asyncio
import tornado

DB_NAME = "sensor_data.db"      # the DB file

ONE_DAY = timedelta(days=1)

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("data_plotter.html")

    # def post(self):
    #     sensor = self.request.body.decode('utf-8')
    #     conn = sqlite3.connect(DB_NAME)
    #     cursor = conn.cursor()
    #     data = [ [row[0], row[1]] for row in cursor.execute(f"SELECT timestamp, value FROM {sensor}") ]
    #     self.write(json.dumps(data))
    #     conn.close()

    def post(self):
        data_request = json.loads(self.request.body)
        #print(data_request)
        sensor = data_request["sensor"]
        date1 = datetime.fromisoformat(data_request["date"])
        date2 = date1 + ONE_DAY
        #print(sensor, date1, date2)
        start = date1.strftime("%Y-%m-%d")
        end = date2.strftime("%Y-%m-%d")
        #print(start, end)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        SQL = f"SELECT * FROM {sensor} WHERE timestamp >= DATE('{start}') AND timestamp < DATE('{end}')"
        #print(SQL)
        data = [ [row[0], row[1]] for row in cursor.execute(SQL) ]
        #print(data)
        self.write(json.dumps(data))
        conn.close()

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