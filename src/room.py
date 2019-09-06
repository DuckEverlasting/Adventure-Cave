from text_style import error_text


class Room:
    def __init__(self, data):
        self.name = data["name"]
        self.desc = data["desc"]
        self.no_mobs = data["no_mobs"]
        self.items = data["init_items"]

    def __str__(self):
        return self.name

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            if item.obtainable:
                self.items.remove(item)
                return (True,)
            else:
                return (False, "You decide to leave it there.")
        else:
            return (False, error_text("ERROR: NOTHING HERE BY THAT NAME\n"))