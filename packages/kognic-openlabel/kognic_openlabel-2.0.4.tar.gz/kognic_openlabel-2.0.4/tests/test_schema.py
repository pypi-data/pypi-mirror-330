import json

from jsonschema import validate as json_validator

import kognic.openlabel.models as OLM
import kognic.openlabel.schemas as schemas

SCHEMA_FILE = "openlabel-1-0-0.json"

def get_schema() -> dict:
    schema_path = "/".join([schemas.__path__[0], SCHEMA_FILE])
    with open(schema_path, "r") as fp:
        return json.load(fp)

def test_schema_validation_empty():
    ola = OLM.OpenLabelAnnotation(
        openlabel=OLM.Openlabel(
            metadata=OLM.Metadata(schema_version=OLM.SchemaVersion.field_1_0_0)
        )
    )
    ola_dict = ola.dict(exclude_none=True)
    json_validator(ola_dict, schema=get_schema())

