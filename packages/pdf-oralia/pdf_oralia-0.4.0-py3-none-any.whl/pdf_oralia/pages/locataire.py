from pydantic import BaseModel, field_validator

HEADER_LOC = [
    "Locataires",
    "Période",
    "Loyers",
    "Taxes",
    "Provisions",
    "Divers",
    "",
    "Total",
    "Réglés",
    "Impayés",
]


class Line(BaseModel):
    mois: int
    annee: int
    immeuble: str
    Lot: str
    Type: str
    Locataire: str
    Loyers: float
    Taxes: float
    Provisions: float
    Divers: float
    Total: float
    Réglés: float
    Impayés: float

    @field_validator(
        "Loyers",
        "Taxes",
        "Provisions",
        "Divers",
        "Total",
        "Réglés",
        "Impayés",
        mode="before",
    )
    def set_default_if_empty(cls, v):
        if v == "":
            return 0
        return v


def is_it(page_text):
    if "SITUATION DES LOCATAIRES" in page_text:
        return True
    return False


def parse_lot(string):
    words = string.split(" ")
    return {"Lot": "{:02d}".format(int(words[1])), "Type": " ".join(words[2:])}


def fsm():
    current_state = "new_row"
    row = {}
    line = yield
    while True:
        if line == HEADER_LOC:
            line = yield
        elif current_state == "new_row":
            if line[0] != "" and line[0] != "TOTAUX":
                row.update(parse_lot(line[0]))
                current_state = "add_loc"
            line = yield
        elif current_state == "add_loc":
            if line[0] != "":
                row["Locataire"] = line[0]
                current_state = "add_totaux"
            line = yield
        elif current_state == "add_totaux":
            if line[0] == "Totaux":
                row.update(
                    {
                        "Loyers": line[2],
                        "Taxes": line[3],
                        "Provisions": line[4],
                        "Divers": line[5],
                        "Total": line[7],
                        "Réglés": line[8],
                        "Impayés": line[9],
                    }
                )
                line = yield row
                row = {}
                current_state = "new_row"
            else:
                line = yield
