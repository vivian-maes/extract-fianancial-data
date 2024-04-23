# data_saver.py
import pandas as pd
import pickle
import json
import os


def save_to_csv(data, filename):
    """
    Sauvegarde les données dans un fichier CSV.

    :param data: Liste des données à sauvegarder.
    :param filename: Nom du fichier où sauvegarder les données.
    """
    df = pd.DataFrame(data, columns=["Symbol", "Name", "Industry", "market"])
    df.to_csv(filename, index=False)


def save_panda_csv(data, filename):
    """
    Sauvegarde les données d'un objet panda dans un fichier CSV.
    Crée les répertoires parents si nécessaire.

    :param data: Fichier panda.
    :param filename: Nom du fichier où sauvegarder les données.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data.to_csv(filename)


def save_panda_parquet(data, filename):
    """
    Sauvegarde les données d'un objet panda dans un fichier parquet.
    Crée les répertoires parents si nécessaire.

    :param data: Fichier panda.
    :param filename: Nom du fichier où sauvegarder les données.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data.to_parquet(filename, compression="snappy")


def save_to_json(data, filename):
    """
    Sauvegarde des données dans un fichier JSON.
    Crée les répertoires parents si nécessaire.

    :param data: Les données à sauvegarder (doivent être sérialisables en JSON).
    :param filename: Le chemin du fichier où les données seront sauvegardées.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_pickle(data, filename):
    """
    Sauvegarde des données dans un pickle.
    Crée les répertoires parents si nécessaire.

    :param data: Les données à sauvegarder vu comme une suite de binaire.
    :param filename: Le chemin du fichier où les données seront sauvegardées.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb") as file:
        pickle.dump(data, file)


def save_raw(data, filename):
    """
    Sauvegarde des données dans un plat.
    Crée les répertoires parents si nécessaire.

    :param data: Les données à sauvegarder vu comme une suite de binaire.
    :param filename: Le chemin du fichier où les données seront sauvegardées.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)
