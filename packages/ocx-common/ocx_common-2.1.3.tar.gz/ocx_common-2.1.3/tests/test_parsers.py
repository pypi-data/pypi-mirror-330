#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE

# Project imports
from ocx_common.parser.parsers import OcxNotifyParser, OcxParser

from .conftest import MODEL_FOLDER, TEST_MODEL


class TestNotifyParser:
    def test_parse(self, shared_datadir):
        file = shared_datadir / MODEL_FOLDER / TEST_MODEL
        parser = OcxNotifyParser()
        root = parser.parse(str(file))
        name = root.header.name
        assert name == "OCX-MODEL1/A"


def test_parser(shared_datadir):
    file = shared_datadir / MODEL_FOLDER / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    assert (
        root.tag
        == "{https://3docx.org/fileadmin//ocx_schema//V300//OCX_Schema.xsd}ocxXML"
    )


# def test_parser_invalid_source(shared_datadir):   # ToDO: Add edge test case when source does not exist
#     file = shared_datadir / "not_exist.3docx"
#     try:
#         OcxParser(str(file))
#         assert False
#     except OcxParserError:
#         assert True
