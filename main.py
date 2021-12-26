from multiprocessing import Process, Queue
from flask import Flask
from application.routes import *
from engine import Room, Engine

app = Flask(__name__)

if __name__ == "__main__":
    room = Room()
    engine = Engine()
    q = Queue()
    p1 = Process(target=Engine.worker, args=(engine, q, room))
    p1.start()

    app.config.update(queue=q)
    app.register_blueprint(page)
    # print(app.url_map)
    app.run()
