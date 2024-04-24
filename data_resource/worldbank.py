import sys
import requests
from tqdm import tqdm

from configuration import application
from data_manipulation.data_saver import save_to_json


def fetch_indicators():
    destination_path = "raw/indicator/indicator_list.json"
    data_base_path = application.load()["data_base_path"]

    base_url = "http://api.worldbank.org/v2/indicator?format=json"
    current_page = 1
    total_pages = 1

    indicators = []

    response = requests.get(base_url)
    if response.status_code == 200:
        total_pages: int = response.json()[0]["pages"]

        with tqdm(total=total_pages, desc="Read indicator", file=sys.stdout) as pbar:
            while current_page <= total_pages:
                url = f"{base_url}&page={current_page}"
                response = requests.get(url)
                data = response.json()
                total_pages = data[0]["pages"]
                indicators += data[1]
                current_page += 1
                pbar.update(1)

        save_to_json(indicators, data_base_path.format(destination_path))


def fetch_regions():
    # URL pour obtenir la liste des pays et régions

    destination_path = "raw/indicator/region_list.json"
    data_base_path = application.load()["data_base_path"]

    base_url = "http://api.worldbank.org/v2/country?format=json"
    current_page = 1
    total_pages = 1

    indicators = []

    response = requests.get(base_url)
    if response.status_code == 200:
        total_pages: int = response.json()[0]["pages"]

        with tqdm(total=total_pages, desc="Read indicator", file=sys.stdout) as pbar:
            while current_page <= total_pages:
                url = f"{base_url}&page={current_page}"
                response = requests.get(url)
                data = response.json()
                total_pages = data[0]["pages"]
                indicators += data[1]
                current_page += 1
                pbar.update(1)

        save_to_json(indicators, data_base_path.format(destination_path))
