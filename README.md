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

- astable, look though dataArray and find longest instance for each column, send as argument to astablerow as maxwidth or something
- prinutil as table/row, use + in corners, optional alter different colour on rows, input as columns, not just rows, option to use deviding rows
- base class for service
- update old methods with proper docstrings
- import more common functions/exceptions