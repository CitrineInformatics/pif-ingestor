from pif_ingestor.ui import get_cli
from pif_ingestor import main
from pypif import pif
from os.path import exists
from os import remove


def setup_function():
    """Remove output files from previous test runs"""
    fname = "tests/merge/1000000.cif_pif.json"
    if exists(fname):
        remove(fname)

    return


def test_dft_csv_merge():
    """Test that merge works works"""
    argv = "tests/merge/1000000.cif -f merge".split()
    args = get_cli().parse_args(args=argv)
    main(args)

    # Make sure there is an output
    assert exists("tests/merge/1000000.cif_pif.json"), "Expected to find output pif for 1000000.cif"

    # Check that one property from each ingester is included
    with open("tests/merge/1000000.cif_pif.json", "r") as f:
        merged = pif.load(f)[0]
    # This is from the calphad tdb ingester
    assert next((x for x in merged.properties if x.name == "Thermodynamic database"), None) != None
    # This is from the CIF ingester
    space_group = next((x for x in merged.properties if x.name == "Space group symbol"), None)
    assert(space_group.scalars[0].value == "P2_1/c")

