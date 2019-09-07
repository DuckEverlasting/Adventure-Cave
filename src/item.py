class Item:
    def __init__(self, name, long_name, desc, obtainable=True):
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.obtainable = obtainable

    def __str__(self):
        return self.name
    
    def use(self):
        print(f"You don't see a way to use the {self.name}.\n")
        return False
    
    def use_from_env(self):
        if self.obtainable:
            print("Try picking it up first.\n")
            return False
        else:
            print("You can't use that.\n")
            return False
    
    def on_look(self):
        pass

    def on_pick_up(self):
        pass

class Light_Source(Item):
    def __init__(self, name, long_name, desc, obtainable=True, active=False):
        super().__init__(name, long_name, desc, obtainable)
        self.active = active
