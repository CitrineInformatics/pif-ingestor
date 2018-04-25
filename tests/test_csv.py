from pif_ingestor.ui import get_cli
from pif_ingestor import main
from pypif import pif
from os.path import exists


def test_csv_generator():
    """Test that generator-returning ingesters work"""
    argv = "tests/csv/template_example.csv template_csv".split()
    args = get_cli().parse_args(args=argv)
    main(args)

    # Make sure both files are processed
    expected_name = "tests/csv/template_example.csv_pif.json"
    assert exists(expected_name), "Expected to find output pif for template_example"

    # Check basic parsing
    with open(expected_name, "r") as f:
        csv_pif = pif.load(f)

    assert csv_pif[0].names[0] == 'P20 Tool steel'
    assert csv_pif[0].sub_systems[0].names[0] == 'Martensite'
    assert csv_pif[0].sub_systems[0].quantity.ideal_mass_percent.value == '80'
    assert csv_pif[0].contacts[0].name == 'Jo Hill'
    assert csv_pif[0].contacts[0].email == 'jo@citrine.io'
    assert csv_pif[0].contacts[2].name == 'Mary'
    assert csv_pif[0].contacts[2].url == 'http://jo'
