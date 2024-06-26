import json
import os
from functions.array import append

_DATA_PATH = "./data/db.json"
_DATA_DIR_PATH = "./data"
_EMPTY_DB = {'places': [], 'enquiries': [], 'bookings': []}


def _test_storage():
    # db.json file issues can cause entire program to crash, try rectifying issues before program starts
    # try reading and writing from the file, if it fails then file is corrupt
    # delete old file and write new one if the user wants to
    try:
        _dump_data(_load_db())
        return True  # if successful
    except (PermissionError, FileNotFoundError, json.JSONDecodeError) as e:
        print("DATABASE FILE IS CORRUPT!!!")
        user_input = ""
        while user_input.lower() != "y" and user_input.lower() != "n":
            user_input = input("**tip:choose N to see json error message**\nDo you want to clear program cache? (Y/N)\n")

        if user_input.lower() == "y":
            os.remove(_DATA_PATH)
            init_db()
            print("Please run the program again.")
        else:
            print(f"JSON ERROR: {e}")

        quit()


def init_db():
    # creates a db.json file and dir if it doesn't already exist

    if not os.path.exists(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    if not os.path.isfile(_DATA_PATH):
        with open(_DATA_PATH, 'w') as file:
            # Dump the data into the new JSON file
            json.dump(_EMPTY_DB, file, indent=2)
    else:
        # if database already exists then check for errors before program starts
        _test_storage()


def _load_db():
    # loads up the entire db file
    with open(_DATA_PATH, 'r') as file:
        data = json.load(file)
        return data


def _dump_data(new_data):
    # writes an entire db file
    with open(_DATA_PATH, 'w') as file:
        json.dump(new_data, file, indent=2)


def save_data(data, dict_name):
    # Open the JSON file for writing
    new_data = _load_db()  # gets json data
    new_data[dict_name] = append(new_data[dict_name], data)
    _dump_data(new_data)  # adds modified data back to json file


def load_data(dict_name):
    # loads up arrays contained within given dict_name
    new_data = _load_db()  # gets json data
    return new_data[dict_name]


def update_data(dict_name, key, value, new_data):
    # dict_name is the name of the dictionary data is stored in e.g. 'places'
    # key is the key of the dictionary item to be updated
    # value is the value of the dictionary item to be updated

    # so 'update_data' with 'new_data' in 'dict_name' where 'key' is 'value'
    remove_data(dict_name, key, value)
    save_data(new_data, dict_name)


def remove_data(dict_name, key, value):
    # dict_name is the name of the dictionary data is stored in e.g. 'places'
    # key is the key of the dictionary item to be removed
    # value is the value of the dictionary item to be removed

    # so remove_data from dict_name where key is {key} and value is {value} like sql

    # Open the JSON file for writing
    new_data = _load_db()

    # new_data[dict_name].remove(data)
    # region USING LOW QUALITY CODE TO REMOVE DATA FROM AN EXISTING ARRAY INSTEAD OF 'remove()' AS IT IS A BUILT-IN FUNC
    # creates an array that can be 1 length smaller than array loaded frm db and adds all the items from the db array excluding the item parsed by user
    new_data_array = [None] * (len(new_data[dict_name]))
    current_index = 0
    new_array_size = 0
    for i in new_data[dict_name]:
        # creates a new array and adds all the items from the old array to the new one except the item that is to be deleted
        if i[key] != value:  # if current value matches provide val, add to new array
            new_array_size += 1
            new_data_array[current_index] = i
            current_index += 1

    # sets the old array size to be length of remaining items, then adds each item back to the old array (can not use dynamically sized array as it is built in function)
    new_data[dict_name] = [None] * new_array_size
    # adds the data back one by one
    for i in range(0, new_array_size):
        new_data[dict_name][i] = new_data_array[i]
    # endregion

    _dump_data(new_data)  # adds it back to json file
