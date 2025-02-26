import re
from pydantic import BaseModel, field_validator


HEADER_CHARGE = [
    "",
    "RECAPITULATIF DES OPERATIONS",
    "Débits",
    "Crédits",
    "Dont T.V.A.",
    "Locatif",
    "Déductible",
]
DF_TYPES = {
    "Fournisseur": str,
    "RECAPITULATIF DES OPERATIONS": str,
    "Débits": float,
    "Crédits": float,
    "Dont T.V.A.": float,
    "Locatif": float,
    "Déductible": float,
    "immeuble": str,
    "mois": str,
    "annee": str,
    "lot": str,
}


class Line(BaseModel):
    mois: int
    annee: int
    immeuble: str
    lot: str
    Champs: str
    Categorie: str
    Fournisseur: str
    Libellé: str
    Débit: float
    Crédits: float
    Dont_TVA: float
    Locatif: float
    Déductible: float

    @field_validator(
        "Débit", "Crédits", "Dont_TVA", "Locatif", "Déductible", mode="before"
    )
    def set_default_if_empty(cls, v):
        if v == "":
            return 0
        return v


def is_it(page_text):
    if (
        "RECAPITULATIF DES OPERATIONS" in page_text
        and "COMPTE RENDU DE GESTION" not in page_text
    ):
        return True
    return False


def get_lot(txt):
    """Return lot number from "RECAPITULATIF DES OPERATIONS" """
    regex = r"[BSM](\d+)(?=\s*-)"
    try:
        result = re.findall(regex, txt)
    except TypeError:
        return "*"
    if result:
        return "{:02d}".format(int(result[0]))
    return "*"


def fsm():
    current_state = "total"
    row = {}
    line = yield
    while True:
        if line == HEADER_CHARGE:
            line = yield
        if current_state == "total":
            if line[1].lower().split(" ")[0] in ["total", "totaux"]:
                current_state = "new_champs"
            line = yield
        elif current_state == "new_champs":
            if line[0] != "":
                current_state = "new_cat_line"
                row = {"Champs": line[0], "Categorie": "", "Fournisseur": ""}
            line = yield
        elif current_state == "new_cat_line":
            if line[1].lower().split(" ")[0] in ["total", "totaux"]:
                current_state = "new_champs"
                line = yield
                row = {}
            elif line[2] != "" or line[3] != "":
                row.update(
                    {
                        "Fournisseur": line[0] if line[0] != "" else row["Fournisseur"],
                        "Libellé": line[1],
                        "lot": get_lot(line[1]),
                        "Débit": line[2],
                        "Crédits": line[3],
                        "Dont_TVA": line[4],
                        "Locatif": line[5],
                        "Déductible": line[6],
                    }
                )
                line = yield row
                row = {
                    "Champs": row["Champs"],
                    "Categorie": row["Categorie"],
                    "Fournisseur": row["Fournisseur"],
                }
            elif line[0] != "" and line[1] == "":
                row.update({"Categorie": line[0]})
                line = yield
            elif line[1] != "":
                row.update({"Categorie": line[1]})
                line = yield
            elif line[0] != "":
                row.update({"Fournisseur": line[0]})
                line = yield
            else:
                line = yield
