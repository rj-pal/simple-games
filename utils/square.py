from enum import Enum
from colorama import Fore, Style

class Square(Enum):
    """Represents a single square as ASCII String."""
    BLANK = ["            "] * 5
    
    R = [
        Fore.RED + "    ****    " + Style.RESET_ALL, 
        Fore.RED + "  ********  " + Style.RESET_ALL, 
        Fore.RED + " ********** " + Style.RESET_ALL, 
        Fore.RED + "  ********  " + Style.RESET_ALL,
        Fore.RED + "    ****    " + Style.RESET_ALL
    ]
    
    Y = [
    Fore.LIGHTYELLOW_EX + "    ****    " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + "  ********  " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + " ********** " + Style.RESET_ALL, 
    Fore.LIGHTYELLOW_EX + "  ********  " + Style.RESET_ALL,
    Fore.LIGHTYELLOW_EX + "    ****    " + Style.RESET_ALL
   ]
    
    B = [
    Fore.BLUE + "    ****    " + Style.RESET_ALL, 
    Fore.BLUE + "  ********  " + Style.RESET_ALL, 
    Fore.BLUE + " ********** " + Style.RESET_ALL, 
    Fore.BLUE + "  ********  " + Style.RESET_ALL,
    Fore.BLUE + "    ****    " + Style.RESET_ALL
   ]

    O = [
        "    *  *    ", 
        "  *      *  ", 
        " *        * ", 
        "  *      *  ", 
        "    *  *    "
    ]
    X = [
        "  *       * ", 
        "    *   *   ", 
        "      *     ", 
        "    *   *   ", 
        "  *       * "
    ]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Name: {self.name}\nValue: {self.value}'
    
