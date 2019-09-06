class Item:
    def __init__(self, data):
        self.name = data["name"]
        self.long_name = data["long_name"]
        self.desc = data["desc"]
        self.obtainable = data["obtainable"]

    def __str__(self):
        return self.name