import logging
from logging.config import dictConfig
from pathlib import Path

import click

from .extract import extract_save, extract_plan
from .join import join_excel


@click.group()
@click.option("--debug/--no-debug", default=False)
def main(debug):
    if debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging_config = dict(
        version=1,
        formatters={"f": {"format": "%(levelname)-8s %(name)-12s %(message)s"}},
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": logging_level,
            }
        },
        root={
            "handlers": ["h"],
            "level": logging_level,
        },
    )

    dictConfig(logging_config)


@main.group()
def extract():
    pass


@extract.command()
@click.argument("pdf_file", required=1)
@click.option("--dest", help="Où mettre les fichiers produits", default="")
def on(pdf_file, dest):
    if not dest:
        pdf_path = Path(pdf_file)
        dest = pdf_path.parent

    extract_save(pdf_file, dest)


@extract.command()
@click.option(
    "--src", help="Tous les fichiers dans folder (de façon récursive)", default="./"
)
@click.option("--dest", help="Où mettre les fichiers produits", default="./")
@click.option(
    "--only-plan",
    help="Ne produit rien mais indique les changements",
    default=False,
    is_flag=True,
)
@click.option(
    "--force",
    help="Écrase les fichiers produits précédemment",
    default=False,
    is_flag=True,
)
def all(src, dest, force, only_plan):
    src_path = Path(src)

    dest = Path(dest)
    dest.mkdir(exist_ok=True)

    for pdf_file in src_path.rglob("**/*.pdf"):
        relative_path = pdf_file.relative_to(src_path)
        files_dest = dest / relative_path.parent
        logging.info(f"Found {pdf_file}")

        plan_dest = extract_plan(pdf_file, files_dest)
        save = []
        for k, p in plan_dest.items():
            if not p.exists() or force:
                save.append(k)

        if only_plan:
            for s in save:
                logging.info(f"Planing to create {plan_dest[s]}")
        else:
            files_dest.mkdir(parents=True, exist_ok=True)
            extract_save(pdf_file, files_dest, save)


@main.command()
@click.option("--src", help="Tous les fichiers dans src", default="./")
@click.option("--dest", help="Où mettre les fichiers produits", default="")
@click.option(
    "--force",
    help="Ecraser si le ficher destination existe.",
    default=False,
    is_flag=True,
)
def join(src, dest, force):
    """Join tous les fichiers excel charge (resp locataire) de src dans un seul fichier charge.xlsx dans dist.

    Exemple:

        pdf-oralia join --src <dossier_source> --dest <dossier_destination>


    """
    dest_charge = f"{dest}/charge.xlsx"
    if not force and Path(dest_charge).exists():
        raise ValueError(f"The file {dest_charge} already exists")
    dest_locataire = f"{dest}/locataire.xlsx"
    if not force and Path(dest_locataire).exists():
        raise ValueError(f"The file {dest_locataire} already exists")

    if not Path(src).exists():
        raise ValueError(f"The source directory ({src}) does not exists.")
    join_excel(src, dest_charge, "*_charge.xlsx")
    logging.info(f"Les données charges ont été concaténées dans {dest_charge}")
    join_excel(src, dest_locataire, "*_locataire.xlsx")
    logging.info(f"Les données locataires ont été concaténées dans {dest_locataire}")
