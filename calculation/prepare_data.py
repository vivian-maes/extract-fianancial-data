import sys
import os
from tqdm import tqdm
from configuration import application
from data_manipulation.data_loader import (
    list_files_without_extensions,
    load_csv,
    load_json,
)

"""
Computes the sector information for the given data set.

Args:
    data_set (dict): A dictionary containing the actions and configuration.

Returns:
    dict: The updated data set with the sector information added.
"""


def create_basic_structure():
    symbol_path = "raw/symbol"
    data_base_path = application.load()["data_base_path"]
    list_symb = list_files_without_extensions(data_base_path.format(symbol_path))
    list_symb.sort()
    return {"actions": list_symb, "config": {}}


"""
Computes the sector information for each action in the given data set.

Args:
    data_set (dict): A dictionary containing the actions and other data.

Returns:
    dict: The updated data_set dictionary with the sector information added.
"""


def compute_sector(data_set):
    symbol_path = "raw/symbol/{}.json"
    data_base_path = application.load()["data_base_path"]

    sector = []
    sector_config = {}
    currrent_global_indx = 0

    with tqdm(
        total=len(data_set["actions"]), desc="Compute sector", file=sys.stdout
    ) as pbar:
        for action in data_set["actions"]:
            pbar.set_description(f"Sector for {action.ljust(6)}")

            action_info = load_json(data_base_path.format(symbol_path.format(action)))

            if "industry" in action_info.keys():
                sector_name = action_info["industry"]
            elif "category" in action_info.keys():
                sector_name = action_info["category"]
            elif "quoteType" in action_info.keys():
                sector_name = action_info["quoteType"]
            else:
                sector_name = "unknown"

            if sector_name in sector_config.values():
                current_index = [
                    key for key, value in sector_config.items() if value == sector_name
                ][0]
            else:
                current_index = currrent_global_indx
                sector_config[current_index] = sector_name
                currrent_global_indx += 1

            sector.append(current_index)
            pbar.update(1)

    data_set["sector"] = sector
    data_set["config"]["sector"] = sector_config

    return data_set


def compute_anual_value(data_set):
    symbol_path = "raw/history/{}.csv"
    data_base_path = application.load()["data_base_path"]

    low_global_year = None
    hight_global_year = None

    actions_quote_temp = []
    actions_quote = []

    with tqdm(
        total=len(data_set["actions"]), desc="Compute quote", file=sys.stdout
    ) as pbar:
        for action in data_set["actions"]:
            pbar.set_description(f"Quote for  {action.ljust(6)}")
            histories = load_csv(
                data_base_path.format(symbol_path.format(action)), date_fields=["Date"]
            )

            # init variable for current action
            current_year = None
            current_value = 0.0
            count_tick = 0
            low_action_year = None
            hight_action_year = None
            quotes = []

            # loop for all history quotations
            for _, history in histories.iterrows():
                year = history["Date"].year
                if current_year != year:
                    # Store price in quotes array
                    if current_year is not None:
                        price = round(current_value / count_tick, 6)
                        quotes.append(price)

                    # Reset pour la nouvelle année
                    # save lowest or highest year
                    if low_global_year == None or year < low_global_year:
                        low_global_year = year
                    if hight_global_year == None or year > hight_global_year:
                        hight_global_year = year
                    # save lowest or highest year action specific
                    if low_action_year == None or year < low_action_year:
                        low_action_year = year
                    if hight_action_year == None or year > hight_action_year:
                        hight_action_year = year

                    current_year = year
                    current_value = history["Close"]
                    count_tick = 1
                else:
                    # Ajouter à la valeur pour l'année en cours
                    current_value += history["Close"]
                    count_tick += 1

            # Après la fin de la boucle, traitez la dernière année
            if current_year is not None and count_tick > 0:
                price = round(current_value / count_tick, 6)
                quotes.append(price)

            # Save quotes for current action
            actions_quote_temp.append(
                {
                    "low_year": low_action_year,
                    "hight_year": hight_action_year,
                    "quotes": quotes,
                }
            )
            pbar.update(1)

    with tqdm(
        total=len(data_set["actions"]), desc="Padding quote    ", file=sys.stdout
    ) as pbar:
        # Remplisage des valeur inconue
        for action_quote in actions_quote_temp:
            low_year = action_quote["low_year"]
            hight_year = action_quote["hight_year"]
            quotes = action_quote["quotes"]

            if low_year == None:
                low_year = hight_global_year + 1
                hight_year = hight_global_year

            low_miss = low_year - low_global_year - 1
            hight_miss = hight_global_year - hight_year

            if low_miss > 0:
                liste_min_zeros = [0.0 for _ in range(low_miss)]
            else:
                liste_min_zeros = []

            if hight_miss > 0:
                liste_max_zeros = [0.0 for _ in range(hight_miss)]
            else:
                liste_max_zeros = []

            actions_quote.append(liste_min_zeros + quotes + liste_max_zeros)
            pbar.update(1)

    data_set["quotes"] = actions_quote
    data_set["config"]["date_quote"] = {
        "start_year": low_global_year,
        "end_year": hight_global_year,
    }
    return data_set


"""
Computes the dividends for the actions in the given data set.

Args:
    data_set (dict): A dictionary containing the data set information, including the actions and configuration.

Returns:
    dict: The updated data set with the computed dividends.
"""


def compute_dividend(data_set):
    symbol_path = "raw/dividend/{}.csv"
    data_base_path = application.load()["data_base_path"]

    start_year = data_set["config"]["date_quote"]["start_year"]
    end_year = data_set["config"]["date_quote"]["end_year"]

    actions_dividends = []

    with tqdm(
        total=len(data_set["actions"]), desc="Compute dividends", file=sys.stdout
    ) as pbar:

        for action in data_set["actions"]:
            dividends = []
            currrent_dividend = 0
            current_year = None
            break_year = None

            pbar.set_description(f"Divid for  {action.ljust(6)}")

            file_path = data_base_path.format(symbol_path.format(action))
            if os.path.exists(file_path):
                try:
                    hist_dividends = load_csv(file_path, date_fields=["Date"])

                    if hist_dividends.empty:
                        delta = end_year - start_year
                        dividends = [0.0 for _ in range(delta)]
                    else:

                        for _, hist in hist_dividends.iterrows():
                            current_year = hist["Date"].year
                            if current_year != break_year:
                                if break_year == None:
                                    missing_year = current_year - start_year - 1
                                    if missing_year > 0:
                                        dividends += [0.0 for _ in range(missing_year)]
                                else:
                                    missing_year = current_year - break_year - 1
                                    if missing_year > 0:
                                        dividends += [0.0 for _ in range(missing_year)]
                                    dividends.append(currrent_dividend)

                                break_year = current_year
                                currrent_dividend = hist["Dividends"]

                            else:
                                currrent_dividend += hist["Dividends"]

                        # store last year
                        dividends.append(currrent_dividend)
                        missing_year = end_year - current_year
                        if missing_year > 0:
                            dividends += [0.0 for _ in range(missing_year)]
                except Exception as _:
                    delta = end_year - start_year
                    dividends = [0.0 for _ in range(delta)]
            else:
                delta = end_year - start_year
                dividends = [0.0 for _ in range(delta)]

            actions_dividends.append(dividends)
            pbar.update(1)

    data_set["dividends"] = actions_dividends
    return data_set
