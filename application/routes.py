from flask import request, render_template, Blueprint, current_app as app

from engine import Engine, Room
from helpers import get_latest_data, get_some_data, set_new_temperature
from multiprocessing import current_process, Queue, Process
import datetime

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/")
def index():
    return render_template("index.html", bar=get_latest_data())


@page.route("/temp", methods=["POST"])
def temp_change():
    new_temp = request.args.get("temp")
    try:
        if new_temp is None:
            return {"errorMessage": "no temperature set"}
    except NameError:
        print("temperature setting failed")
    set_new_temperature(app.config['queue'], new_temp)
    return {"set-temperature": new_temp}
    #  to check: curl -X POST http://127.0.0.1:5000/temp?temp=17


@page.route("/plot", methods=["GET, POST"])
def plot():
    # this changes requested temperature in engine

    return render_template("subpage.html", bar="data")
    # this will return template
    # additionally json with some data to chart as beginning
    # (from midnight?)
    # also returns how much time left for the heat up
    # TODO


@page.route("/plot/more", methods=["GET"])
def more():
    how_much = request.args.get("count")
    return get_some_data(how_much)
    # this returns some more data in json
    # request to be made with /plot/more?count=<number, like 123> for example
    # http://127.0.0.1:5000/plot/more?count=11


@page.route("/estimate", methods=["GET"])
def estimate():
    current_temp = request.args.get("current_temp")
    set_temp = request.args.get("set_temp")
    print(current_temp)
    print(set_temp)
    engine = Engine()
    room = Room(float(current_temp), float(set_temp))
    ret_value = 0
    queue = Queue()

    p = Process(target=Engine.time_prediction, args=(engine, room, queue))
    p.start()
    p.join()
    ret_value = queue.get()
    print(str(datetime.timedelta(seconds=ret_value)))
    return render_template("subpage.html", bar=(str(datetime.timedelta(seconds=ret_value))))
    # this will return template
    # additionally json with some data to chart as beginning
    # (from midnight?)
    # also returns how much time left for the heat up
    # TODO
