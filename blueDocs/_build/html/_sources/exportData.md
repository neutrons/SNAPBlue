# `exportData`

## Overview

Once data have been reduced, they are available as mantid workspaces and are also automatically saved as `.nxs` files along with a detailed `reductionRecord` that captures all parameters used in reduction. In addition, it is necessary to export data in appropriate formats for subsequent analysis, `exportData` enables this.

By default, `exportData` will output all available reduced data workspaces in three pre-defined formats:

* `gsa` GSAS and GSAS2 format output. Different pixel groups are stored as separate "banks" in the output file
* `xye` TOPAS and FULPROF format output. Different pixel groups are stored as separate output files
* `csv` PARIALLY IMPLEMENTED: currently the output is called `.csv` but is actually tab delineated. Nevertheless, this provides a simple ascii format with the reduced data as a function of d-spacing

As noted in the description of `reduce` multiple reductions of the same run are supported by adding a suffix with a timestamp to the end of a mantid workspace name. However, by default, only the most recent workspace will be exported and the timestamp will _not_ be used in the exported filename. It is possible to override this if necessary (see below) if refinement of different reduction treatements is useful (e.g. to test different attenuation corrections)

Finally, it is intended to automatically link outout files to corresponding templates and or `instprm` files (in the case of GSAS). This work is on going, however, already `exportData` will automatically create a "dummy" gsas `instprm file` by default. This file is given the same file name (but a different extension) to the exported GSAS/GSAS2 data and it will be automatically used when loading the data (`.gsa` file) into GSAS2.

```{warning}
At present the autocreated GSAS2 `.instprm` file should be viewed as an approximately starting point. It is _not_ a fully calibrated file! Work is ongoing to figure out how to propagate existing, manually calibrated `instPrm` files however, since these are needed for each state and for each pixel group within a state, some kind of automated solution is desirable. This isn't trivial to realise though...
```
```{note}
At present, export does not track state or `Lite` mode. This can be added as an option if it's needed
```

## Export locations

The data are exported to the `IPTS/shared` directory according to the reduced run number (is an override needed for this?) and a subdirectory in their called `/SNAPRed/export`. Within this subdirectory separate folders will be created for each requested export format and, within these, separate folders for each pixel grouping scheme used during reduction 

e.g.

```
/SNS/SNAP/IPTS-34952/shared/SNAPRed/export/gsa/column/
```

## `exportFormats`

The desired export formats can be specified using this parameter. Its value is in the form of a list of string, each supported string is a 3 character as described in the overview. The default value of this parameter is ['gsa','xye','csv'] and all three formats will be created. 

If a different format needs to be supported, just let Malcolm know.

## `latestOnly`

Defaulting to `True` this ensures that only the latest reduced workspace is exported and that it's timestamp is excluded from the exported filename. If, instead, this is set `False` _all_ existing reductions of a given run are exported and their filenames will include their timestamps.

## `gsasInstPrm`

Defaults to `True`. This will export a dummy instPrm to the gsas export folder with the same name as the exported data.