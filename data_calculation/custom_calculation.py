# On suppose que data_set est un DataFrame Pandas ou une structure de données similaire.

from configuration import application


def process_data1(data_set):
    print("Processing data 1")
    return data_set


def process_data2(data_set):
    print("Processing data 2")
    return data_set


def process_data3(data_set):
    print("Processing data 3")
    return data_set


def call_custom_function(data_set):
    calculations = application.load()["calculations"]

    for name in calculations:
        function_to_call = globals().get(name)
        if function_to_call:
            data_set = function_to_call(data_set)
        else:
            raise ValueError(f"No function named {name} found in this module")

    return data_set
