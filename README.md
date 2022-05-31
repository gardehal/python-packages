# python-packages
 Collection of general Python functions.

## Install locally

1. $ `cd [path to this folder]`
1. Install PipReqs to install all dependencies 
    - $ `python -m pip install pipreqs` 
    - $ `pipreqs .`
    - $ `python -m pip install -r requirements.txt`
1. $ `python pip install .`
1. Check installed packages
    - $ `python pip list`
1. Purge (external) packages
    - $ `python -m pip cache purge`

## TODO

- update shouldn't update soft deleted unless option to include is true
- logutil, with log level and option to also print
- asTable by column
- asTable left-adjust text (default), center text, right-adjust text in cells
- update old methods with proper docstrings
- import more common functions/exceptions
- grdException vs grdExceptions - with S is wrong but not mentioned anywhere? chahce issue, attempted to delete all packages but still there?
- debug print, if it can automatically get the name of calling function, use printS default warning, debug arg, format: "DEBUG: func - message"
- update debugs in try/catch with printStack (e.g. jsonRepo)
- do something so colors show in MS cmd, powershell, etc.
- import still weird, should be .PrintUtil, not grdUtil.PrintUtil but doesn't always work..
- delete WebUtil?