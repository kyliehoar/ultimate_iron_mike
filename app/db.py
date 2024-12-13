import csv
import os
import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    # Path to the CSV file
    csv_path = os.path.join(
        current_app.root_path, "static", "model", "Cleaned UFC Master Dataset.csv"
    )

    # Load existing fighter names into a set
    existing_fighters = set(
        row["name"] for row in db.execute("SELECT name FROM fighters").fetchall()
    )

    fighters_to_insert = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            red_name = row["RedFighter"]
            if red_name not in existing_fighters:
                age = row["RedAge"]
                height = row["RedHeightCms"]
                weight = row["RedWeightLbs"]
                reach = row["RedReachCms"]
                wins = row["RedWins"]
                losses = row["RedLosses"]
                currentwinstreak = row["RedCurrentWinStreak"]
                currentlosestreak = row["RedCurrentLoseStreak"]
                longestwinstreak = row["RedLongestWinStreak"]
                fighters_to_insert.append(
                    (
                        red_name,
                        age,
                        height,
                        weight,
                        reach,
                        wins,
                        losses,
                        currentwinstreak,
                        currentlosestreak,
                        longestwinstreak,
                    )
                )
                existing_fighters.add(red_name)
            blue_name = row["BlueFighter"]
            if blue_name not in existing_fighters:
                age = row["BlueAge"]
                height = row["BlueHeightCms"]
                weight = row["BlueWeightLbs"]
                reach = row["BlueReachCms"]
                wins = row["BlueWins"]
                losses = row["BlueLosses"]
                currentwinstreak = row["BlueCurrentWinStreak"]
                currentlosestreak = row["BlueCurrentLoseStreak"]
                longestwinstreak = row["BlueLongestWinStreak"]
                fighters_to_insert.append(
                    (
                        blue_name,
                        age,
                        height,
                        weight,
                        reach,
                        wins,
                        losses,
                        currentwinstreak,
                        currentlosestreak,
                        longestwinstreak,
                    )
                )
                existing_fighters.add(blue_name)

    if fighters_to_insert:
        db.executemany(
            "INSERT INTO fighters (name, age, height, weight, reach, wins, losses, currentwinstreak, currentlosestreak, longestwinstreak) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            fighters_to_insert,
        )
        db.commit()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
