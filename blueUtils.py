# some helpful functions for use with SNAPRed script version
import yaml

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

    #TODO: make function to initialise SEE definition with mandatory inputs
    ymlOut = SEEDirectory + outputName
    return ymlOut 

def loadSEE(seeDefinition):

    #TODO: add this to application.yml
    defaultSEEDir = '/SNS/SNAP/shared/Calibration_next/SimpleContainers/'
    inputYML = f"{defaultSEEDir}{seeDefinition}.yml"

    #TODO: manage errors when file doesn't exist etc.
    with open(inputYML,'r') as file:
            seeDict = yaml.safe_load(file)

    return seeDict

def reduceSNAP(runNumber,sampleEnv='none',mask='none'):

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
    from snapred.meta.Config import Config
    from rich import print as printRich

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # other imports (e.g. our own utilties)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # import sys
    # import importlib
    # sys.path.append("/SNS/SNAP/shared/Malcolm/code/SNAPBlue")
    # import blueUtils as blue
    # importlib.reload(blue)

    # import argparse

    ######################HERE ARE THE INPUT PARAMS###################################

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # load default reduction params from yml instead of script
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    defaultYML = "/SNS/SNAP/shared/Malcolm/code/SNAPBlue/defaultRedConfig.yml"
    blueGlob = globalParams("/SNS/SNAP/shared/Malcolm/code/SNAPBlue/defaultRedConfig.yml")
    useLiteMode=blueGlob.useLiteMode
    pixelMasks = blueGlob.pixelMasks
    keepUnfocused = blueGlob.keepUnfocussed
    convertUnitsTo = blueGlob.convertUnitsTo

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # define primary inputs and overrides using argparse
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # parser = argparse.ArgumentParser(description="Reduce SNAP data")

    # # run number. mandatory. TODO: allow this to be a list
    # parser.add_argument('runString', help='run number to reduce (for now single run at a time)')

    # # add optional arguments here
    # parser.add_argument(
    #         "-m",
    #         "--mask",  # Optional (but recommended) long version
    #         type=str,
    #         default="none",
    #         help = 'name of pixel mask workspace [TODO: allow for mask files?]'
    #         )

    # parser.add_argument(
    #         "-s",
    #         "--sampleEnv",  # Optional (but recommended) long version
    #         type=str,
    #         default="none",
    #         help = 'name of sample environment definition file (without extension)'
    #         )

    # args = parser.parse_args()
    runNumber = str(runNumber)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #  Now proceed to set up orchestration
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # when requested load additional config options
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #case 1: SEE definition provided. These will be YML stored in a specific 
    #location that contain as many pre-specified parameters as possible
    #for a given SEE set-up

    if sampleEnv != 'none':
        seeDict = oadSEE(ampleEnv)

    if mask != 'none':
        pixelMasks = mask


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # default exception handling TODO: move to yml
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # This is a bitwise flag you can update to say whether or not you are fine with
    # 1. missing calibration
    # 2. aritifical normalization
    # 3. missing normalization
    # 4. etc.
    # 
    #  e.g. continueFlags = ContinueWarning.Type.MISSING_CALIBRATION | ContinueWarning.Type.MISSING_NORMALIZATION
    continueFlags = ContinueWarning.Type.UNSET  
    # continueFlags = ContinueWarning.Type.MISSING_NORMALIZATION

    artificialNormalizationIngredients = None

    # NOTE: Uncomment if you want to perform aritificial normalization
    artificialNormalizationIngredients = ArtificialNormalizationIngredients(
        peakWindowClippingSize = Config["constants.ArtificialNormalization.peakWindowClippingSize"],
        smoothingParameter=0.5,
        decreaseParameter=True,
        lss=True
    )

    reductionService = ReductionService()
    timestamp = reductionService.getUniqueTimestamp()

    reductionRequest = ReductionRequest(
        runNumber=runNumber,
        useLiteMode=useLiteMode,
        timestamp=timestamp,
        continueFlags=continueFlags,
        pixelMasks=pixelMasks,
        keepUnfocused=keepUnfocused,
        convertUnitsTo=convertUnitsTo,
        artificialNormalizationIngredients=artificialNormalizationIngredients
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #  Load the supporting data (e.g. default pixel groups etc.)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    reductionService.validateReduction(reductionRequest)

    # 1. load grouping workspaces from the state folder  TODO: how to init state?
    groupings = reductionService.fetchReductionGroupings(reductionRequest)
    reductionRequest.focusGroups = groupings["focusGroups"]
    # 2. Load Calibration (error out if it doesnt exist, comment out if continue anyway)
    # 3. Load Normalization (error out if it doesnt exist, comment out if continue anyway)
    # 3. Load the run data (lite or native)  
    groceries = reductionService.fetchReductionGroceries(reductionRequest)
    groceries["groupingWorkspaces"] = groupings["groupingWorkspaces"]

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #  Load the metadata i.e. ingredients
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # 1. load reduction ingredients
    ingredients = reductionService.prepReductionIngredients(reductionRequest, groceries.get("combinedPixelMask"))
    ingredients.artificialNormalizationIngredients = artificialNormalizationIngredients

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Additional useful config information
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    dataFactoryService = DataFactoryService()
    calibrationPath = dataFactoryService.getCalibrationDataPath(
                runNumber, useLiteMode, VersionState.LATEST
            )
    # print(calibrationPath)
    calibrationRecord = dataFactoryService.getCalibrationRecord(
                runNumber, useLiteMode, VersionState.LATEST
            )
    # print(calibrationRecord.version)
    normalizationPath = dataFactoryService.getNormalizationDataPath(
                runNumber, useLiteMode, VersionState.LATEST
            )
    # print(normalizationPath)
    normalizationRecord = dataFactoryService.getNormalizationRecord(
                runNumber, useLiteMode, VersionState.LATEST
            )
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

            - Pixel Groups: {allPixelGroups}

            - Diffraction Calibration:
                - .h5 path: {calibrationPath}
                - .h5 version: {calibrationRecord.version}

            - Normalisation Calibration:
                - raw vanadium path: {normalizationPath}

        """)

    #optional arguments provided...

    if sampleEnv != 'none':
        print(f"""          
            Sample environment was specified.

                - name: {seeDict["name"]}
                - id: {seeDict["id"]}
                - type: {seeDict["type"]}
                - mask: {seeDict["pixelMasks"]}
            
            """)

    if mask != 'none':
        print(f"""
            Mask workspace was specified.

            Mask workspace name: {args.mask}
            
            """)

    continueInstruction = input("enter anything to continue")

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

