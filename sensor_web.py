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
        sensor = self.request.body.decode('utf-8')
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        data = [ [row[0], row[1]] for row in cursor.execute(f"SELECT timestamp, value FROM {sensor}") ]
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