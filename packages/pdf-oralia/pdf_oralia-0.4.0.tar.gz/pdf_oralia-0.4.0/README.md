# PDF AURALIA

Extraction de fichiers de comptabilité en pdf vers xlsx.

## Utilisation

- Lancement sur un fichier pdf particulier

  ```bash
  pdf_oralia extract on <pdf_file> --dest <where to put producted files>
  ```

- Lancement sur tous les fichiers d'un repertoire (récursivement )

  ```bash
  pdf_oralia extract all --src <source folder> --dest <destination folder>
  ```

  Cette commande reproduira la structure du dossier source dans destination. Seul les fichiers non existants seront traités. Par default, les fichiers déjà produits ne seront pas écrasés.
  On peut ajouter les options suivantes:

  - `--force`: pour écraser les fichiers déjà traités
  - `--only-plan`: pour voir quels fichiers pourraient être créé sans le faire.
