import os
import pathlib
import random
import time
from datetime import datetime

import config
from DriverSingleton import DriverSingleton
from selenium.webdriver.support import expected_conditions as EC


def getDelayElement(by, key, visible=False):
    return DriverSingleton.get_wait().until(EC.visibility_of_element_located((by, key))) if visible else (
        DriverSingleton.get_wait().until(EC.presence_of_element_located((by, key))))


def randomSleep(second):
    sleep_time = random.uniform(1, second)
    time.sleep(sleep_time)


def rename(old_file_new, new_file_name):
    suffix = get_suffix(old_file_new)
    location = config.get_location()
    new_file_name = new_file_name + suffix
    os.rename(os.path.join(location, old_file_new), os.path.join(location, new_file_name))


def parse_date(date, old_format, new_format):
    format_date = datetime.strptime(date, old_format)
    return format_date.strftime(new_format)


def get_suffix(old_file_new):
    return pathlib.Path(old_file_new).suffix


