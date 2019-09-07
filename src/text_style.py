from colorama import Fore, Back, Style


# Set up wrappers for coloring text
def title_text(string):
    return f"{Fore.YELLOW}{Style.BRIGHT}{Back.BLUE}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def error_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def desc_text(string):
    return f"{Fore.YELLOW}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def item_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def item_in_desc_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"

def mob_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def mob_in_desc_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"

def dir_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def dir_in_desc_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"