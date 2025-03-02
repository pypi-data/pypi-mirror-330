import numpy as np
import pandas as pd


def is_it(page_text):
    if "COMPTE RENDU DE GESTION" in page_text:
        return True
    return False


def extract(table, additionnal_fields: dict = {}):
    """Extract "remise commercial" from first page"""
    extracted = []
    header = table[0]
    for row in table[1:]:
        if "Remise commerciale gérance" in row:
            r = dict()
            for i, value in enumerate(row):
                r[header[i]] = value
            for k, v in additionnal_fields.items():
                r[k] = v
            extracted.append(r)

    return extracted

    # df = pd.DataFrame(table[1:], columns=table[0]).replace("", np.nan)
    # df = df[
    #     df["RECAPITULATIF DES OPERATIONS"].str.contains(
    #         "Remise commerciale gérance", case=False, na=False
    #     )
    # ]
    #
    # df.columns.values[0] = "Fournisseur"
    # return df
