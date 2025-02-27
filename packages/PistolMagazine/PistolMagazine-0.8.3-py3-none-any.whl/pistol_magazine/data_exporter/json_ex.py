import json
from .exporter import Exporter


# class JSONExporter(Exporter):
#     def export(self, data, filename):
#         with open(filename, 'a') as output_file:
#             output_file.write(json.dumps(data))


class JSONExporter(Exporter):
    def export(self, data, filename):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("The provided string is not a valid JSON format")
        with open(filename, 'w') as output_file:
            json.dump(data, output_file, indent=4)
