from flask import Blueprint, render_template, request
from .db import get_db
import pickle
import json

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/")
def index():
    db = get_db()
    fighters = db.execute("SELECT * FROM fighters").fetchall()
    fighters = [
        dict(fighter) for fighter in fighters
    ]  # Convert Row objects to dictionaries
    return render_template("home/index.html", fighters=fighters)


@bp.route("/predict", methods=["GET"])
def predict():
    model = pickle.load(open("app/static/model/ufc_ui_model.pkl", "rb"))
    red_fighter = request.args.get("redFighter")
    blue_fighter = request.args.get("blueFighter")

    # Convert JSON strings to dictionaries
    red_fighter = json.loads(red_fighter)
    blue_fighter = json.loads(blue_fighter)
    ageDiff = blue_fighter["age"] - red_fighter["age"]
    heightDiff = blue_fighter["height"] - red_fighter["height"]
    reachDiff = blue_fighter["reach"] - red_fighter["reach"]
    winsDiff = blue_fighter["wins"] - red_fighter["wins"]
    lossesDiff = blue_fighter["losses"] - red_fighter["losses"]
    currentwinstreakDiff = (
        blue_fighter["currentwinstreak"] - red_fighter["currentwinstreak"]
    )
    currentlosestreakDiff = (
        blue_fighter["currentlosestreak"] - red_fighter["currentlosestreak"]
    )
    longestwinstreakDiff = (
        blue_fighter["longestwinstreak"] - red_fighter["longestwinstreak"]
    )
    # blue - red
    # 1 for red, 0 for  blue
    features = [
        [
            ageDiff,
            heightDiff,
            reachDiff,
            winsDiff,
            lossesDiff,
            currentwinstreakDiff,
            currentlosestreakDiff,
            longestwinstreakDiff,
        ]
    ]
    result = model.predict(features)
    return json.dumps({"result": int(result[0])})
