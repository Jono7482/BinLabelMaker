import json
import Settings
import os


def generate_labels_json():
    if not os.path.isfile('Labels.json'):
        a_list = Settings.LABELS
        with open("Labels.json", "w") as fp:
            json.dump(a_list, fp, indent=4)


def generate_settings_json():
    if not os.path.isfile('Settings.json'):
        a_list = Settings.SETTINGS
        with open("Settings.json", "w") as fp:
            json.dump(a_list, fp, indent=4)


def get_labels():
    with open("Labels.json", "r") as fp:
        _file = json.load(fp)
    return _file


def get_settings():
    with open("Settings.json", "r") as fp:
        _file = json.load(fp)
    return _file


def print_json_object(json_list):
    print(json.dumps(json_list, indent=4))
