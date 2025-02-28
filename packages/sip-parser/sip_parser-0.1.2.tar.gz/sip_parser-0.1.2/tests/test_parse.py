""" text_elevator_cd_pdf.py - test Starr and xUML notation Elevator class diagram pdf output"""

import pytest
from pathlib import Path
from sip_parser.parser import SIParser

scenarios = [
    "elevator",
]

@pytest.mark.parametrize("pop", scenarios)
def test_scenarios_pdf(pop):

    result = SIParser.parse_file(file_input=Path(f"scenarios/{pop}.sip"), debug=False)
    assert result
