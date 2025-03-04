# some helpful functions for use with SNAPRed script version
import yaml
from mantid.simpleapi import *
from mantid.kernel import PhysicalConstants
import numpy as np
import json
import importlib
import SNAPStateMgr as ssm
importlib.reload(ssm)
import SNAPExportTools as exportTools
importlib.reload(exportTools)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# SNAPRed imports
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

class globalParams:

# This class holds a set of parameters that will be applied during reduction
# these are stored in a YAML file and can be changed by specifying alternate
# YAML files

    def __init__(self,defaultYML):

        with open(defaultYML,'r') as file:
            ymlIn = yaml.safe_load(file)

        self.useLiteMode = ymlIn["useLiteMode"]
        self.pixelMasks = ymlIn["pixelMasks"]
        self.keepUnfocussed = ymlIn["keepUnfocussed"]
        self.convertUnitsTo = ymlIn["defaultUnfocussedWorkspaceUnits"]
        self.AN_smoothingParameter = ymlIn["artificialNorm"]["smoothingParameter"]
        self.AN_decreaseParameter = ymlIn["artificialNorm"]["decreaseParameter"]
        self.AN_lss = ymlIn["artificialNorm"]["lss"]

        return
    
def makeDefaultYML(outputYML):

    #dictionary of params
    params = {"useLiteMode": True,
              "pixelMasks": [],
              "keepUnfocussed": False,
              "defaultUnfocussedWorkspaceUnits": "dSpacing"
              }
    
    with open(outputYML, 'w') as file:
        yaml.dump(params, file)

    print('wrote: ',outputYML)

def makeSEE(outputName,SEEDirectory):

    #TODO: make function to initialise SEE (=  Sample Environment Equipment) definition with mandatory inputs
    ymlOut = SEEDirectory + outputName
    return ymlOut 

def loadSEE(seeDefinition,SEEFolder):

    #loads Parameters from SEE definition as a dictionary

    #TODO: add this to application.yml
    inputYML = f"{SEEFolder}/{seeDefinition}.yml"

    #TODO: manage errors when file doesn't exist etc.
    with open(inputYML,'r') as file:
            seeDict = yaml.safe_load(file)

    return seeDict

def indexStates(isLite=True):

    allAvailableStates = ssm.availableStates()

        #12345678901234567890123456789012345678901234567890

    
    outputStrings = []
    statuses = []
    for stateID in allAvailableStates:

        stateDict = ssm.pullStateDict(stateID)
        difcal = ssm.checkCalibrationStatus(stateID,isLite,calType='difcal')
        nrmcal = ssm.checkCalibrationStatus(stateID,isLite,calType='normcal')

        # parse possible scenarios
        if difcal["isCalibrated"] and nrmcal["isCalibrated"]:
            calStatus = '*CALIB*'
        if not difcal["isCalibrated"] or not nrmcal["isCalibrated"]:
            calStatus = "PARTIAL"
        if not difcal["isCalibrated"] and not nrmcal["isCalibrated"]:
            calStatus = "UNCALIB"

        desc = ssm.autoStateName(stateDict)
        nDifcal = difcal['numberCalibrations']

        if difcal['latestCalibration'] != "never":

            latestDifcalRun = difcal['mostRecentCalib']['runNumber']
        else:
            latestDifcalRun = ""

        nNrmcal = nrmcal['numberCalibrations']

        if nrmcal['latestCalibration'] != "never":
            latestNrmcalRun = nrmcal['mostRecentCalib']['runNumber']
        else:
            latestNrmcalRun = ""

        outputString = (f"{stateID}|{desc}|"
                        f" {calStatus} |"
                        f"     {nDifcal}     | {latestDifcalRun.rjust(6)} |"
                        f"     {nNrmcal}     | {latestNrmcalRun.rjust(6)} |"
                            )
        statuses.append(calStatus) 
        outputStrings.append(outputString)

    #output in order of calibration status...
    print("\n StateID        | Desc.                   | Status  |No. difcals| latest |No. nrmcals| latest |")
    for i,string in enumerate(outputStrings):
        if statuses[i] == "UNCALIB":
            print(string) 

    for i,string in enumerate(outputStrings):
        if statuses[i] == "PARTIAL":
            print(string) 

    for i,string in enumerate(outputStrings):
        if statuses[i] == "*CALIB*":
            print(string) 



