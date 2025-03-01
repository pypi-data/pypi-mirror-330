import json
import os
import jsonschema.validators
from pathlib import Path


class InputValidator:
    def __init__(self):
        self.schemas = {}
        schema_folder = f"{Path(__file__).parent}/schemas"
        for filename in os.listdir(schema_folder):
            if filename.endswith('.json'):
                with open(os.path.join(schema_folder, filename)) as f:
                    self.schemas[os.path.splitext(filename)[0]] = json.load(f)

    def is_valid_input(self, operation_type, input_json):
        schema = self.schemas.get(operation_type)
        if schema is None:
            return False
        try:
            jsonschema.validators.validate(input_json, schema)
            return True
        except jsonschema.ValidationError:
            return False
