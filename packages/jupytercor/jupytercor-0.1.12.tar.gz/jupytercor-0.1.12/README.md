# Jupytercor

Jupytercor est un package python qui permet de convertir les cellules markdown d'un notebook jupyter avec pandoc.

## Installation et utilisation

Pour installer jupytercor, vous devez avoir python3 et pandoc installés sur votre machine.

Vous pouvez ensuite installer jupytercor avec pip:

```bash
pip install --upgrade jupytercor
```

Pour utiliser jupytercor, vous devez exécuter le script jupytercor.py avec la commande suivante:

```bash
jupytercor input.ipynb [-o output.ipynb] [--clean] [--to FORMAT] [--images]
```

Où:

- `input.ipynb` est le nom du fichier notebook d'entrée à convertir
- `-o output.ipynb` est une option qui permet de spécifier le nom du fichier notebook de sortie (par défaut c'est output.ipynb)
- `--to FORMAT` est une option pour préciser le format de sortie. 
    - `--to latex` pour convertir en LaTeX.
    - `--to pdf`pour convertir en PDF.
- `--clean` est une option qui permet d'effectuer les conversions avec pandoc (par défaut c'est False)
- `--images` est une option qui permet de télécharger les images distantes dans un dossier `images` (par défaut c'est False)

## Fonctionnalités et options

Jupytercor offre les fonctionnalités et options suivantes:

- Il lit un fichier notebook au format ipynb et en extrait les cellules markdown
- Il transforme chaque cellule markdown en html avec pandoc en utilisant l'option `-f markdown -t html`
- Il transforme chaque cellule html en markdown avec pandoc en utilisant l'option `-f html -t gfm-raw_html`
- Il remplace le contenu des cellules markdown par le texte transformé
- Il écrit un nouveau fichier notebook au format ipynb avec les cellules converties
- Il permet à l'utilisateur de choisir le nom du fichier notebook d'entrée et celui du fichier notebook de sortie
- Il permet à l'utilisateur d'activer ou non les conversions avec pandoc grâce au drapeau `--clean`
- Il permet à l'utilisateur de télécharger les images distantes avec une url grâce au drapeau `--images`

## Licence et crédits

Jupytercor est distribué sous la licence MIT.

Jupytercor utilise nbformat pour lire et écrire des fichiers notebooks.

Jupytercor utilise subprocess pour exécuter des commandes pandoc.

Jupytercor utilise argparse pour analyser les arguments passés au script.

Jupytercor s'inspire du code trouvé sur cette page web: https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree