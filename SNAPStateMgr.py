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
import copy
import shutil
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
from snapred.backend.data.LocalDataService import LocalDataService
from snapred.backend.dao.indexing.IndexEntry import IndexEntry


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
    "calibrationType":calType,
    "isLite":isLite
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

    mostRecentCalibTS = 0
    mostRecentCalib = 0
    if len(calIndex) > firstIndex[calType]:
        calStatus["isCalibrated"] = True
        calStatus["numberCalibrations"] = len(calIndex)-1
        ts = calIndex[-1]["timestamp"]
        calStatus["latestCalibration"] = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
        calStatus["calibRuns"] = []
        
        for i,entry in enumerate(calIndex[firstIndex[calType]:]):
            calStatus["calibRuns"].append(entry["runNumber"])
            if entry["timestamp"]>= mostRecentCalibTS:
                mostRecentCalibTS = entry["timestamp"]
                mostRecentCalib = i + 1 #zeroth index is not counted

    else:
        calStatus["isCalibrated"] = False
        calStatus["numberCalibrations"] = 0
        calStatus["latestCalibration"] = "never"

    calStatus["indexPath"] = indexPath
    calStatus["calibIndex"] = calIndex #list of calibrations
    calStatus["mostRecentCalib"] = calIndex[mostRecentCalib] #dict for most recent calibration
    return calStatus

def detectorConfig(stateDict):

    #returns a unique ID for a given detector config. It only cares about
    #detector angles

    import hashlib

    # print("detectorConfig:",stateDict)

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

def copyDifcal(refCal,cal,propagate=False): # refCal and Cal are CalibrationStatus dictionaries generated by checkCalibrationStatus


    refCalDict = refCal["mostRecentCalib"]
    calDict = cal["mostRecentCalib"]
    seedRun = refCalDict["runNumber"]
    destRun = cal["calibIndex"][0]["runNumber"] #need instantiating run number to ensure it matches state
 
    print(f"\nReference calibration to be copied from state: {stateDef(seedRun)[0]}")
    for key in refCalDict:
        print(f"{key} : {refCalDict[key]}")
    print(f"\nMost recent calibration is version {calDict['version']} in destination state: {stateDef(destRun)[0]} ")

    newIE = IndexEntry(version=calDict["version"]+1,
        runNumber=calDict["runNumber"],
        useLiteMode=refCal["isLite"],
        appliesTo = refCalDict["appliesTo"],
        comments = f"(copied from run:{refCalDict['runNumber']} version:{refCalDict['version']})  original comments: {refCalDict['comments']}",
        author = f"{refCalDict['author']} (original author)",
        timestamp = refCalDict['timestamp']
        )
    
    #build directory name and create directory
    refVersion = refCal["mostRecentCalib"]["version"]
    oldCalibDir = f"{os.path.dirname(refCal['indexPath'])}/v_{str(refVersion).zfill(4)}"
    newCalibDir = f"{os.path.dirname(cal['indexPath'])}/v_{str(newIE.version).zfill(4)}"

    newCalibDir = newCalibDir# + "_test"

    if propagate: 
        try:
            print(f"propagation requested, new calibration will be version {newIE.version}") 
            shutil.copytree(oldCalibDir,newCalibDir)
            os.remove(f"{newCalibDir}/CalibrationRecord.json") # it will be replaced with franken CR
            os.remove(f"{newCalibDir}/CalibrationParameters.json")
            
            #need to manually change version in file names
            reVersionDifcal(oldCalibDir,newCalibDir,seedRun,destRun)
            print(" - Calibration folder has been copied and reVersioned")
               
        except:
            print(f"Error calibration directory already exists: {newCalibDir}")
            print("can\'t copy here!")
            return

    if propagate:
        
        #need to update calibrationRecord with a "frankenRecord" a merging of relative
        #parts of two calibrationRecords

        newCR = frankenRecord(seedRun=seedRun,
            seedVersion=refVersion,
            destRun = destRun, #only used to define destination state
            destVersion = newIE.version,
            isLite=cal["isLite"],
            printRecord=False #used for debugging
            )
        
        saveCalibrationRecord(newCR,newIE,destRun)
        print(" - Calibration Record, Parameters and Index have been updated")

    if not propagate:
        print("Calibration was requested to not be propagated")

    return

