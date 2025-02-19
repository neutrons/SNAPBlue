# `indexStates`

## Overview

This is a simple utility that reports all available states (those that have been instantiated) and their current calibration status. 

typical usage is: 

```
import sys
sys.path.append("/SNS/SNAP/shared/code/SNAPBlue")

import blueUtils as blue

blue.indexStates()
```
which gives output that looks like: 
```
 StateID        | Desc.                   | Status  |No. difcals|No. nrmcals|
b358bc9ca6f9f3de| -65.5: 105.0: 3.0: 30: 1| UNCALIB |     0     |    0      |
d1946b4615db2d4e| -50.0:  90.0: 6.4: 60: 2| UNCALIB |     0     |    0      |
b810d6da5d4af06e| -65.5: 105.0: 1.8: 60: 1| PARTIAL |     0     |    2      |
ffefaa93ccb23678| -65.5: 105.0: 2.1: 60: 2| PARTIAL |     0     |    1      |
685b9dc2fd699205| -65.5:  90.0: 6.4: 60: 1| PARTIAL |     0     |    1      |
0e04feff89cf95f3| -90.0:  66.0: 6.4: 60: 1| PARTIAL |     0     |    1      |
c073719d9101e8f2| -65.5: 105.0: 6.4: 60: 1| PARTIAL |     0     |    1      |
17fcca13ece67241| -50.0:  90.0: 6.4: 60: 1| PARTIAL |     0     |    1      |
74370ebaa23119db| -65.5:  90.0: 2.1: 60: 1| *CALIB* |     1     |    1      |
702ba297516db7bf| -50.0: 105.0: 6.4: 60: 1| *CALIB* |     8     |    3      |
e1d38f0788481997| -76.0: 105.0: 2.1: 60: 1| *CALIB* |     3     |    3      |
04bd2c53f6bf6754| -65.5: 105.0: 2.1: 60: 1| *CALIB* |     1     |    1      |
27588df26158e93c| -50.0: 105.0: 2.1: 60: 1| *CALIB* |     3     |    1      |
3c7b8c841d10a16b| -90.0:  66.0: 2.1: 60: 1| *CALIB* |     1     |    1      |
ce8a5e1e29a1de97| -50.0:  90.0: 2.1: 60: 1| *CALIB* |     1     |    1      |
```

TODO: probably useful to add run numbers of latest calibration runs (when they exist)??

## `isLite`

The only optional parameter is `isLite`, which defaults to True.