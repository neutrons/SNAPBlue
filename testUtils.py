import sys
import time
import importlib
sys.path.append("/SNS/SNAP/shared/code/SNAPBlue")
import blueUtils as blue
import SNAPStateMgr as ssm
importlib.reload(blue)
importlib.reload(ssm)
from mantid import config
config.setLogLevel(3, quiet=True)
t0 = time.time()

isLite = True

# create State
# ssm.createState(64434,
#     isLite)
#propagate difcal

blue.propagateDifcal(64431,
    isLite,
    propagate=True)

print(f"\n Complete! execution took: {time.time()-t0:.1f}s")