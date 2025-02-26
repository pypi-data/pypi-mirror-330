from pydantic import BaseModel, field_validator

HEADER_PATRIMOINE = [
    "Etage",
    "Lots",
    "Type de lot",
    "Nom du Locataire",
    "Loyer Annuel",
    "Début Bail",
    "Fin Bail",
    "Entrée",
    "Départ",
    "Révisé le",
    "U",
    "Dépôt Gar.",
]


class Line(BaseModel):
    mois: int
    annee: int
    immeuble: str
    Etage: str
    Lot: str
    Type: str
    Locataire: str
    Loyer_annuel: int
    Debut_bail: str
    Fin_bail: str
    Entree: str
    Depart: str
    Revision_bail: str
    Usage: str
    Depot_garantie: float

    @field_validator("Loyer_annuel", "Depot_garantie", mode="before")
    def set_default_if_empty(cls, v):
        if v == "":
            return 0
        return v


def is_it(page_text):
    if "VOTRE PATRIMOINE" in page_text:
        return True
    return False


def fsm():
    current_state = "new_line"
    row = {}
    line = yield
    while True:
        if line == HEADER_PATRIMOINE:
            line = yield
        if current_state == "new_line":
            if line[0] != "":
                row = {
                    "Etage": line[0],
                    "Lot": line[1][-2:] if line[1] != "" else row["Lot"],
                    "Type": line[2] if line[2] != "" else row["Type"],
                    "Locataire": line[3],
                    "Loyer_annuel": line[4].replace(" ", ""),
                    "Debut_bail": line[5],
                    "Fin_bail": line[6],
                    "Entree": line[7],
                    "Depart": line[8],
                    "Revision_bail": line[9],
                    "Usage": line[10],
                    "Depot_garantie": line[11].replace(" ", ""),
                }
                line = yield row
            else:
                line = yield
