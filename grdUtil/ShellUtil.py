from os import environ

from .ShellType import ShellType


def getCurrentShellType() -> ShellType:
    """
    Gets type fo current shell (Windows CMD, PowerShell, Bash...).
    
    Returns:
        ShellType: type of shell else None.
    """
    
    if("shell" in environ and "bash" in environ["shell"]):
        return ShellType.BASH
    elif("pathext" in environ and ".cpl" in environ["pathext"]):
        return ShellType.POWERSHELL
    elif("pathext" in environ):
        return ShellType.CMD
    
    return None
