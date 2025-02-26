#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import subprocess
from importlib import resources

from jupytercor.images import *
from jupytercor.utils import *

# Create an argument parser object
parser = argparse.ArgumentParser(
    description="Convert markdown cells in a jupyter notebook with pandoc"
)
# Add an input file argument
parser.add_argument("input_file", help="The name of the input notebook file")
# Add an output file argument with no default value
parser.add_argument(
    "-o", "--output_file", help="The name of the output notebook file", default=None
)
# Add an toargument with pdf default value
parser.add_argument("--to", help="The name of the output format", default="pdf")

# Add an templateargument with cornouaille default value
parser.add_argument("--template", help="Template: cornouaille or eisvogel", default="cornouaille")
# Add a clean flag argument with a default value of False
parser.add_argument(
    "--clean",
    help="Clean the markdown cells with pandoc conversions",
    action="store_true",
)

# Add a images flag argument with a default value of False
parser.add_argument(
    "--images", help="Downlad image in images folder", action="store_true"
)

# Add a debug flag argument with a default value of False
parser.add_argument("--debug", help="Debug mode", action="store_true")
# Parse the arguments
args = parser.parse_args()


def convert_to_latex(input_file: str, template = "cornouaille.latex") -> None:
    """Convert a notebook to latex using pandoc

    Args:
        input_file (str): The name of the input notebook file

    Returns:
        None
    """
    name, ext = os.path.splitext(input_file)
    output_tex = name + ".tex"


    # Accéder aux ressources du package
    with resources.as_file(resources.files("jupytercor.templates")) as templates_path:
        with resources.as_file(resources.files("jupytercor.filters")) as filters_path:
            filter1 = os.path.join(filters_path, "panflute-headers.py")
            filter2 = os.path.join(filters_path, "pandoc-ldotcarreaux.py")
            template_file = os.path.join(templates_path, template)
            
            # Vérifier que les fichiers existent
            print(f"Filter 1 path: {filter1}")
            print(f"Filter 2 path: {filter2}")
            print(f"Template path: {template_file}")
            for path in [filter1, filter2, template_file]:
                if not os.path.exists(path):
                    print(f"File not found: {path}")
                    raise FileNotFoundError(f"Missing file: {path}")
            try:
                tex = subprocess.run(
                    [
                        "pandoc",
                        input_file,
                        "-t",
                        "latex",
                        "-o",
                        output_tex,
                        "--listing",
                        "--filter",
                        os.path.join(filters_path, "panflute-headers.py"),
                        "--filter",
                        os.path.join(filters_path, "pandoc-ldotcarreaux.py"),
                        "--template",
                        os.path.join(templates_path, template),
                    ],
                    capture_output=True,
                    check=True,
                )
            except FileNotFoundError as e:
                print("Pandoc not found, please install it.")
            except subprocess.CalledProcessError as e:
                print("Error while running pandoc. Please check your notebook.")


def convert_to_pdf(input_file: str, template = "cornouaille") -> None:
    """
    Convert a notebook to pdf using pandoc and xelatex
    Args:
        input_file (str): The name of the input notebook file

    Returns:
        None"""
    name, ext = os.path.splitext(input_file)
    output_tex = name + ".tex"
    output_pdf = name + ".pdf"
    # Accéder aux ressources du package
    with resources.as_file(resources.files("jupytercor.templates")) as templates_path:
        with resources.as_file(resources.files("jupytercor.filters")) as filters_path:
            extra = []
            if "cornouaille" in template:
                extra = ["--listing",
                                "--filter",
                                os.path.join(filters_path, "panflute-headers.py"),
                                "--filter",
                                os.path.join(filters_path, "pandoc-ldotcarreaux.py"),]
            tex = subprocess.run(
                [
                    "pandoc",
                    input_file,
                    "-t",
                    "latex",
                    "-o",
                    output_tex,
                    
                    "--template",
                    os.path.join(templates_path, template),
                ] + extra,
                capture_output=True,
            )
            subprocess.run(["xelatex", output_tex])


def main():
    print("Hello from jupytercor !")
    if args.debug:
        templates_path = os.path.join(os.path.dirname(__file__), "templates")
        print("Debug mode")
        print(templates_path)
        return None
    if args.images:
        print("Téléchargement d'images éventuelles...")
        nb = process_images(nb)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)

        print("Téléchargement d'images effectué avec succès !")
    elif args.clean:
        # Read the input notebook file from the input_file argument
        nb = nbformat.read(args.input_file, as_version=4)
        print("Démarrage du nettoyage...")
        templates_path = os.path.join(os.path.dirname(__file__), "templates")
        filters_path = os.path.join(os.path.dirname(__file__), "filters")
        nb = clean_markdown(nb, templates_path, filters_path)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)
        print("Nettoyage effectué avec succès !")
    elif args.to:
        print(f"Conversion vers {args.to} avec le template {args.template}")
        if args.to == "pdf":
            convert_to_pdf(args.input_file,args.template)
        elif args.to == "latex":
            convert_to_latex(args.input_file,args.template)
        else:
            print("Format de sortie non pris en charge")

        return None
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    

    if args.clean:
        print("Démarrage du nettoyage...")
        templates_path = os.path.join(os.path.dirname(__file__), "templates")
        filters_path = os.path.join(os.path.dirname(__file__), "filters")
        nb = clean_markdown(nb, templates_path, filters_path)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)
        print("Nettoyage effectué avec succès !")
    elif args.images:
        print("Téléchargement d'images éventuelles...")
        nb = process_images(nb)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)

        print("Téléchargement d'images effectué avec succès !")


if __name__ == "__main__":
    main()
