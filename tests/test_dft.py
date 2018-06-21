from pif_ingestor.ui import get_cli
from pif_ingestor import main
from pypif import pif
from os.path import exists
from os import remove


def setup_function():
    """Remove output files from previous test runs"""
    fname = "tests/dft/B.hR12/pif.json"
    if exists(fname):
        remove(fname)

    fname = "tests/dft/B.hR105/pif.json"
    if exists(fname):
        remove(fname)

    return


def test_recursive_dft():
    """Test that recursive application of the DFT ingester works"""
    argv = "tests/dft -f dft -m tests/dft/metadata.json -r".split()
    args = get_cli().parse_args(args=argv)
    main(args)

    # Make sure both files are processed
    assert exists("tests/dft/B.hR12/pif.json"), "Expected to find output pif for B.hR12"
    assert exists("tests/dft/B.hR105/pif.json"), "Expected to find output pif for B.hR105" 

    # Check basic parsing
    with open("tests/dft/B.hR12/pif.json", "r") as f:
        bhr12 = pif.load(f)[0]
    assert bhr12.chemical_formula == "B12"
    assert len(bhr12.contacts) == 2

    emails = set(["johnsmith@generic.org", "janedoe@generic.org"])
    assert set(x.email for x in bhr12.contacts) == emails


def test_auto_dft():
    """Test that auto-format works"""
    argv = "tests/dft/B.hR12".split()
    args = get_cli().parse_args(args=argv)
    main(args)

    # Make sure both files are processed
    assert exists("tests/dft/B.hR12/pif.json"), "Expected to find output pif for B.hR12"
    assert not exists("tests/dft/B.hR105/pif.json"), "Did not expect to find output pif for B.hR105"
    # Check basic parsing
    with open("tests/dft/B.hR12/pif.json", "r") as f:
        bhr12 = pif.load(f)[0]
    assert bhr12.chemical_formula == "B12"
