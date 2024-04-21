import sys
from tqdm import tqdm
from configuration import application
from data_manipulation.data_loader import list_files_without_extensions, load_json


def create_basic_structure():
    symbol_path = "raw/symbol"
    data_base_path = application.load()["data_base_path"]
    list_symb = list_files_without_extensions(data_base_path.format(symbol_path))
    list_symb.sort()
    return {"actions": list_symb, "config": {}}


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
            pbar.set_description(f"Sector for {action.ljust(6)}:")

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
