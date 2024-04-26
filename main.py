# main.py
import argparse
import os
from tqdm import tqdm


from data_calculation.custom_calculation import call_custom_function
from data_extraction.prepare_data import (
    compute_anual_value,
    compute_dividend,
    compute_sector,
    create_basic_structure,
)
from configuration import application
from data_manipulation.data_loader import load_pickle
from data_manipulation.data_saver import (
    save_to_json,
    save_to_pickle,
)
from data_resource.nasdaqtrader import get_stocklists, read_symbols
from data_resource.worldbank import fetch_data, fetch_indicators, fetch_regions
from data_resource.yahoo import get_historical, get_symbol_resume


def export_data():
    #
    # Export data from nasdaqtrader, yahoo, worldbank
    #
    get_stocklists()
    get_symbol_resume(read_symbols())
    get_historical()
    fetch_indicators()
    fetch_regions()


def prepare_data():
    #
    # Prepare data_set
    #
    data_set = create_basic_structure()
    data_set = compute_sector(data_set)
    data_set = compute_anual_value(data_set)
    data_set = compute_dividend(data_set)
    data_set = fetch_data(data_set)
    save_data(data_set)


def calculate_data():
    #
    # Call custom function
    #
    data_set = load_data()
    call_custom_function(data_set)
    save_data(data_set)


def save_data(data_set):
    save_to_json(data_set, application.load()["data_base_path"].format("data_set.json"))
    save_to_pickle(
        data_set, application.load()["data_base_path"].format("data_set.pkl")
    )


def load_data():
    return load_pickle(application.load()["data_base_path"].format("data_set_save.pkl"))


def main():
    os.system("cls" if os.name == "nt" else "clear")

    parser = argparse.ArgumentParser(
        description="Run parts of the script based on command line arguments."
    )
    parser.add_argument(
        "--export", action="store_true", help="Export data from external sources"
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare base data set from external sources",
    )
    parser.add_argument(
        "--calculate",
        action="store_true",
        help="Calculate additional data from base data set with your custom functions",
    )
    args = parser.parse_args()

    if args.export:
        export_data()

    if args.prepare:
        prepare_data()

    if args.calculate:
        calculate_data()


if __name__ == "__main__":
    main()