def reVersionDifcal(seedDir,destDir,seedRun,destRun):

    # this function will conduct various operations to update version info between
    # a copied difcal folder and the original seed folder

    seedVersion = seedDir.split('/')[-1].split('_')[1]
    destVersion = destDir.split('/')[-1].split('_')[1]

    #rename one at a time:

    seedRun = str(seedRun).zfill(6)
    destRun = str(destRun).zfill(6)


    os.rename(f"{destDir}/dsp_column_{seedRun}_v{seedVersion.zfill(4)}.nxs.h5",
              f"{destDir}/dsp_column_{destRun}_v{destVersion.zfill(4)}.nxs.h5")
    
    os.rename(f"{destDir}/diffract_consts_{seedRun}_v{seedVersion.zfill(4)}.h5",
              f"{destDir}/diffract_consts_{destRun}_v{destVersion.zfill(4)}.h5")
    
    os.rename(f"{destDir}/diagnostic_column_{seedRun}_v{seedVersion.zfill(4)}.nxs.h5",
              f"{destDir}/diagnostic_column_{destRun}_v{destVersion.zfill(4)}.nxs.h5")

def loadCalibrationRecord(runNum,isLite,version):

    #read existing calibration record from disk

    if type(runNum) != str:
        runNum=str(runNum)    
    
    localDataService=LocalDataService()
    cr = localDataService.readCalibrationRecord(runNum,isLite,version)

    return cr

def saveCalibrationRecord(calibrationRecord,indexEntry,destinationRun):

    localDataService=LocalDataService()
    localDataService.writeCalibrationRecord(calibrationRecord,indexEntry)

    return

def frankenRecord(seedRun,
    seedVersion, destRun, destVersion, isLite, printRecord=False):

    #this will copy the calibration record (CR) corresponding to the state associated with "seedRun"
    #and with version "seedVersion". Then it will get the default calibration record ("v_0000")
    #corresponding to state of destRun. isLite must be the same for both.
    #
    #a copy is made of the seed CR is made, then its attributes updated.
    # The frankenCR is returned

    seedCR = loadCalibrationRecord(seedRun,isLite,seedVersion)

    destDefaultCR = loadCalibrationRecord(destRun,isLite,0)
    franken = copy.deepcopy(seedCR)

    franken.version = destVersion
    franken.runNumber = destRun
    franken.calculationParameters.version = destVersion
    franken.calculationParameters.instrumentState = destDefaultCR.calculationParameters.instrumentState
    franken.calculationParameters.seedRun = destDefaultCR.calculationParameters.seedRun
    franken.calculationParameters.creationDate = destDefaultCR.calculationParameters.creationDate
    franken.calculationParameters.name = destDefaultCR.calculationParameters.name
    #need to rewrite workspace names
    franken.workspaces = {
        "diffCalOutput" :[f"dsp_column_{str(destRun).zfill(6)}_v{str(destVersion).zfill(4)}"],
        "diffCalDiagnostic" :[f"diagnostic_column_{str(destRun).zfill(6)}_v{str(destVersion).zfill(4)}"],
        "diffCalTable" :[f"diffract_consts_{str(destRun).zfill(6)}_v{str(destVersion).zfill(4)}"],
        "diffCalMask":[f"diffract_consts_mask_{str(destRun).zfill(6)}_v{str(destVersion).zfill(4)}"]
    }

    if printRecord:
        print("FRANKEN RECORD:")
        print(franken.runNumber)
        print(franken.useLiteMode)
        print("version: ",franken.version)
        print("calculationParameters:")
        for par in franken.calculationParameters:
            print('\n')
            print(par)
        print("calculationParameters:")

        print("\ncrystalInfo\n")
        print(franken.crystalInfo)

        #pixelGroups
        print("\npixelGroups\n")
        print(franken.pixelGroups)

        #workspaces
        print("\nworkspaces")
        print(franken.workspaces)

    return franken
