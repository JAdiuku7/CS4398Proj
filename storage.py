import json
import os

FILE_PATH = "data/workouts.json"


def load_data():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except:
            return []


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
