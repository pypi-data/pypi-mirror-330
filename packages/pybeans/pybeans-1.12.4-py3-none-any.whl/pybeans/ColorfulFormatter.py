import logging, json
from collections.abc import Iterable
from colorama import Fore, Back, Style

class ColorfulFormatter(logging.Formatter):

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Style.RESET_ALL + Style.DIM + "%(asctime)s - %(name)s - " + Style.RESET_ALL + Fore.BLUE + Back.WHITE + " %(levelname)s " + Style.RESET_ALL + Fore.CYAN + " - %(message)s (%(filename)s:%(lineno)d)",
        logging.INFO: Style.RESET_ALL + Style.DIM + "%(asctime)s - %(name)s - " + Style.RESET_ALL + Fore.YELLOW + Back.BLUE + Style.BRIGHT + " %(levelname)s " + Style.RESET_ALL + Fore.GREEN + " - %(message)s (%(filename)s:%(lineno)d)",
        logging.WARNING: Style.RESET_ALL + Style.DIM + "%(asctime)s - %(name)s - " + Style.RESET_ALL + Fore.BLUE + Back.YELLOW + " %(levelname)s " + Style.RESET_ALL + Fore.YELLOW + " - %(message)s (%(filename)s:%(lineno)d)",
        logging.ERROR: Style.RESET_ALL + Style.DIM + "%(asctime)s - %(name)s - " + Style.RESET_ALL + Fore.WHITE + Back.RED + Style.BRIGHT + " %(levelname)s " + Style.RESET_ALL + Fore.RED + Style.BRIGHT + " - %(message)s (%(filename)s:%(lineno)d)",
        logging.CRITICAL: Style.RESET_ALL + Style.DIM + "%(asctime)s - %(name)s - " + Style.RESET_ALL + Fore.WHITE + Back.RED + Style.BRIGHT + " %(levelname)s " + Style.RESET_ALL + Fore.RED + Style.BRIGHT + " - %(message)s (%(filename)s:%(lineno)d)",
    }

    def format(self, record):
        if isinstance(record.msg, Iterable) and not isinstance(record.msg, str):
            record.msg = json.dumps(record.msg, indent=4, ensure_ascii=False)
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)