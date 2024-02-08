import json

setting = None


def parse_setting():
    global setting
    if setting is None:
        with open('./config.json', 'r') as file:
            setting = json.load(file)
            return setting
    return setting


def get_location():
    return parse_setting()['location']


def get_out_date():
    return parse_setting()['out_date']


def get_max_count():
    return parse_setting()['max_count']
