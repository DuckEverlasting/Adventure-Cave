from text_style import error_text


class Player:
    def __init__(self, init_loc, init_items=[]):
        self.loc = init_loc
        self.items = init_items

    def move(self, dir):
        if hasattr(self.loc, f"{dir}_to"):
            dest = getattr(self.loc, f"{dir}_to")
            self.loc = dest[0]
            return dest[1] + "\n"
        else:
            return False

    def look_item(self, item):
        if item in self.items or item in self.loc.items:
            return True
        else:
            return False

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            return False
    
    def use_item(self, item):
        if item in self.items:
            if hasattr(item, "use"):
                item.use()
            else:
                print("You can't use that.\n")
        elif item in self.loc.items:
            if item.obtainable:
                print("Try picking it up first.\n")
            else:
                print("You can't use that.\n")
        else:
            print("There is no such item here.\n")