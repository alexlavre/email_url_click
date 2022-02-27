import datetime
import eml_parser


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def parse_eml(path):
    try:
        with open(path, 'rb') as eml_file:
            parsed_eml = eml_parser.EmlParser().decode_email_bytes(eml_file.read())
            return parsed_eml
    except Exception as e:
        print(e)
