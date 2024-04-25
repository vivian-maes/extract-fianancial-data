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


def fetch_data(data_set):
    ## Recuperer les dates debut fion des quote.
    start_year = data_set["config"]["date_quote"]["start_year"]
    end_year = data_set["config"]["date_quote"]["end_year"]

    app = application.load()
    regions = app["regions"]
    indicators = app["indicators"]

    all_indicators = []
    indicators_config = {}
    region_config = {}

    indicators_config_is_first = True
    region_indx = 0
    indicator_indx = 0

    with tqdm(
        total=len(regions) * len(indicators), desc="Fetch indicators", file=sys.stdout
    ) as pbar:

        for region in regions:
            region_config[region_indx] = region
            region_indicators = []
            for indicator in indicators:
                url = f"http://api.worldbank.org/v2/country/{region}/indicator/{indicator}?format=json&date={start_year}:{end_year}"
                response = requests.get(url)
                innfo_data = response.json()
                current_page = 1
                total_pages: int = innfo_data[0]["pages"]

                if indicators_config_is_first:
                    indicators_config[indicator_indx] = {
                        "code": indicator,
                        "description": innfo_data[1][0]["indicator"]["value"],
                    }

                # process data here
                current_inidicator = []
                current_start_year = None
                current_end_year = None
                while current_page <= total_pages:
                    loop_url = f"{url}&page={current_page}"
                    response = requests.get(loop_url)
                    datas = response.json()
                    total_pages = datas[0]["pages"]
                    current_page += 1

                    for data in datas[1]:
                        if current_end_year is None:
                            current_end_year = int(data["date"])
                        current_start_year = int(data["date"])
                        current_inidicator.insert(
                            0, data["value"] if data["value"] is not None else 0.0
                        )

                miss = current_start_year - start_year
                if miss > 0:
                    padding = [0.0 for _ in range(miss)]
                    current_inidicator = padding + current_inidicator

                miss = end_year - current_end_year
                if miss > 0:
                    padding = [0.0 for _ in range(miss)]
                    current_inidicator += padding

                region_indicators.append(current_inidicator)

                indicator_indx += 1

            indicators_config_is_first = False
            region_indx += 1
            indicator_indx = 0
            all_indicators.append(region_indicators)
            pbar.update(1)

    data_set["indicators"] = all_indicators
    data_set["config"]["indicators"] = indicators_config
    data_set["config"]["regions"] = region_config
    return data_set


##--    # URL de l'API pour les données d'inflation (Indice des prix à la consommation)
##--    url = f"http://api.worldbank.org/v2/country/{region_code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}"
##--
##--    # Envoi de la requête GET à l'API
##--    response = requests.get(url)
##--
##--    # Vérifier que la requête a réussi
##--    if response.status_code == 200:
##--        # Convertir la réponse en JSON
##--        data = response.json()
##--        print(data[1])
##--    else:
##--        return "Failed to fetch data: " + response.status_code
##--
