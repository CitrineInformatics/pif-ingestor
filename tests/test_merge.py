from pif_ingestor.ui import get_cli
from pif_ingestor import main
from pypif import pif
from os.path import exists
from os import remove


def setup_function():
    """Remove output files from previous test runs"""
    fname = "tests/merge/pif.json"
    if exists(fname):
        remove(fname)

    return


def test_dft_csv_merge():
    """Test that auto-format works"""
    argv = "tests/merge -f merge".split()
    args = get_cli().parse_args(args=argv)
    main(args)

    # Make sure both files are processed
    assert exists("tests/merge/pif.json"), "Expected to find output pif for B.hR12"
    # Check basic parsing
    with open("tests/merge/pif.json", "r") as f:
        merged = pif.load(f)[0]
    assert merged.chemical_formula == "B12"
    assert merged.names[0] == 'P20 Tool steel'

