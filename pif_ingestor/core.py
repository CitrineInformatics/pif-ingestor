from .ui import get_cli
from .manager import run_extension
from .enrichment import add_tags, add_license, add_contact
from .uploader import upload
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

    # Upload the pif and associated files
    if args.dataset:
        if os.path.isfile(args.path):
            to_upload = [args.path, pif_name]
        else:
            to_upload = [args.path]
        upload(to_upload, args.dataset)
