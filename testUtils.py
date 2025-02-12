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
# 
blue.propagateDifcal(64431,
    isLite,
    propagate=True)
 
# cr_old = ssm.loadCalibrationRecord(64431,isLite,3)
# cr_new = ssm.loadCalibrationRecord(64433,isLite,0)
# 
# print("old version: ",cr_old.version)
# print("new version: ",cr_new.version)
# print("updating new version...")
# cr_new.version = 1
# print("new version: ",cr_new.version)
# 
# print("\nnew cr contents:")
# for item in cr_new:
#     print("\n",item)
# 
# print("\nold cr contents:")
# for item in cr_old:
#     print("\n",item)
 

print(f"\n Complete! execution took: {time.time()-t0:.1f}s")