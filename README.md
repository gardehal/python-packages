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

- logutil, missing JSON logging
- do something so colors show in MS cmd, powershell, etc.
- import, cannot use relative path like "..grdUtil.x" in grdService, or "..grdException.x" anywhere. Options? Always have to use self package?
- BaseService.baseRepository should be generic repo type, not locked to LocalJson, and be injectable
- delete WebUtil?
- convert DatetimeObject, FilePathObject to util functions 
- json datetimes defaults to string, could be fixed?