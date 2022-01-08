import queue

from flask import request, Blueprint, current_app as app
from flask_cors import cross_origin
import helpers
from engine import Engine
from room import Room
from helpers import get_latest_data, get_some_data, set_new_temperature
from multiprocessing import Queue, Process
import datetime

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/")
@cross_origin()
def index():
    return ""


# to check: curl -X POST http://127.0.0.1:5000/settemp?temp=17
@page.route("/settemp", methods=["POST"])
@cross_origin()
def temp_change():
    try:
        new_temp = float(request.args.get("temp"))
        if new_temp is None:
            return {"errorMessage": "no temperature set"}
        set_new_temperature(app.config['queue'], new_temp)
        return {"set-temperature": new_temp}
    except queue.Empty or queue.Full:
        print("queue push failed")
        return {"errorMessage": "no temperature set"}
    except NameError:
        print("temperature setting failed")
        return {"errorMessage": "no temperature set"}


# this returns last row of data in json
# GET request to be made with http://127.0.0.1:5000/data
@page.route("/data", methods=["GET"])
@cross_origin()
def get_data():
    return get_latest_data()


# this returns some more data in json
# request to be made with /plot/more?count=<number, like 123> for example
# http://127.0.0.1:5000/data/more?count=11
@page.route("/data/more", methods=["GET"])
@cross_origin()
def more():
    try:
        how_much = request.args.get("count")
        how_much = helpers.limit(int(how_much), 1, 50)
        return get_some_data(how_much)
    except NameError:
        print("fetching data failed")
        return {"errorMessage": "fetching data failed"}


# example call:
# curl -X GET "http://127.0.0.1:5000/estimate?current_temp=19&set_temp=23"
# returns amount of time until temperature reached
@page.route("/estimate", methods=["GET"])
@cross_origin()
def estimate():
    try:
        current_temp = request.args.get("current_temp")
        set_temp = request.args.get("set_temp")
        engine = Engine()
        room = Room(float(current_temp), float(set_temp))
        new_queue = Queue()

        p = Process(target=Engine.time_prediction, args=(engine, room, new_queue))
        p.start()
        p.join()
        ret_value = new_queue.get()
        return {"time-estimate": str(datetime.timedelta(seconds=ret_value))}
    except Exception:
        print("exception on estimate call")
        return {"errorMessage": "estimating data failed"}


@page.errorhandler(ValueError)
def val_error(err):
    print("temperature not a float")
    return {"errorMessage": "not_float"}
