import glob
import logging

import pandas as pd


def join_excel(src, dest, file_pattern):
    """Join every excel file in arc respecting file_pattern into on unique file in dist"""
    filenames = list_files(src, file_pattern)
    logging.debug(f"Concatenate {filenames}")
    dfs = extract_dfs(filenames)
    joined_df = pd.concat(dfs)
    logging.debug(f"Writing joined excel to {dest}")
    joined_df.to_excel(dest, index=False)
    logging.debug(f"with {len(joined_df)} rows")


def list_files(src, file_glob):
    return list(glob.iglob(f"{src}/{file_glob}"))


def extract_dfs(filenames):
    dfs = []
    for filename in filenames:
        logging.debug(f"Extracting {filename}")
        df = pd.read_excel(filename)
        logging.debug(f"Found {len(df)} rows")
        dfs.append(df)
    return dfs
