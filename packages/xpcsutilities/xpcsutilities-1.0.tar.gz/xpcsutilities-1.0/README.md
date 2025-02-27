# XPCSUtilities

Display XPCS result files from ESRF ID02 beamline, perform basic operations on results, basic fitting tools.

![XPCSUtilities logo](xpcsutilities/xpcsutilities-logo.svg)

## Installation

**System requirements**

XPCSUtilities works only with python version >= 3.6. Pip will take care of all dependencies. Dependency list can be showed in setup.py file.

It is **strongly** recommended to install XPCSUtilities in a dedicated virtual environment (virtualenv) to prevent any library version mismatch issue.

```bash
pip install https://gitlab.esrf.fr/id02/xpcsutilities/-/archive/main/xpcsutilities-main.zip
```
## python package

This package can be used in your own analysis script to read data directly from the hdf5/NxXPCS format.

```python

from xpcsutilities.tools.result_file import XPCSResultFile

with XPCSResultFile('my_filename.h5') as fd: # Always use into a with statement!
    
    print(fd.analysis_keys)
    
    lag, cf, std = fd.get_correlations('full') # Use here the right analysis key

    cf, lag, age = fd.get_ttcf('full', 3) # Return the TTCF of ROI#3 in the 'full' analysis

```


## GUI

To launch the program:
```bash
XPCSUtilities
```
If installed in an virtual environement, load the environement first.

On the left panel, you'll find the files of current working folder. You can select any files that you want to display on the right panel. Current working folder is set by the "Set working folder" button. Files are filtered according to the wildcard filter below the button. Multiple filters can be set by using a comma-separated list if wildcards. New files are automatically displayed on the list.

The plot button below display the selected file(s) in current tab.

### SAXS 1D

This tab display the radial average of the time averaged 2D pattern. This graphs also shows the correlation ranges.

### SAXS 2D

This tab display the time averaged 2D pattern. Mask and q-mask can be displayed as overlay.

- Corrected: raw 2D pattern corrected by flatfield file
- Raw: Time average of all 2D patterns recorded
- Averaged: 2D pattern reconstructed from 1D curve

### Correlations

This tab display the correlation functions

### TTCF

This tab display the Two Time Correlation Functions

### Fit

This tab provide basic fitting tools. Several models can be used togethers to fit the data. 
