class Config(object):

    val = {
        "sources_file": "sources.json",
        "get_interval": 5
    }

    def set_config(self, arg):

        data = arg.split("=", 1)
        
        if data[0] in self.val:
            self.val[data[0]] = data[1]
        else:
            print(f"Warning: {data[0]} is an invalid config field.")