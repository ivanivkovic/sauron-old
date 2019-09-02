import jsonpickle, urllib.request, os, sys, mysql.connector
from imports.format import FormatConverter

class Manager:

    sources = []
    dbConn = []
    db = []

    def __init__(self, sources_file):

        self.load_sources_file(sources_file)

        self.dbConn = mysql.connector.Connect(
                host="localhost",
                user="tester",
                passwd="tester123"
        )

        self.db = self.dbConn.cursor()
        self.create_database()

    def __exit(self):

        self.db.close()

    def update_datasets(self):

        for item in self.sources:

            print("Reading dataset %s..." % (item['name']))

            fstring = self.read_source(item["url"])

            # If there is data, cache it, for when the source might be obsolete.
            if len(fstring) > 0:

                file_name = self.generate_cache_file_name(item)
                self.write_to_file(file_name, fstring)

                rows = []

                if item["file_type"] == "csv":

                    rows = FormatConverter.parse_csv(fstring, item["remove_rows"])

                elif item['file_type'] == 'json':

                    rows = FormatConverter.parse_json(fstring, item["remove_rows"])

                item["data"] = rows

                print('Writing dataset %s to database...' % (item['name']))

                query = '''INSERT INTO %s ''' % (item['name'])
                query += '(' + ','.join(item['keys']) + ') VALUES '

                for index, row in enumerate(rows):
                    
                    row = ['"' + r.replace('"','\\"').replace("'", "\\'") + '"' for r in row]

                    if index > 0:
                        query += ','

                    query += '(' + ','.join(row) + ')'

                self.db.execute(query)

            else:

                print("Error: Source empty for %s." % (item['name']))

        print('Success! No errors.')

    def generate_cache_file_name(self, source_obj):

        return "cache/%s.%s" % (source_obj["name"],source_obj["file_type"])

    def write_to_file(self, file_name, fstring):

        print("Writing cache file %s" % file_name)

        with open(file_name, 'w+') as f:

            f.write(fstring)

    def load_sources_file(self, sources_file):

        try:
            with open(sources_file, "r") as f:
                self.sources = FormatConverter.parse_json(f.read())

        except FileNotFoundError:
            print('Error: Sources file does not exist!')

    def create_database(self):

        print ("Creating the database if it doesn't exist...")

        result = self.db.execute('CREATE DATABASE IF NOT EXISTS crawline COLLATE=utf8_general_ci DEFAULT charset=utf8;')

        print('Creating database tables...')

        self.dbConn = mysql.connector.Connect(
                host="localhost",
                user="tester",
                passwd="tester123",
                database="crawline"
        )

        self.db = self.dbConn.cursor()

        for item in self.sources:

            # First, drop the possible existing table so we have a cleared space to work with.
            self.db.execute('''DROP TABLE IF EXISTS %s;''' % (item['name']))

            # Secondary, recreate the table.
            query = '''CREATE TABLE %s ( id INT(11) NOT NULL auto_increment''' % (item["name"])

            for index, key in enumerate(item["keys"]):
                query += '''
                    ,%s %s''' % (key, item["keys"][key])

            query += ''' , PRIMARY KEY (id) ) ENGINE = MyISAM'''

            result = self.db.execute(query)

    def read_source(self, url ):

        response = urllib.request.urlopen(url)
        return response.read().decode("utf-8")
