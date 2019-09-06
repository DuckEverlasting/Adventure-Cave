class Item:
    def __init__(self, name, long_name, desc, obtainable=True):
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.obtainable = obtainable

    def __str__(self):
        return self.name

class Light_Source(Item):
    def __init__(self, name, long_name, desc, obtainable=True, active=False):
        super().__init__(name, long_name, desc, obtainable)
        self.active = active