from colorama import Fore, Back, Style


class Room:
    def __init__(self, name, desc, initItems=[]):
        self.name = name
        self.desc = desc
        self.items = initItems

    def __str__(self):
        return self.name

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM IN ROOM\n{Style.RESET_ALL}"
            )
            return False
