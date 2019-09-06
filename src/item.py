class Item:
    def __init__(self, name, long_name, desc, obtainable=True):
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.obtainable = obtainable

    def __str__(self):
        return self.name
