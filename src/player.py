from colorama import Fore, Back, Style


class Player:
    def __init__(self, initLoc, initItems=[]):
        self.loc = initLoc
        self.items = initItems

    def move(self, dir):
        if hasattr(self.loc, f"{dir}_to"):
            dest = getattr(self.loc, f"{dir}_to")
            self.loc = dest[0]
            print(dest[1] + "\n")
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}ERROR: MOVEMENT NOT ALLOWED\n{Style.RESET_ALL}"
            )

    def lookItem(self, item):
        if item in self.items or item in self.loc.items:
            print(f"{item.desc}\n")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM\n{Style.RESET_ALL}")

    def addItem(self, item):
        self.items.append(item)
        print(f"You pick up the {item.name}.\n")

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"You set down the {item.name}.\n")
            return True
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM IN INVENTORY\n{Style.RESET_ALL}"
            )
            return False
