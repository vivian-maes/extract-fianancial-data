# main.py
import os
from tqdm import tqdm


from data_resource.nasdaqtrader import get_stocklists, read_symbols
from data_resource.yahoo import get_historical, get_symbol_resume

os.system("cls" if os.name == "nt" else "clear")

get_stocklists()

get_symbol_resume(read_symbols())

get_historical()
