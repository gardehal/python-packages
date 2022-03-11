import os

import psutil

from grdUtil.ShellType import ShellType


def getCurrentShellType() -> ShellType:
    """
    Gets type fo current shell (Windows CMD, PowerShell, Bash...).
    
    Returns:
        ShellType: type of shell else None
    """
    
    _cliName = psutil.Process(os.getppid()).name().lower()
    
    if("cmd" in _cliName):
        return ShellType.CMD
    elif("powershell" in _cliName):
        return ShellType.POWERSHELL
    elif("bash" in _cliName):
        return ShellType.BASH
    
    return None
