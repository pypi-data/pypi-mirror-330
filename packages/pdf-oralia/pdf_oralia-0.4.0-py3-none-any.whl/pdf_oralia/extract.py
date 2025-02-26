import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

import pdfplumber

from pdf_oralia.pages import charge, locataire, patrimoine

extract_table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "text",
}


def extract_date(page_text):
    """Extract date from a page

    :param page_text: text in the page
    :return: the extracted date
    """
    blocs = page_text.split("\n")
    for b in blocs:
        if "Lyon le" in b:
            words = b.split(" ")
            return datetime.strptime(words[-1], "%d/%m/%Y")


def extract_building(page_text, buildings=["bloch", "marietton", "servient"]):
    for building in buildings:
        if building in page_text.lower():
            return building
    raise ValueError("Pas d'immeuble trouvé")


def pdf_extract_tables_lines(pdf):
    loc_sink = locataire.fsm()
    next(loc_sink)
    charge_sink = charge.fsm()
    next(charge_sink)
    patrimoine_sink = patrimoine.fsm()
    next(patrimoine_sink)

    for page_number, page in enumerate(pdf.pages):
        page_text = page.extract_text()
        date = extract_date(page_text)
        try:
            additionnal_fields = {
                "immeuble": extract_building(page_text),
                "mois": date.strftime("%m"),
                "annee": date.strftime("%Y"),
            }
        except ValueError:
            logging.warning(
                f"L'immeuble de la page {page_number+1} non identifiable. Page ignorée."
            )
            continue
        table_type = ""
        if locataire.is_it(page_text):
            table_type = "locataire"
        elif charge.is_it(page_text):
            table_type = "charge"
        elif patrimoine.is_it(page_text):
            table_type = "patrimoine"
        else:
            logging.warning(
                f"Type de la page {page_number+1} non identifiable. Page ignorée."
            )
            continue

        for line in page.extract_table(extract_table_settings):
            if table_type == "locataire":
                res = loc_sink.send(line)
                if res:
                    res.update(additionnal_fields)
                    yield locataire.Line(**res)
            elif table_type == "charge":
                res = charge_sink.send(line)
                if res:
                    res.update(additionnal_fields)
                    yield charge.Line(**res)

            elif table_type == "patrimoine":
                res = patrimoine_sink.send(line)
                if res:
                    res.update(additionnal_fields)
                    yield patrimoine.Line(**res)


def from_pdf(pdf_file):
    """Build dataframes one about charges and another on loc"""
    pdf = pdfplumber.open(pdf_file)
    locataire_lines = []
    charge_lines = []
    patrimoine_lines = []
    for line in pdf_extract_tables_lines(pdf):
        if isinstance(line, locataire.Line):
            locataire_lines.append(line)
        elif isinstance(line, charge.Line):
            charge_lines.append(line)
        elif isinstance(line, patrimoine.Line):
            patrimoine_lines.append(line)
        else:
            logging.warning(f"Page {page_number+1} non reconnu. Page ignorée.")

    return {
        "charge": pd.DataFrame([c.__dict__ for c in charge_lines]),
        "locataire": pd.DataFrame([c.__dict__ for c in locataire_lines]),
        "patrimoine": pd.DataFrame([c.__dict__ for c in patrimoine_lines]),
    }


def extract_plan(pdf_file, dest):
    return {
        "charge": Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_charge.xlsx",
        "locataire": Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_locataire.xlsx",
        "patrimoine": Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_patrimoine.xlsx",
    }


def extract_save(pdf_file, dest, save=[]):
    """Extract charge and locataire for pdf_file and put xlsx file in dest"""
    pdf_file = Path(pdf_file)
    xlss = extract_plan(pdf_file, dest)

    if save != []:
        dfs = from_pdf(pdf_file)

        for s in save:
            dfs[s].to_excel(xlss[s], sheet_name=s, index=False)
            logging.info(f"{xlss[s]} saved")
        return {k: v for k, v in xlss.items() if k in save}

    return xlss
