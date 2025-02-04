import sys
import importlib
sys.path.append("/SNS/SNAP/shared/code/SNAPBlue")
import blueUtils as blue
importlib.reload(blue)
from mantid import config
config.setLogLevel(3, quiet=True)

#IF STATE DOESN'T EXIST SNAPRED WILL FAIL!!!!!!!!!
# STATE CAN BE CREATED WITH THE TEST PANEL (YOU JUST NEED A RUN NUMBER)

# #example run with full calibration the "Happy Path"

# blue.reduceSNAP(61991
#     )

#example run where state exists but has no difcal or normcal

# blue.reduceSNAP(63424,
#     continueNoVan=True,
#     continueNoDifcal=True
#     )    

#example run where difcal exists but normcal doesn't

# blue.reduceSNAP(58882,
#    continueNoVan=True
#    ) 

#example using override yml

# blue.reduceSNAP(61991,
#     YMLOverride = "/SNS/SNAP/shared/Malcolm/SNAPBlue/override.yml", # set to retain unfocussed ws
#     pixelMaskIndex = [2]
#     )

#example of (verbose) inspection of parameters but not actually reducing anything

blue.reduceSNAP(58882,
    verbose=True,
    continueNoVan=True,
    continueNoDifcal=True,
    reduceData=False
    )

