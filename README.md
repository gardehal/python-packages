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

- asTable should have an option to not use labels, data as columns, not rows - use lists issue?
- logutil, missing JSON logging
- do something so colors show in MS cmd, powershell, etc.
- import, cannot use relative path like "..grdUtil.x" in grdService, or "..grdException.x" anywhere. Options? Always have to use self package?
- BaseService.baseRepository should be generic repo type, not locked to LocalJson, and be injectable
- delete WebUtil?
- convert DatetimeObject, FilePathObject to util functions 
- json datetimes defaults to string, could be fixed? - seems not, despite hinting like "created: datetime", if the data is null, the type() is always NoneType. Alterative1: Can hack with using a default method on every model, but its slow and unreliable. Alternative2: wrap all datetimes and default-to-string values in object like { pythonType: "datetime", value: "2022-..." }. Requires a lot of refactoring from current...