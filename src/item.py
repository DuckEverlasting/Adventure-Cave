class Item:
    def __init__(self, name, longName, desc):
        self.name = name
        self.longName = longName
        self.desc = desc

    def __str__(self):
        return self.name
