from colorama import Fore, Back, Style


# Set up wrappers for coloring text
def title_text(string):
    return f"{Fore.YELLOW}{Back.BLUE}{string}{Style.RESET_ALL}"

def error_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}"

def desc_text(string):
    return f"{Fore.YELLOW}{string}{Style.RESET_ALL}"

def item_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Style.RESET_ALL}"

def item_in_desc_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.NORMAL}"

def mob_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}"

def mob_in_desc_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.NORMAL}"

def dir_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Style.RESET_ALL}"

def dir_in_desc_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.NORMAL}"