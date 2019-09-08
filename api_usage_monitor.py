"""
@author: NishantParmar
@description: Monitors API usage count, updating the count in a JSON file.
"""

import json
import util

day_key = util.get_current_date()


def write_to_file(file_path, json_obj):
    """Writes a beautified Python object to a JSON file
    Keyword arguments:
        file_path - string of the path of the destination
        json_obj - object to be stored as JSON to the file
    """
    with open(file_path, 'w') as file:
        file.write(json.dumps(json_obj, indent=4, sort_keys=True))


def get_usage_object(file_path):
    """Returns the usage count object of the CSE library - maintained on the
    basis of usage
    Keyword arguments:
        file_path - string of the path of the usage (JSON) file
    """
    usage_count = {}
    try:
        with open(file_path) as count_file:
            usage_count = json.load(count_file)
    except FileNotFoundError:
        usage_count = {day_key: 1}
    except json.JSONDecodeError:
        usage_count = {day_key: 0}
    
    return usage_count


def save_usage_count(usage_count, file_path):
    usage_object = {day_key: usage_count}
    with open(file_path, "w") as count_file:
        json.dump(usage_object, count_file)


def get_usage_count(file_path):
    """Returns the usage count of the CSE library - maintained on the basis of 
    usage
    Keyword arguments:
        file_path - string of the path of the usage (JSON) file
    """
    usage_count = get_usage_object(file_path)
    if usage_count:
        util.write_print_logs("usage_count = {}".format(
                str(usage_count)))
        if day_key in usage_count:
            return usage_count[day_key]
        else:
            return 0


def update_usage_count(file_path):
    """Updates and writes the usage count of the CSE library
    Keyword arguments:
        file_path - string of the path of the usage (JSON) file
    """
    try:
        with open(file_path) as count_file:
            usage_count = json.load(count_file)
            if usage_count:
                util.write_print_logs("usage_count = {}".format(
                        str(usage_count)))
                if day_key in usage_count:
                    usage_count[day_key] += 1
                else:
                    usage_count = {day_key: 1}
                write_to_file(file_path, usage_count)
    except FileNotFoundError:
        usage_count = {day_key: 1}
        write_to_file(file_path, usage_count)
