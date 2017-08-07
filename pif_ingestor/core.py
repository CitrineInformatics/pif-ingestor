from .ui import get_cli
from .manager import run_extension
from .enrichment import add_tags, add_license, add_contact
from .uploader import upload
from .packager import create_package
import os.path
from pypif import pif
import logging


def main():
    """Main driver for pif-ingestor"""

    # Get direction from the user
    parser = get_cli()
    args = parser.parse_args()

    # Run an ingest extension
    pifs = run_extension(args.format, args.path, args.converter_arguments)

    # Perform enrichment
    add_tags(pifs, args.tags)
    add_license(pifs, args.license)
    add_contact(pifs, args.contact)

    # Write the pif
    if os.path.isfile(args.path):
        pif_name = os.path.join(os.path.dirname(args.path), "pif.json")
    else:
        pif_name = os.path.join(args.path, "pif.json")

    with open(pif_name, "w") as f:
        pif.dump(pifs, f, indent=2)
    logging.info("Created pif at {}".format(pif_name))

    if os.path.isfile(args.path):
        all_files = [args.path, pif_name]
    else:
        all_files = [args.path]

    # Upload the pif and associated files
    if args.dataset:
        upload(all_files, args.dataset)

    if args.zip:
        if args.zip[-4:] == ".zip":
            zipname = args.zip
        else:
            zipname = args.zip + ".zip"
        create_package(all_files, zipname, format="zip")

    if args.tar:
        if args.tar[-4:] == ".tar":
            tarname = args.tar
        else:
            tarname = args.tar + ".tar"
        create_package(all_files, tarname, format="tar")
