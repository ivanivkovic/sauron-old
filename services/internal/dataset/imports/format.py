import csv, jsonpickle

class FormatConverter:

    def parse_csv(fstring, remove_rows):

        data = []
        rows = csv.reader(fstring.splitlines(), delimiter=',')

        for index, row in enumerate(rows):
            if remove_rows < index + 1:
                data.append(row)

        return data

    # In construction
    def parse_json(fstring):

        return jsonpickle.decode(fstring)
