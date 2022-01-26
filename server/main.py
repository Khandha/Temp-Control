from multiprocessing import Process, Queue
from flask import Flask
from routes import *
from engine import Engine
from room import Room

app = Flask(__name__)

if __name__ == "__main__":
    try:
        room = Room()
        engine = Engine()
        q = Queue()
        p1 = Process(target=Engine.worker, args=(engine, q, room))
        p1.start()

        app.config.update(queue=q)
        app.register_blueprint(page)
        # print(app.url_map)
        app.run()
    except KeyboardInterrupt as interrupt:
        print("Program interrupted with keyboard stop signal")
        quit()
# TODO: make reaction faster.