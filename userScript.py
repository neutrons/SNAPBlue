import sys
import importlib
sys.path.append("/SNS/SNAP/shared/Malcolm/code/SNAPBlue")
import blueUtils as blue
importlib.reload(blue)
from mantid import config
config.setLogLevel(3, quiet=True)

#to do a simple reduction of run 61991

blue.reduceSNAP(61991,sampleEnv="PE_001") 

