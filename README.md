# python-packages / GrdUtil

Collection of general Python functions.

[![Publish to PyPI](https://github.com/gardehal/python-packages/actions/workflows/publish.yml/badge.svg)](https://github.com/gardehal/python-packages/actions/workflows/publish.yml)
[![GitHub Release](https://img.shields.io/github/release/gardehal/python-packages.svg)]()
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/gardehal/python-packages/blob/main/LICENSE)


## Install locally

[PyPi project](https://pypi.org/project/grdutil/)

Install using pip
- $ `pip install grdutil`
- In python files: `from GrdUtil import *` 

Install from files locally
- $ `cd [path to this folder]`
- $ `pip cache purge` (may help if old packages are cached)
- $ `pip install .`

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