def exportData(exportFormats=['gsa','xye','csv'],latestOnly=True,gsaInstPrm=True):

    exportTools.reducedRuns(exportFormats,
                            latestOnly,
                            gsaInstPrm)
    
def confirmIPTS(ipts,comment="SNAPRed/Blue", subNum=1, redType="Scripts"):

    import subprocess

    #TODO: input validation!

    #validate redType
    allowedRedTypes = ["Scripts","CIS","Auto",""]
    if redType not in allowedRedTypes:
        print(f"ERROR: {redType} is not a supported option for redType parameters")
        return
    #check case
    if redType.lower() == "scripts":
        redType = "Scripts"
    if redType.lower() == "cis":
        redType = "CIS"
    if redType.lower() == "auto":
        redType = "Auto"

    
    execArg = [
        "/SNS/SNAP/shared/Malcolm/devel/confirm-data",
        "SNAP",
        f"{ipts}",
        f"{subNum}",
        f"{redType}",
        "-c",
        f"{comment}",
        "-s",
        "Yes"
    ]

    print(execArg)
    subprocess.run(execArg,
                   capture_output=True,
                   check=True,
                   shell=False) 

def propagateDifcal(refRunNumber,isLite=True,propagate=False,includeGuideStatus=True):

    #This will accept a reference Run number, determine a list of all existing 
    # states with equivalent detector positions propagate and their (diff) calibration status
    # if propagate==True, the latest calibration from the state corresponding to 
    # refRunNumber will be propagates to other compatible states as if it's a formal
    # calibration
 
    refStateID,refStateDict = ssm.stateDef(refRunNumber)
    refDetConfig = ssm.detectorConfig(refStateDict,includeGuideStatus)

    # check diffraction calibration status of reference run
    refCalStatus = ssm.checkCalibrationStatus(refStateID,isLite,"difcal")
    # if state is uncalibrated, stop. Nothing to propagate
    if not refCalStatus["isCalibrated"]:
        print("ERROR: Reference State is uncalibrated! Please calibrate or choose a different reference")
        return
    else:
         print(f"""
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
propagateDifcal: Utility to copy calibrations
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
Origin calibration info
    - Run:  {refRunNumber}
    - State: {refStateID}
    - Detector config: {refDetConfig}
    - calibrated: {refCalStatus['numberCalibrations']} times
    - latest version: {refCalStatus['mostRecentCalib']['version']}           
    """)

    nCompatibleStates = 0
    toPropagateCal = []
    toPropagateState = []
    toPropagateDetConfig = []
    for stateID in ssm.availableStates():
        if stateID != refStateID:
            stateDict = ssm.pullStateDict(stateID) ##
            detConfig = ssm.detectorConfig(stateDict,includeGuideStatus)
            if detConfig == refDetConfig:
                calStatus = ssm.checkCalibrationStatus(stateID,isLite,"difcal")
                toPropagateCal.append(calStatus)
                toPropagateState.append(stateID)
                toPropagateDetConfig.append(detConfig)
                     
                nCompatibleStates += 1

    print(f"\n{nCompatibleStates} state(s) found with matching detector configs\n")

    print("Existing compatible states are:")
    for state in toPropagateState:
        print(state)

    if propagate:
        print("\nThese will be propagated")
        for cal in toPropagateCal:
            ssm.copyDifcal(refCalStatus,cal,propagate)
    else:
        print("\nPropagatation of calibration was not requested")
        

