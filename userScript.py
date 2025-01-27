import sys
import importlib
sys.path.append("/SNS/SNAP/shared/Malcolm/code/SNAPBlue")
import blueUtils as blue
importlib.reload(blue)
from mantid import config
config.setLogLevel(3, quiet=True)

#if state doesn't exist, SNAPRed will fail

#example run where state exists but has no difcal or normcal

# blue.reduceSNAP(63424,
#     continueNoVan=True,
#     continueNoDifcal=True
#     )    

#example run where difcal exists but normcal doesn't

# blue.reduceSNAP(58882,
#    continueNoVan=True
#    ) 
    

# #example run with full calibration
# blue.reduceSNAP(61991,
#     )

#example using override yml
blue.reduceSNAP(61991,
    YMLOverride = "/SNS/SNAP/shared/Malcolm/code/SNAPBlue/override.yml", # set to retain unfocussed ws
    pixelMaskIndex = 2
    )

