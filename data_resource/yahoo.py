from datetime import datetime
import logging
import yfinance as yf
import pandas_market_calendars as cal
import pandas as pd
from tqdm import tqdm
import sys
import os

from configuration import application
from data_manipulation.data_loader import list_files_without_extensions
from data_manipulation.data_saver import save_panda_csv, save_raw, save_to_json

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def get_symbol_resume(symbols):
    # Boucler sur chaque symbole
    destination_path = "data/symbol/{}.json"
    data_base_path = application.load()["data_base_path"]

    with tqdm(total=len(symbols), desc="Read symbols resume", file=sys.stdout) as pbar:
        for symbol in symbols:
            # Mise à jour de la barre de progression avec le nom du fichier traité
            pbar.set_description(f"Read {symbol.lower()}")

            # TODO: Add try cash to hiide notfoun datat and log out error.
            ticker = yf.Ticker(symbol)
            info = ticker.info

            save_to_json(
                info, data_base_path.format(destination_path.format(symbol.lower()))
            )
            pbar.update(1)


def get_historical():
    symbol_list_path = "data/symbol/"
    history_path = "data/history/{}.csv"
    dividend_path = "data/dividend/{}.csv"
    data_base_path = application.load()["data_base_path"]

    symbols = list_files_without_extensions(symbol_list_path)
    with tqdm(total=len(symbols), desc="Read historical", file=sys.stdout) as pbar:
        for symbol in symbols:
            pbar.set_description(f"Read {symbol}")
            try:
                ticker = yf.Ticker(symbol.upper())
                hist = ticker.history(period="max")
                dividends = ticker.dividends

                save_panda_csv(hist, data_base_path.format(history_path.format(symbol)))
                save_panda_csv(
                    dividends, data_base_path.format(dividend_path.format(symbol))
                )
            except Exception as e:
                logging.error(f"Error for {symbol}: {e}", exc_info=True)
            finally:
                pbar.update(1)