def reduce(runNumber,
               sampleEnv='none',
               pixelMaskIndex='none',
               YMLOverride='none',
               continueNoDifcal = False,
               continueNoVan = False,
               verbose=False,
               reduceData=True,
               keepUnfocussed=False,
               lambdaCrop=True, #temporarily needed until SNAPRed can do this during reduction
               emptyTrash=True, #remove temporary mantid workspaces at the end of reduction
            #    export=['gsas','xye','ascii'], #file formats to export to. If empty, no export 
               cisMode=False,
               singlePixelGroup=None,
               qsp=False):

    from mantid import config

    if verbose:
        config.setLogLevel(5, quiet=True)
    else:
        config.setLogLevel(0, quiet=True)


    if cisMode:
        Config._config['cis_mode'] = True
    else:
        Config._config['cis_mode'] = False

    print("SNAPBlue: gathering reduction ingredients...\n")
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # load reduction params from default yml with option to override 
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #TODO: update default to final shared repo path

    if YMLOverride == 'none':
        defaultYML = "/SNS/SNAP/shared/code/SNAPBlue/defaultRedConfig.yml" #this will live in repo
    else:
        defaultYML = YMLOverride

    blueGlob = globalParams(defaultYML)

    #set global parameters
    useLiteMode=blueGlob.useLiteMode
    pixelMasks = blueGlob.pixelMasks
    # keepUnfocussed = blueGlob.keepUnfocussed
    convertUnitsTo = blueGlob.convertUnitsTo

    #process continue flags
    continueFlags = ContinueWarning.Type.UNSET #by default do not continue

    if continueNoVan:
        artificialNormalizationIngredients = ArtificialNormalizationIngredients(
        peakWindowClippingSize = Config["constants.ArtificialNormalization.peakWindowClippingSize"],
        smoothingParameter=blueGlob.AN_smoothingParameter,
        decreaseParameter=blueGlob.AN_decreaseParameter,
        lss=blueGlob.AN_lss
        )
        continueFlags = ContinueWarning.Type.MISSING_NORMALIZATION
        
    else:
        artificialNormalizationIngredients = None

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process input arguments
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    runNumber = str(runNumber)
    SEEFolder = f'{Config["instrument.calibration.home"]}/sampleEnvironmentDefinitions'

    if sampleEnv != 'none':
        seeDict = loadSEE(sampleEnv,SEEFolder)

        if seeDict["masks"]["maskExists"] and (seeDict["masks"]["maskType"]=="static"):
            # TODO: need to separately manage lite versus non lite masks
            # TODO: mantid can't load lite masks ... need to use SNAPRed
            pass

    if pixelMaskIndex != 'none':
        #check that provided value is a list convert if it isn't
        if type(pixelMaskIndex) is not list:
            pixelMaskIndex = [pixelMaskIndex]

        #check that all requested masks actually exist
        for maskIndex in pixelMaskIndex:
            if maskIndex == 0: #account for weird mantid indexing by getting rid of zero 
                maskName = (wng.reductionUserPixelMask().numberTag(1)).build()
            else:
                maskName = (wng.reductionUserPixelMask().numberTag(maskIndex)).build()

            if maskName not in mtd.getObjectNames():
                print(f"ERROR: you requested mask workspace {maskName} but this doesn\'t exist")
                assert False
            pixelMasks.append(maskName)
    
    reductionService = ReductionService()
    timestamp = reductionService.getUniqueTimestamp()

    reductionRequest = ReductionRequest(
        runNumber=runNumber,
        useLiteMode=useLiteMode,
        timestamp=timestamp,
        continueFlags=continueFlags,
        pixelMasks=pixelMasks,
        keepUnfocused=keepUnfocussed,
        convertUnitsTo=convertUnitsTo,
        artificialNormalizationIngredients=artificialNormalizationIngredients
    )

    reductionService.validateReduction(reductionRequest)

    # 1. load default grouping workspaces from the state folder  TODO: how to init state?
    groupings = reductionService.fetchReductionGroupings(reductionRequest)

    # allow selection of singlePixelGroup

    if singlePixelGroup is None:
        reductionRequest.focusGroups = groupings["focusGroups"]
    else:
        reductionRequest.focusGroups = []
        for focGroup in groupings["focusGroups"]:
            if singlePixelGroup.lower()==focGroup.name.lower():
                print(f"Setting single focus group: {focGroup.name}")
                reductionRequest.focusGroups.append(focGroup)


    print("request",reductionRequest.focusGroups)

    # 2. Load Calibration (error out if it doesnt exist, comment out if continue anyway)
    # 3. Load Normalization (error out if it doesnt exist, comment out if continue anyway)
    # 3. Load the run data (lite or native)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # "fetchReductionGroceries" Loads necessary data (e.g. sample neutron data,
    # raw vanadium data, pixel group definitions, DIFCs
    # and pixel masks )
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    groceries = reductionService.fetchReductionGroceries(reductionRequest)

    groceries["groupingWorkspaces"] = groupings["groupingWorkspaces"]

    print(groceries["inputWorkspace"])

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #  Load the metadata i.e. ingredients
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # 1. load reduction ingredients
    ingredients = reductionService.prepReductionIngredients(reductionRequest, groceries.get("combinedPixelMask"))
    ingredients.artificialNormalizationIngredients = artificialNormalizationIngredients

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Determine calibration status and process this
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    dataFactoryService = DataFactoryService()
    calibrationPath = dataFactoryService.getCalibrationDataPath(
                runNumber, useLiteMode, VersionState.LATEST
            )
    # print(calibrationPath)
    calibrationRecord = dataFactoryService.getCalibrationRecord(
                runNumber, useLiteMode, VersionState.LATEST
            )
    
    if calibrationRecord.version == 0 and not continueNoDifcal:
        print("""         
                 
          - WARNING: NO DIFFRACTION CALIBRATION FOUND. TO PROCEED EITHER:
              1. RUN A DIFFRACTION CALIBRATION OR 
              2. SET "continueNoDifcal = True" TO PROCEED WITH DEFAULT GEOMETRY

            """)
        assert False

    # print(calibrationRecord.version)
    normalizationPath = dataFactoryService.getNormalizationDataPath(
                runNumber, useLiteMode, VersionState.LATEST
            )
    # print(normalizationPath)
    normalizationRecord = dataFactoryService.getNormalizationRecord(
                runNumber, useLiteMode, VersionState.LATEST
            )
    
    if type(normalizationRecord) == None:
        print("""         
                 
          - WARNING: NO VANADIUM FOUND. TO PROCEED EITHER: 
              1. RUN A VANADIUM CALIBRATION OR 
              2. SET "continueNoVan = True" TO USE ARTIFICIAL NORMALISATION

            """)
        
    
    # print(normalizationRecord.version)
    stateID = dataFactoryService.constructStateId(runNumber)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Pretty print useful information regarding reduction status
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 

    allPixelGroups = []
    for ingredient in ingredients:   
        if ingredient[0] == "pixelGroups":
            for item in ingredient[1]:
                allPixelGroups.append(item.focusGroup.name)

    print(f"""
            SNAPRed:

                - Run Number: {ingredients.runNumber}

                - state: 
                    - ID: {stateID[0]},
                    - definition: {stateID[1]}

                - Pixel Groups to process: {allPixelGroups}

            """)
    
    
    
    if calibrationRecord.version==0 and continueNoDifcal:
        print("""

          - WARNING: DIAGNOSTIC MODE! DEFAULT GEOMETRY USED.

              """)
    else:
        print(f"""
          Calibration Status:
            - Diffraction Calibration:
                - .h5 path: {calibrationPath}
                - .h5 version: {calibrationRecord.version}

    """)

    if continueNoVan:
        print("""         
                 
          - WARNING: DIAGNOSTIC MODE! VANADIUM CORRECTION NOT USED
            DATA WILL BE ARTIFICIALLY NORMALISED BY DIVISION BY BACKGROUND.

            """)
    else:
        print(f"""            
                - Normalisation Calibration:
                    - raw vanadium path: {normalizationPath}
                    - raw vanadium version: {normalizationRecord.version}

            """)


    #optional arguments provided...

    if sampleEnv != 'none':
        print(f"""          
            Sample environment was specified.

                - name: {seeDict["name"]}
                - id: {seeDict["id"]}
                - type: {seeDict["type"]}
                - mask: {seeDict["masks"]["maskFilenameList"]} NOT YET IMPLEMENTED
            
            """)

    if pixelMasks != 'none' or []:
        print(f"""
            Mask workspace(s) specified:
        """)
        for mask in pixelMasks:
            print(f"""
                {mask}
                  """)

    #obtain useful values from instrument state

        farmFresh = FarmFreshIngredients(
        runNumber=runNumber,
        useLiteMode=useLiteMode,
        focusGroups=[{"name":"All", "definition":""}],
        )
        instrumentState = SousChef().prepInstrumentState(farmFresh)

    if reduceData:

        if lambdaCrop:
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #  Crop data in wavelength space prior to reduction
            #  This was used while troubleshooting spectral edges
            #
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            ConvertUnits(InputWorkspace=groceries["inputWorkspace"],
                        OutputWorkspace=groceries["inputWorkspace"],
                        Target="Wavelength")
            
            CropWorkspace(InputWorkspace=groceries["inputWorkspace"],
                        OutputWorkspace=groceries["inputWorkspace"],
                        XMin = instrumentState.particleBounds.wavelength.minimum,
                        XMax = instrumentState.particleBounds.wavelength.maximum)
            
            ConvertUnits(InputWorkspace=groceries["inputWorkspace"],
                        OutputWorkspace=groceries["inputWorkspace"],
                        Target="TOF")


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Execute reduction here
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        data = ReductionRecipe().cook(ingredients, groceries)
        record = reductionService._createReductionRecord(reductionRequest, ingredients, data["outputs"])

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #  Save the data
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        saveReductionRequest = ReductionExportRequest(
            record=record
        )

        reductionService.saveReduction(saveReductionRequest)
        print(f"""
        Reduction COMPLETE

            - Run Number: {ingredients.runNumber}

            - state: 
                - ID: {stateID[0]},
                - definition: {stateID[1]}

            - Pixel Groups to process: {allPixelGroups}

        """)
    
    if calibrationRecord.version==0 and continueNoDifcal:
        print("""
          - WARNING: DIAGNOSTIC MODE! DEFAULT GEOMETRY USED TO CONVERT UNITS.
              """)
    else:
        print(f"""
          Calibration Status:
            - Diffraction Calibration:
                - .h5 path: {calibrationPath}
                - .h5 version: {calibrationRecord.version}

    """)

    if continueNoVan:
        print("""         
          - WARNING: DIAGNOSTIC MODE! VANADIUM CORRECTION NOT USED
            DATA WILL BE ARTIFICIALLY NORMALISED USING DIVISION BY BACKGROUND
            """)
    else:
        print(f"""            
            - Normalisation Calibration:
                - raw vanadium path: {normalizationPath}
                - raw vanadium version: {normalizationRecord.version}

            """)

    #optional arguments provided...

    if sampleEnv != 'none':
        print(f"""          
            Sample environment was specified.

                - name: {seeDict["name"]}
                - id: {seeDict["id"]}
                - type: {seeDict["type"]}
                - mask: {seeDict["masks"]["maskFilenameList"]} NOT YET IMPLEMENTED
            
            """)

    if pixelMasks != 'none' or []:
        print(f"""
            Mask workspace(s) specified:
        """)
        for mask in pixelMasks:
            print(f"""
                {mask}
                  """)


    if verbose:

        

        print("\nINSTRUMENT PARAMETERS")
        print(f"- Calib.home: {Config['instrument.calibration.home']}")
        # print("\nParams in SNAPInstPrm:")
        print("- L1: ",instrumentState.instrumentConfig.L1)
        print("- L2: ",instrumentState.instrumentConfig.L2)
        L = instrumentState.instrumentConfig.L1+instrumentState.instrumentConfig.L2
        print("- bandwidth: ",instrumentState.instrumentConfig.bandwidth)
        print("- lowWavelengthCrop: ",instrumentState.instrumentConfig.lowWavelengthCrop)

        # print("\nParams in application.yml")
        print("- low d-Spacing crop: ",Config["constants.CropFactors.lowdSpacingCrop"])
        print("- high d-Spacing crop: ",Config["constants.CropFactors.highdSpacingCrop"])

        # print("\nParams from state")
        wav = instrumentState.detectorState.wav
        print("- Central wavelength: ",wav)

        print("\n")
        bandwidth = instrumentState.instrumentConfig.bandwidth
        lowWavelengthCrop = instrumentState.instrumentConfig.lowWavelengthCrop
        lamMin = instrumentState.particleBounds.wavelength.minimum
        lamMax = instrumentState.particleBounds.wavelength.maximum
        tofMin = instrumentState.particleBounds.tof.minimum
        tofMax = instrumentState.particleBounds.tof.maximum
        
        print(f"- wavelength limits: {lamMin:.4f}, {lamMax:.4f}")
        # print(f"- TOF limits: {tofMin:.1f}, {tofMax:.1f}")

        # some tests to confirm that these numbers are being calculated as expected
        convFactor = Config["constants.m2cm"] * PhysicalConstants.h / PhysicalConstants.NeutronMass

