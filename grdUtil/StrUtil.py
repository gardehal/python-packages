
from typing import List


def maxLen(string: str, maxLen: int = 20, continuedPostfix: str = "..") -> str:
    """
    Return a string s with maximum length of maxLen or just the string, whatever is shortest.

    Args:
        s (str): String to maxLen.
        maxLen (int, optional): Maximum length of final string. Defaults to 20.
        continuedPostfix (str, optional): Whatever value to show string is cut off/shortened. Set None to disable this. Defaults to "..".
        
    Returns:
        str: String s that is shorter or the same length as maxLen.
    """
        
    s = string
    if(len(s) > maxLen):
        s = s[0:maxLen]
    
    if(continuedPostfix != None and len(s) > len(continuedPostfix)):
        return s[0:maxLen-len(continuedPostfix)] + continuedPostfix
    
    return s

def joinAsString(*args) -> str:
    """
    Join all args as string and return the resulting single string.
    
    Args:
        args (*args): Any values to stringify.

    Returns:
        str: Joined string of all args.
    """

    result = ""
    for a in args:
        if(isinstance(a, List)):
            a = joinAsString(*a)
        
        result += str(a)
    
    return result