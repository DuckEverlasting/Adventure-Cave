from text_style import error_text


class Player:
    def __init__(self, data):
        self.loc = data["init_loc"]
        self.items = data["init_items"]

    def move(self, dir):
        if hasattr(self.loc, f"{dir}_to"):
            dest = getattr(self.loc, f"{dir}_to")
            self.loc = dest[0]
            print(f"{dest[1]}\n")
            return True
        else:
            print(error_text("ERROR: MOVEMENT NOT ALLOWED\n"))
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
                return True
            else:
                print("You can't use that.\n")
                return False
        elif item in self.loc.items:
            if hasattr(item, "use_from_env"):
                item.use_from_env()
                return True
            elif item.obtainable:
                print("Try picking it up first.\n")
                return False
            else:
                print("You can't use that.\n")
                return False
        else:
            print("There is no such item here.\n")
            return False