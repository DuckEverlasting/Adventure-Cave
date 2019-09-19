class Item:
    def __init__(self, name, long_name, desc, weight=None, tags=[]):
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.weight = weight
        self.tags = tags

    def __str__(self):
        return self.name
    
    def use(self):
        print(f"You don't see a way to use the {self.name}.\n")
        return False
    
    def use_from_env(self):
        if "obtainable" in self.tags:
            print("Try picking it up first.\n")
            return False
        else:
            print("You can't use that.\n")
            return False
    
    def on_eat(self):
        pass
    
    def on_look(self):
        pass

    def on_pick_up(self):
        pass

    def eat(self, container):
        if "food" in self.tags:
            print(f"You wolf down the {self.name}. Yum.\n")
            self.on_eat()
            container.items.remove(self)
            return True
        elif "corpse" in self.tags:
            print("What? No. That's just... no.\n\nGross.\n")
            return False
        else:
            print(f"That's... not food.\n")
            return False
    

class Light_Source(Item):
    def __init__(self, name, long_name, desc, weight=None, lit=False, tags=[]):
        super().__init__(name, long_name, desc, weight, tags)
        self.lit = lit
        self.tags = tags + ["light_source"]

class Weapon(Item):
    def __init__(self, name, long_name, desc, stats, attack_text, weight=None, tags=[]):
        super().__init__(name, long_name, desc, weight, tags)
        self.damage = stats["damage"]
        self.accuracy = stats["accuracy"]
        self.attack_text = attack_text
        self.tags = tags + ["weapon"]