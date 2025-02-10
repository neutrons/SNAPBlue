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
# from snapred.backend.data import LocalDataService as lds
from snapred.backend.dao.request.FarmFreshIngredients import FarmFreshIngredients
from snapred.backend.service.SousChef import SousChef


def loadSNAPInstPrm():

  #TODO: remove hardcoding of this location
   
  instPrmJson = '/SNS/SNAP/shared/Calibration_testing/SNAPInstPrm.json'

  with open(instPrmJson, "r") as json_file:
    instPrm = json.load(json_file)
  return instPrm 

def checkStateExists(stateID,powderHome):

  statePath = f"{powderHome}{stateID}/"
  # print(statePath)
  # print("exists:",os.path.exists(statePath))
  return os.path.exists(statePath) 
 
def checkCalibrationStatus(stateID,powderHome,isLite,calType):

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
      indexPath = f"{powderHome}/{stateID}/lite/{subFolder[calType]}/{jsonName[calType]}"
  else:
      indexPath = f"{powderHome}/{stateID}/native/{subFolder[calType]}/{jsonName[calType]}"

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

  return calStatus

def detectorConfig(stateDict):

    #returns a unique ID for a given detector config. It only cares about
    #detector angles

    import hashlib

    #stateDictString can be two different things depending on how it's made ugh... 
    #manage this:
    if type(stateDict)==str:
        stateDict = json.loads(stateDict) #convert to dict 
        detectorDict = {
            "vdet_arc1" : stateDict["vdet_arc1"],
            "vdet_arc2" : stateDict["vdet_arc2"]}
    else:
        detectorDict = {
            "vdet_arc1" : stateDict["arc"][0],
            "vdet_arc2" : stateDict["arc"][0]}
        
    hasher = hashlib.shake_256()
    decodedKey = json.dumps(detectorDict).encode('utf-8')
    hasher.update(decodedKey)
    hashedKey = hasher.digest(4).hex()

    return hashedKey

def availableStates():

    #list of non state folders within main calibration directory (just one atm)
    powderHome = Config['instrument.calibration.home']+"/Powder/"
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

    # print(stateParamsJson["instrumentState"]["detectorState"])
    return stateParamsJson["instrumentState"]["detectorState"]