# main.py
import os
from tqdm import tqdm


from calculation.prepare_data import (
    compute_anual_value,
    compute_divident,
    compute_sector,
    create_basic_structure,
)
from configuration import application
from data_manipulation.data_saver import (
    save_panda_parquet,
    save_to_json,
    save_to_pickle,
)
from data_resource.nasdaqtrader import get_stocklists, read_symbols
from data_resource.yahoo import get_historical, get_symbol_resume

os.system("cls" if os.name == "nt" else "clear")

#
# Export data from yahoo
#
##--get_stocklists()
##--get_symbol_resume(read_symbols())
##--get_historical()

#
# Prepare data_set
#
data_set = create_basic_structure()
data_set = compute_sector(data_set)
data_set = compute_anual_value(data_set)
data_set = compute_divident(data_set)
#
save_to_json(data_set, application.load()["data_base_path"].format("data_set.json"))
save_to_pickle(data_set, application.load()["data_base_path"].format("data_set.pkl"))


##--actions_data = {
##--    'action': ['Action A', 'Action B', 'Action C', 'Action D'],
##--    'secteur': ['Technologie', 'Finance', 'Energie', 'Santé'],
##--    'region': ['USA', 'Europe', 'Asie', 'International'],
##--    'rendement_ajuste_inflation': [0.05, 0.03, 0.04, 0.06],  # Rendement annuel moyen ajusté
##--    'stable_during_crisis': [True, False, True, True],
##--    'dividendes_reguliers': [True, True, True, True]
##--}
