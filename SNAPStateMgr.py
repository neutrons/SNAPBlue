# SNAPStateManager is a module for holding convenient functions for managing SNAP instrument states
#
# TODO: contains functions copied from "stateFromRun.py" at some point should edit that script to
# point to this module

import h5py
import sys
import json
from datetime import datetime
import os
import sys
# from finddata import cli
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# SNAPRed imports TODO: clean up what is not needed...
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from snapred.backend.dao.ingredients.ArtificialNormalizationIngredients import ArtificialNormalizationIngredients
from snapred.backend.dao.request import ReductionExportRequest
from snapred.backend.dao.request.ReductionRequest import ReductionRequest
from snapred.backend.data.DataFactoryService import DataFactoryService
from snapred.backend.error.ContinueWarning import ContinueWarning
from snapred.backend.recipe.ReductionRecipe import ReductionRecipe
from snapred.backend.service.ReductionService import ReductionService
from snapred.backend.dao.indexing.Versioning import Version, VersionState
from snapred.meta.mantid.WorkspaceNameGenerator import WorkspaceNameGenerator as wng
from snapred.meta.Config import Config
from snapred.backend.data import LocalDataService as lds
from snapred.backend.dao.request.FarmFreshIngredients import FarmFreshIngredients
from snapred.backend.service.SousChef import SousChef

class SNAPHome():
   # main definition of calibration directory
   def __init__(self):
      self.calib = Config['instrument.calibration.home']
      self.powder = self.calib + "/Powder/"

def loadSNAPInstPrm():

  home = SNAPHome()
  instPrmJson = home + 'SNAPInstPrm.json'

  with open(instPrmJson, "r") as json_file:
    instPrm = json.load(json_file)
  return instPrm 

def stateDef(runNumber):
    #returns a list, first entry is stateID, second is dictionary of state parameters
    
    dataFactoryService = DataFactoryService()
    if type(runNumber) != str:
            runNumber=str(runNumber)

    stateID,stateDictStr = dataFactoryService.constructStateId(runNumber)
    stateDict = json.loads(stateDictStr)
    print("ssm stateDef function returns this dict: ",stateDict)

    return [stateID,stateDict]

def checkStateExists(stateID):
  
  home = SNAPHome()
  powderHome = home.powder
  statePath = f"{powderHome}{stateID}/"

  return os.path.exists(statePath) 
 
def checkCalibrationStatus(stateID,isLite,calType):

    home = SNAPHome()
    powderHome = home.powder
    #dictionary to hold status
    calStatus = {
    "stateID":stateID,
    "calibrationType":calType
    }

    #dictionaries to build paths for difference cases
    subFolder = {"difcal":'diffraction',
                "normcal":"normalization"}

    jsonName = {"difcal":"CalibrationIndex.json",
                "normcal":"NormalizationIndex.json"}

    firstIndex = {"difcal":1,
                 "normcal":0}    #annoyingly these are different

    #build paths
    if isLite:
        indexPath = f"{powderHome}{stateID}/lite/{subFolder[calType]}/{jsonName[calType]}"
    else:
        indexPath = f"{powderHome}{stateID}/native/{subFolder[calType]}/{jsonName[calType]}"

    #first check if index exists
    if not os.path.isfile(indexPath):
        calStatus["isCalibrated"] = False
        calStatus["numberCalibrations"] = 0
        calStatus["latestCalibration"] = "never"
        
        return calStatus

    #if index exists, read it    
    f = open(indexPath)
    calIndex = json.load(f)
    f.close()    

    if len(calIndex) > firstIndex[calType]:
        calStatus["isCalibrated"] = True
        calStatus["NumberCalibrations"] = len(calIndex)-1
        ts = calIndex[-1]["timestamp"]
        calStatus["latestCalibration"] = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
        calStatus["calibRuns"] = []
        for entry in calIndex[firstIndex[calType]:]:
            calStatus["calibRuns"].append(entry["runNumber"])

    else:
        calStatus["isCalibrated"] = False
        calStatus["numberCalibrations"] = 0
        calStatus["latestCalibration"] = "never"

    calStatus["indexPath"] = indexPath
    return calStatus

def detectorConfig(stateDict):

    #returns a unique ID for a given detector config. It only cares about
    #detector angles

    import hashlib

    print("detectorConfig:",stateDict)

    detectorDict = {
            "vdet_arc1" : stateDict["vdet_arc1"],
            "vdet_arc2" : stateDict["vdet_arc2"]}
        
    hasher = hashlib.shake_256()
    decodedKey = json.dumps(detectorDict).encode('utf-8')
    hasher.update(decodedKey)
    hashedKey = hasher.digest(4).hex()

    return hashedKey
   

def availableStates():

    #list of non state folders within main calibration directory (just one atm)
    home = SNAPHome()
    powderHome = home.powder
    nonStateFolders = ['PixelGroupingDefinitions']

    #create list of state folders
    stateFolderList = [f for f in os.listdir(powderHome) if os.path.isdir(os.path.join(powderHome,f))]
    for nonState in nonStateFolders:
        stateFolderList.remove(nonState)

    return stateFolderList

def pullStateDict(stateIDString):

    #given a stateID as a string, will return a dictionary of state parameters

    stateSeedDir = f"{Config['instrument.calibration.home']}/Powder/{stateIDString}/lite/diffraction/v_0000/"
    stateParamsJson = stateSeedDir + "/CalibrationParameters.json"

    f = open(stateParamsJson)
    stateParamsJson = json.load(f)
    f.close()

    # This returns dictionary with different keys from defState. Convert the keys to 
    # match. Also, need to apply rounding that is used when generating state info.

    initDict = stateParamsJson["instrumentState"]["detectorState"]

    arc1 = float(round(initDict["arc"][0]*2)/2)
    arc2 = float(round(initDict["arc"][1]*2)/2)
    wav = float(round(initDict["wav"],1))
    freq = int(round(initDict["freq"] ))
    pos = int(initDict["guideStat"])

    finalDict = {"vdet_arc1" : arc1,
                 "vdet_arc2" : arc2,
                 "WavelengthUserReq" : wav,
                 "Frequency" : freq,
                 "Pos" : pos 
                 }

    # print(stateParamsJson["instrumentState"]["detectorState"])
    return finalDict

def autoStateName(stateDict):

    print(stateDict)

    arcStr1 = f"{stateDict['vdet_arc1']:.1f}".rjust(6)
    arcStr2 = f"{stateDict['vdet_arc2']:.1f}".rjust(6)
    lamStr = f"{stateDict['WavelengthUserReq']:.1f}".rjust(4)
    freqStr = f"{stateDict['Frequency']:.0f}".rjust(3)
    guideStr = str(stateDict['Pos']).rjust(2)
    name = f"{arcStr1}|{arcStr2}|{lamStr}|{freqStr}|{guideStr}"
    return name

def createState(runNumber,isLite,hrn='none'):

    stateID,stateDict = stateDef(runNumber)

    #only do anything if state doesn't exist
    if checkStateExists(stateID):
        print(f"state: {stateID} already exists. Nothing to do")
    else: 
        if hrn == 'none':
            hrn = autoStateName(stateDict) # if not specified, humanReadableName will be auto generated.

        print(f"Creating state {stateID} with name {hrn}")
        localDataService = lds.LocalDataService()
        localDataService.initializeState(str(runNumber), isLite, hrn)