#         print(f""" SOME TESTING...
# calculated lamMin is {wav - bandwidth/2 + lowWavelengthCrop}:.4f, {}
# """)

        assert lamMin == wav - bandwidth/2 + lowWavelengthCrop
        assert lamMax == wav + bandwidth/2
        # print(f"calculated tof limits: {lamMin*L/convFactor:.1f}, {lamMax*L/convFactor:.1f}")
        assert tofMin == lamMin*L/convFactor
        assert tofMax == lamMax*L/convFactor
        # calcTofM
        # calcTofMax

        pgs = ingredients.pixelGroups #ingredients.pixelGroups is a list of pgs
        print("\nPIXEL GROUP PARAMETERS")
#         print(f"""TOF limits {pgs[0].timeOfFlight.minimum:.1f} - {pgs[0].timeOfFlight.maximum:.1f}
# Requested Bins across halfWidth: {pgs[0].nBinsAcrossPeakWidth}""")

        for pgs in ingredients.pixelGroups:     #ingredients.pixelGroups is a list of pgs
            
            #pgs are pixel group classes, they are iterable with each item in the class are
            #tuples with the first value of the tuple being its name

            print(f"""
-----------------------------------------------
pixel grouping scheme: {pgs.focusGroup.name}
with {len(pgs.pixelGroupingParameters)} subGroup(s)
                  """)
            dMins = []
            dMaxs = []
            dBins = []
            L2s = []
            twoThetas = []

            for subGroup in pgs.pixelGroupingParameters:

                params = pgs.pixelGroupingParameters[subGroup]
                dMaxs.append(params.dResolution.maximum)
                dBins.append(params.dRelativeResolution/pgs.nBinsAcrossPeakWidth)
                dMins.append(params.dResolution.minimum)
                L2s.append(params.L2)
                twoThetas.append(params.twoTheta)

            twoThetasDeg = [180.0*x/np.pi for x in twoThetas]
            cropDMins = [d+Config["constants.CropFactors.lowdSpacingCrop"] for d in dMins]
            cropDMaxs = [d-Config["constants.CropFactors.highdSpacingCrop"] for d in dMaxs]
            #reduce precision for pretty printing



            dMaxs = [round(num,4) for num in dMaxs]
            dMins = [round(num,4) for num in dMins]
            dBins = [round(num,4) for num in dBins]
            cropDMins = [round(num,4) for num in cropDMins]
            cropDMaxs = [round(num,4) for num in cropDMaxs]    

            L2s = [round(num,4) for num in L2s]
            twoThetas = [round(num,4) for num in twoThetas]
            twoThetasDeg = [round(num,1) for num in twoThetasDeg]

            just = 20
            print("L2 (m)".ljust(just),L2s)
            print("twoTheta (rad)".ljust(just),twoThetas)
            print("twoTheta (deg)".ljust(just),twoThetasDeg)
            print("dMin (Å)".ljust(just),dMins)
            print("dMax (Å)".ljust(just),dMaxs)
            print("dMin (Å) - cropped".ljust(just),cropDMins)
            print("dMax (Å) - cropped".ljust(just),cropDMaxs)
            print("dBin".ljust(just),dBins)


    #clean up after myself

    dirty = ["tof_all_lite_copy",
             "tof_all_lite_raw",
             "tof_all_copy",
             "tof_all_raw",
             "SNAPLite_grouping",
             "SNAP_grouping",
             "diffract_consts_",
             "pixelmask_"] #workspaces with these expresions in their names
    if emptyTrash:
        wsList = mtd.getObjectNames()
        for ws in wsList:
            for dirt in dirty:
                if dirt in ws:
                    DeleteWorkspace(ws)

    if qsp:
        exportTools.convertToQ()

    # for par in instrumentState:
    #     print(par)
    config.setLogLevel(3, quiet=True)


    

