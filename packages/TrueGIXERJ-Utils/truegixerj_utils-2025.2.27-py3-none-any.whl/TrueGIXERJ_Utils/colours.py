ENDC = '\033[0m'
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
CYAN = '\033[96m'

def red(text: str) -> str:
    """
    Returns the input red

    :param text: the input text to be coloured
    :return: the text wrapped in ANSI escape codes
    """
    return RED + text + ENDC

def yellow(text: str) -> str:
    """
    Returns the input yellow

    :param text: the input text to be coloured
    :return: the text wrapped in ANSI escape codes
    """
    return YELLOW + text + ENDC

def green(text: str) -> str:
    """
    Returns the input green

    :param text: the input text to be coloured
    :return: the text wrapped in ANSI escape codes
    """
    return GREEN + text + ENDC

def cyan(text: str) -> str:
    """
    Returns the input cyan

    :param text: the input text to be coloured
    :return: the text wrapped in ANSI escape codes
    """
    return CYAN + text + ENDC

