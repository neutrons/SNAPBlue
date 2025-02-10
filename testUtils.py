import sys
import time
import importlib
sys.path.append("/SNS/SNAP/shared/code/SNAPBlue")
import blueUtils as blue
importlib.reload(blue)
from mantid import config
config.setLogLevel(3, quiet=True)
t0 = time.time()

blue.propagateDifcal(64413,
    isLite=True,
    propagate=False)

print(f"\n Complete! execution took: {time.time()-t0:.1f}s")