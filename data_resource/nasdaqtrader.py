import os
import pandas as pd

from configuration import application
from data_manipulation.data_convertion import pipe_to_tab_delimited
from data_manipulation.data_loader import load_file_from_ftp
from data_manipulation.data_saver import save_raw


def get_stocklists():
    server = "ftp.nasdaqtrader.com"
    source_path = "symboldirectory/{}.txt"
    destination_path = "raw/symbol_list/{}.csv"
    data_base_path = application.load()["data_base_path"]

    for file in ["nasdaqlisted", "otherlisted"]:
        destination = destination_path.format(file)
        if os.path.exists(destination):
            os.remove(destination)

        source = data_base_path.format(source_path.format(file))
        data = load_file_from_ftp(server, 21, source)

        save_raw(pipe_to_tab_delimited(data), destination)


def read_symbols():

    data = []

    destination_path = "raw/symbol_list/{}.csv"

    # "nasdaqlisted",
    for file in ["otherlisted"]:
        destination = destination_path.format(file)
        colone = "Symbol" if file == "nasdaqlisted" else "ACT Symbol"

        # Charger le fichier CSV délimité par des tabulations
        df = pd.read_csv(destination, delimiter="\t")

        # Supprimer les lignes où la colonne 'ma_colonne' contient des valeurs NaN ou vides
        df = df.dropna(subset=[colone])
        # Vous pouvez également vouloir supprimer les lignes où colone contient des chaînes vides
        df = df[df[colone] != ""]

        # last line has 'File createtd at...'
        drop_idx = df[df[colone].str.contains("File")].index
        df.drop(drop_idx, inplace=True)

        if file != "nasdaqlisted":
            for smb in ["\.W", "\.U", "\$"]:
                drop_idx = df[df[colone].str.contains(smb)].index
                df.drop(drop_idx, inplace=True)

        # Extraire la colonne nettoyée
        colonne_nettoyee = df[colone]
        # Convertir la colonne nettoyée en liste
        liste_colonne = colonne_nettoyee.tolist()

        data += liste_colonne

    return data
