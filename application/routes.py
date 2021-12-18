from flask import request, render_template, Blueprint
from main import *
from main import get_latest_data

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/")
def index():
    return render_template("index.html", bar=get_latest_data())


@page.route("/temp", methods=["POST"])
def temp_change():
    pass


@page.route("/plot", methods=["GET, POST"])
def plot():
    # this changes requested temperature in engine

    return render_template("subpage.html", bar="data")
    # this returns template
    # additionally returns json with some data to chart as beginning
    # (from midnight?)
    # also returns how much time left for the heat up
    # 


@page.route("/plot/more", methods=["GET"])
def more():
    how_much = request.args.get("count")
    return get_some_data(how_much)
    # this returns some more data in json
    # request to be made with /plot/more?count=<number, like 123> for example
    # http://127.0.0.1:5000/plot/more?count=11
