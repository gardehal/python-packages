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

## Errors

- Colours not showing in printX functions, getting "←[92m" or similar codes at start of lines
  - Make sure you're using a shell that can render colours, like Git Bash
  - Enter $ `export FORCE_COLOR=true` in the shell and close, then open the shell

## TODO

- fix init of FPO if file doesnt exist but path is valid
- fix pylance not recognizing this, temp fix by adding project to ctrl+, then extrapaths
- respect max width of terminal window
- asTable should have an option to not use labels, data as columns, not rows - use lists issue?
- logutil, missing JSON logging
- do something so colors show in MS cmd, powershell, etc.
- import, cannot use relative path like "..grdUtil.x" in grdService, or "..grdException.x" anywhere. Options? Always have to use self package?
- BaseService.baseRepository should be generic repo type, not locked to LocalJson, and be injectable
- delete WebUtil?
- convert DatetimeObject, FilePathObject to util functions 
- json datetimes defaults to string, could be fixed? - seems not, despite hinting like "created: datetime", if the data is null, the type() is always NoneType. Alterative1: Can hack with using a default method on every model, but its slow and unreliable. Alternative2: wrap all datetimes and default-to-string values in object like { pythonType: "datetime", value: "2022-..." }. Requires a lot of refactoring from current...

- input validation and read improvement
  - define a flag with aliases
  - set up some positional argument matrix including positional arg name, index, type and nullability, max value min value, max len, min len
  - when a flag is hit, return some key value, enum?, and dict? with positional arguments
  - if a enum or something is required type, universal way of casting? non primitives casting???
  - input null as None, if "None" is wanted as a string, double quote it?
  - validate missing order numbers, starting at 0
  - init should happen, then add lines of args
  - Args(flag = "-", namedArgumentDelim = ":")
  - valueSubArgs = SubArg(name = "value", order = 0, aliases = ["value", "v"], type = int, nullable = False, max = 1000, min = 0)
  - unitsSubArgs = SubArg(name = "unit", order = 1, aliases = ["unit", "u", "measurement", "m"], type = str, nullable = True, maxLen = 6, minLen = 0)
  - Args.addArg(name = "Height", hitValue = DimensionEnum.HEIGHT, aliases = ["h", "height", "up"], subArgs = [valueSubArgs, unitsSubArgs], printErrors = True)
  - results = Args.validate(inputString)
  - argResults(flagName, flagHitValue, flagIndex/order from input, subargsdict? obj?, )
    - The following syntax expected as input
      - Main.py -h 100 
      - Main.py -height 100 
      - Main.py -height 100 cm 
      - Main.py -height value:100 unit:cm 
      - Main.py -height value : 100 unit : cm 
      - Main.py -height value:100
      - Main.py -height 100 99 ...........  (99 is a str technically.., if unit was an enum or something, this would fail.. custom value mapping as input per subarg?)
    - incorrect input, should return errors from validation since its True
      - Main.py height .. (missing flag indicator) 
      - Main.py -height .. (missing required positional arg 0, "value") 
      - Main.py -height -width value:100 .. (missing required positional arg 0, "value" on first flag) 
      - Main.py -height asd .. (expected required positional arg 0, "value" to be int) 
      - Main.py -height 999999 .. (expected required positional arg 0, "value" to be less than 1000)
      - Main.py -height -1 .. (expected required positional arg 0, "value" to be more than -1)
      - Main.py -height 100 aaaaaaaaaaaa .. (expected positional arg 1, "unit" to be shorter than 6 chars)
    - unsure
      - Main.py -height unit:cm value:100 .... (if they're named, order shouldnt matter as long as the required are there and they're all named?)
      - Main.py -height 1 2 3 4 unit:cm value:100 .... (positional and named mixed, but all required are ok, prefer named)