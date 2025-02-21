Search.setIndex({"docnames": ["SNAPStateMgr", "autoStateName", "availableStates", "blueUtils", "checkCalibrationStatus", "checkStateExists", "confirmIPTS", "createState", "exportData", "indexStates", "intro", "printCalibrationHome", "propagateDifcal", "pullStateDict", "reduce", "setup", "stateDef"], "filenames": ["SNAPStateMgr.md", "autoStateName.md", "availableStates.md", "blueUtils.md", "checkCalibrationStatus.md", "checkStateExists.md", "confirmIPTS.md", "createState.md", "exportData.md", "indexStates.md", "intro.md", "printCalibrationHome.md", "propagateDifcal.md", "pullStateDict.md", "reduce.md", "setup.md", "stateDef.md"], "titles": ["SNAPStateMgr", "<code class=\"docutils literal notranslate\"><span class=\"pre\">autoStateName</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">availableStates</span></code>", "blueUtils", "<code class=\"docutils literal notranslate\"><span class=\"pre\">checkCalibrationStatus</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">checkStateExists</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">confirmIPTS</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">createState</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">exportData</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">indexStates</span></code>", "Welcome to the docs for SNAPBlue", "<code class=\"docutils literal notranslate\"><span class=\"pre\">printCalibrationHome</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">propagateDifcal</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">pullStateDict</span></code>", "<code class=\"docutils literal notranslate\"><span class=\"pre\">reduce</span></code>", "Set up", "<code class=\"docutils literal notranslate\"><span class=\"pre\">stateDef</span></code>"], "terms": {"A": [0, 16], "core": [0, 15], "concept": [0, 14], "snapr": [0, 3, 4, 6, 8, 10, 11, 12, 14, 15], "i": [0, 1, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15], "creation": 0, "manag": [0, 10], "collect": 0, "differ": [0, 8, 14], "instrument": [0, 14], "configur": [0, 4], "known": 0, "state": [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 16], "associ": 0, "orchestr": [0, 10], "calibr": [0, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14], "reduct": [0, 8, 10, 14], "task": 0, "The": [0, 3, 4, 7, 8, 9, 14, 15, 16], "modul": [0, 10, 12, 14, 15], "snapblu": [0, 3, 9, 12, 14], "util": [0, 1, 2, 3, 9, 10, 12, 14], "exploit": 0, "thi": [0, 1, 2, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15], "function": [0, 3, 4, 8, 10, 12, 13, 14, 15], "do": [0, 15], "us": [0, 1, 3, 7, 8, 9, 10, 12, 13, 14, 15], "thing": [0, 15], "insid": [0, 11, 14, 15], "ani": [0, 12, 14], "python": [0, 14, 15], "script": [0, 3, 6, 10, 14, 15], "As": [0, 8, 14], "blueutil": [0, 9, 10, 12, 14, 15], "intend": [0, 8], "import": [0, 1, 3, 4, 5, 9, 12, 13, 14, 15, 16], "allow": [0, 6, 14], "its": [0, 3, 10, 14, 15], "typic": [0, 3, 9, 12, 15], "ssm": [0, 1, 4, 5, 12, 13, 16], "sy": [0, 9, 12, 14, 15], "path": [0, 9, 12, 14, 15], "append": [0, 9, 12, 14, 15], "sn": [0, 4, 8, 9, 12, 14, 15], "snap": [0, 3, 4, 8, 9, 10, 12, 14, 15], "share": [0, 4, 8, 9, 12, 14, 15], "code": [0, 9, 12, 14, 15], "blue": [0, 6, 9, 12, 14, 15], "an": [0, 5, 6, 8, 12, 14, 15, 16], "part": 0, "definit": [0, 13], "home": [0, 2, 5, 7, 11], "directori": [0, 5, 8], "defin": [0, 3, 8, 14, 16], "file": [0, 8, 13, 14, 15], "call": [0, 8, 12, 15], "applic": [0, 14], "yml": [0, 14, 15], "live": 0, "repo": [0, 11, 15], "depend": [0, 12, 14, 15], "which": [0, 3, 4, 9, 12, 14], "version": [0, 4], "being": 0, "could": 0, "point": [0, 6, 8, 14], "locat": [0, 12, 14, 15], "It": [0, 4, 7, 8, 10, 11, 12, 14], "": [0, 6, 8, 10, 13, 14], "consid": [0, 12], "printcalibrationhom": [0, 10], "can": [0, 3, 7, 8, 12, 14, 15], "check": [0, 2, 4], "current": [0, 8, 9, 10, 11, 14], "small": 1, "gener": [1, 7], "string": [1, 4, 6, 7, 8, 13], "represent": 1, "give": [1, 9], "concis": 1, "descript": [1, 8], "paramet": [1, 3, 7, 8, 9, 12, 13, 14, 16], "requir": [1, 3, 4, 5, 7, 13, 15], "dictionari": [1, 4, 16], "either": [1, 14], "pullstatedict": [1, 10], "statedef": [1, 10], "exampl": [1, 4, 5, 6, 12, 13, 14, 16], "snapstatemgr": [1, 4, 5, 10, 12, 13, 16], "id": 1, "dict": 1, "64413": [1, 9, 14], "desc": [1, 9], "print": [1, 4, 5, 11, 13, 16], "return": [1, 4, 5, 13, 16], "65": [1, 9, 16], "5": [1, 9, 16], "105": [1, 9, 16], "0": [1, 4, 9, 13, 14, 16], "2": [1, 9, 13, 14, 15, 16], "1": [1, 4, 6, 9, 13, 14, 15, 16], "60": [1, 9, 13, 16], "clearli": 1, "two": [1, 4, 10, 15, 16], "detector": [1, 3, 12, 14], "angl": 1, "wavelength": 1, "frequenc": [1, 13, 16], "guid": 1, "statu": [1, 3, 4, 6, 9], "specifi": [2, 4, 7, 8, 11, 12, 13, 14], "retur": 2, "list": [2, 3, 4, 6, 8, 16], "stateid": [2, 4, 5, 9, 13, 16], "all": [2, 8, 9, 14, 15], "exist": [2, 3, 4, 5, 8, 9, 12, 14], "folder": [2, 5, 7, 8, 13], "main": [3, 10, 15], "layer": [3, 15], "contain": [3, 14, 16], "reduc": [3, 6, 8, 10], "neutron": 3, "diffract": [3, 4, 12, 14], "data": [3, 6, 8, 10, 12, 13, 14], "measur": 3, "onc": [3, 8, 12, 15], "variou": [3, 14, 15], "ar": [3, 6, 8, 10, 12, 14, 15], "avail": [3, 8, 9, 12, 14, 15], "method": [3, 14, 16], "each": [3, 4, 8, 10, 12, 14], "have": [3, 8, 9, 12, 14, 15], "set": [3, 8, 10, 12, 14], "argument": [3, 4, 5, 6, 7, 14, 16], "wherev": 3, "possibl": [3, 8, 12, 14], "given": [3, 8], "sensibl": 3, "default": [3, 4, 6, 8, 9, 12, 14, 15], "so": 3, "often": 3, "time": 3, "thei": [3, 8, 9], "ignor": 3, "howev": [3, 8, 15], "whenev": 3, "more": 3, "complic": 3, "non": 3, "standard": [3, 14], "support": [3, 8], "customis": 3, "exportdata": [3, 10], "export": 3, "format": [3, 8], "output": [3, 8, 9, 14, 16], "subsequ": [3, 8, 12], "refin": [3, 8], "analysi": [3, 8], "propagatedifc": [3, 10], "copi": [3, 12, 14, 15], "from": [3, 6, 8, 12, 13, 14], "one": [3, 4, 12], "anoth": [3, 12], "compat": [3, 12], "e": [3, 6, 8, 14, 16], "same": [3, 8], "posit": [3, 12], "indexst": [3, 10], "three": [4, 8, 14], "islit": 4, "whether": [4, 5, 14], "lite": [4, 8, 12], "nativ": [4, 12], "caltyp": 4, "difcal": [4, 9, 12], "normcal": 4, "normalis": [4, 14], "full": [4, 14], "inform": [4, 10, 14], "regard": [4, 14], "request": [4, 8], "true": [4, 5, 8, 9, 12, 14], "caldict": 4, "3c7b8c841d10a16b": [4, 5, 9, 13], "kei": [4, 13, 16], "calibindex": 4, "els": 4, "ncalibr": 4, "index": [4, 14], "entri": [4, 16], "n": [4, 14], "calibentri": 4, "key2": 4, "calibrationtyp": 4, "iscalibr": 4, "numbercalibr": 4, "latestcalibr": 4, "2025": 4, "02": [4, 14], "17": 4, "14": 4, "31": 4, "11": 4, "calibrun": 4, "64437": [4, 9], "indexpath": 4, "calibration_test": 4, "powder": 4, "calibrationindex": 4, "json": 4, "runnumb": [4, 7], "uselitemod": 4, "appliesto": 4, "comment": [4, 6], "when": [4, 8, 9, 12, 14], "load": [4, 8, 14], "stateconfig": 4, "none": 4, "other": [4, 10, 15], "found": 4, "author": 4, "intern": 4, "timestamp": [4, 8, 14], "1739820536": 4, "8264458": 4, "test": [4, 8, 14], "c": 4, "ridlei": 4, "1739820671": 4, "918172": 4, "mostrecentcalib": 4, "note": [4, 8, 14, 15], "fals": [5, 8, 12, 14], "reflect": 5, "f": [5, 15, 16], "command": [6, 15], "updat": [6, 12, 15], "expermi": 6, "track": [6, 8], "section": 6, "ipt": [6, 8], "websit": 6, "record": 6, "user": 6, "access": [6, 15], "usag": [6, 9, 12], "12345": 6, "where": [6, 14], "number": [6, 8, 9, 12, 13, 14, 16], "There": [6, 10, 15], "3": [6, 8, 9, 14], "option": [6, 7, 8, 9, 14], "subnum": 6, "integ": 6, "just": [6, 8], "after": 6, "decim": 6, "g": [6, 8, 14, 16], "redtyp": 6, "ci": 6, "auto": 6, "free": 6, "form": [6, 8], "utilti": 7, "instanti": [7, 9], "new": [7, 12, 14], "creat": [7, 8, 12, 14, 15], "popul": 7, "correspond": [7, 8, 12, 13, 14], "ha": [7, 12, 14, 15], "singl": 7, "look": [7, 9, 12, 15], "determin": 7, "hrn": 7, "human": 7, "readabl": 7, "name": [7, 8, 14], "If": [7, 8, 12, 14, 15], "provid": [7, 8, 12, 14, 16], "autostatenam": [7, 10], "instead": [7, 8], "been": [8, 9, 12, 14, 15], "mantid": [8, 14], "workspac": [8, 14], "also": [8, 10, 12, 14], "automat": [8, 12, 14], "save": 8, "nx": 8, "along": 8, "detail": [8, 14], "reductionrecord": 8, "captur": 8, "In": [8, 15], "addit": [8, 14, 15], "necessari": [8, 12, 15], "appropri": 8, "enabl": 8, "By": [8, 12, 14], "pre": [8, 14, 15], "gsa": 8, "gsas2": 8, "pixel": [8, 14], "group": [8, 14], "store": 8, "separ": [8, 12], "bank": [8, 14], "xye": 8, "topa": 8, "fulprof": 8, "csv": 8, "parial": 8, "implement": [8, 14], "actual": [8, 12, 14], "tab": 8, "delin": 8, "nevertheless": 8, "simpl": [8, 9, 14, 15], "ascii": 8, "d": [8, 14], "space": [8, 14], "multipl": 8, "run": [8, 9, 10, 12, 13, 14, 16], "ad": 8, "suffix": 8, "end": 8, "onli": [8, 9, 14], "most": [8, 14], "recent": 8, "filenam": 8, "overrid": [8, 14], "see": [8, 14], "below": [8, 14], "treatement": 8, "attenu": 8, "correct": [8, 14], "final": [8, 14], "link": 8, "outout": 8, "templat": 8, "instprm": 8, "case": [8, 15], "work": 8, "go": 8, "alreadi": 8, "dummi": 8, "extens": 8, "At": 8, "present": 8, "autocr": 8, "should": [8, 15], "view": 8, "approxim": 8, "start": 8, "fulli": [8, 14], "ongo": 8, "figur": [8, 14], "out": [8, 11, 14], "how": 8, "propag": 8, "manual": 8, "sinc": [8, 12], "need": [8, 12, 14, 15], "within": 8, "some": [8, 14], "kind": 8, "autom": 8, "solut": 8, "desir": [8, 14], "isn": 8, "t": 8, "trivial": 8, "realis": 8, "though": 8, "doe": [8, 13, 14], "mode": [8, 12], "accord": [8, 14], "subdirectori": 8, "scheme": [8, 14], "dure": [8, 14], "34952": 8, "column": [8, 14], "Its": [8, 14], "valu": [8, 14, 16], "charact": 8, "describ": [8, 10, 14], "let": [8, 14], "malcolm": [8, 14, 15], "know": [8, 14], "ensur": [8, 15], "latest": [8, 9], "exclud": 8, "includ": [8, 10], "report": [9, 14], "those": 9, "like": 9, "No": 9, "nrmcal": 9, "b358bc9ca6f9f3d": 9, "30": 9, "uncalib": 9, "d1946b4615db2d4e": 9, "50": 9, "90": [9, 13], "6": [9, 12, 14], "4": 9, "b810d6da5d4af06": 9, "8": 9, "partial": 9, "64417": 9, "ffefaa93ccb23678": 9, "64459": 9, "685b9dc2fd699205": 9, "64446": 9, "0e04feff89cf95f3": [9, 16], "66": [9, 13], "64439": 9, "c073719d9101e8f2": 9, "64415": 9, "17fcca13ece67241": 9, "64422": 9, "74370ebaa23119db": 9, "calib": 9, "64444": 9, "64443": 9, "702ba297516db7bf": 9, "64433": [9, 12], "e1d38f0788481997": 9, "76": 9, "63438": 9, "63436": 9, "04bd2c53f6bf6754": [9, 16], "64412": 9, "27588df26158e93c": 9, "64431": [9, 12], "64430": 9, "64436": 9, "ce8a5e1e29a1de97": 9, "64420": 9, "64419": 9, "todo": [9, 12], "probabl": [9, 15], "add": 9, "interfac": 10, "sever": 10, "relat": 10, "follow": [10, 14, 15], "up": [10, 14], "confirmipt": 10, "checkstateexist": 10, "checkcalibrationstatu": 10, "availablest": 10, "createst": [10, 12], "rel": [11, 14], "self": 11, "explanatori": 11, "your": [11, 15], "fequent": 12, "sometim": [12, 13, 14], "valid": 12, "oper": 12, "donor": 12, "destin": 12, "ident": 12, "identifi": 12, "across": 12, "while": [12, 14], "indic": [12, 14], "you": [12, 14, 15], "order": [12, 15], "done": [12, 14, 15], "snapstatemanag": 12, "doc": 12, "too": 12, "would": [12, 14], "first": [12, 14, 15], "make": [12, 15], "For": [12, 14, 15], "4\u00e5": 12, "made": 12, "must": [12, 14], "conduct": [12, 14], "reli": 12, "transfer": 12, "good": 12, "practic": 12, "examin": 12, "expect": [12, 14], "outcom": 12, "without": 12, "consequ": 12, "behaviour": 12, "equal": 12, "sure": [12, 15], "everyth": 12, "abl": 13, "pull": 13, "directli": 13, "rather": 13, "than": 13, "input": 13, "statedict": [13, 16], "vdet_arc1": [13, 16], "vdet_arc2": [13, 16], "wavelengthuserreq": [13, 16], "po": [13, 16], "mandatori": 14, "On": 14, "happi": 14, "execut": 14, "complet": 14, "thu": 14, "minim": 14, "61991": 14, "abov": [14, 15], "result": 14, "appear": 14, "mantidworbench": 14, "tree": 14, "spectra": 14, "subgroup": 14, "begin": 14, "word": 14, "unit": 14, "dsp": 14, "year": 14, "month": 14, "dai": 14, "hour": 14, "minut": 14, "second": 14, "reduced_dsp_all_064413_2025": 14, "18t170940": 14, "reduced_dsp_bank_064413_2025": 14, "reduced_dsp_column_064413_2025": 14, "normal": [14, 15], "bit": 14, "visual": 14, "jar": 14, "beta": 14, "period": 14, "comparison": 14, "success": 14, "easi": 14, "remov": 14, "them": 14, "me": 14, "featur": 14, "interest": 14, "particular": 14, "filter": 14, "workpac": 14, "neat": 14, "wai": 14, "clean": 14, "pass": 14, "parenthes": 14, "syntax": 14, "here": 14, "flag": 14, "diagnost": 14, "proce": 14, "specif": [14, 15], "h5": 14, "diffractomet": 14, "constant": 14, "relev": 14, "find": 14, "built": [14, 15], "workflow": 14, "similarli": 14, "assess": 14, "vanadium": 14, "background": 14, "extract": 14, "pattern": 14, "artifici": 14, "algorithm": 14, "clippeak": 14, "smoothingparamet": 14, "decreaseparamet": 14, "lss": 14, "config": 14, "defaultredcconfig": 14, "overriden": 14, "control": 14, "over": 14, "log": 14, "level": 14, "messag": 14, "window": 14, "retent": 14, "unfocuss": 14, "dataset": 14, "x": 14, "chang": 14, "appli": 14, "mask": 14, "caveat": 14, "maskworkspac": 14, "maskworkspace_n": 14, "type": 14, "specifii": 14, "delet": 14, "intermedi": 14, "inspect": 14, "retain": 14, "troubleshoot": 14, "tricki": 14, "what": 14, "mani": 14, "help": 14, "Be": 14, "awar": 14, "lot": 14, "memori": 14, "reop": 14, "defaultredconfig": 14, "edit": 14, "NOT": 14, "yet": 14, "protoyp": 14, "sampl": 14, "environ": 14, "pe": 14, "cell": 14, "dac": 14, "etc": 14, "prerequisit": 15, "activ": 15, "local": 15, "now": 15, "nightli": 15, "treat": 15, "hopefulli": 15, "soon": 15, "formal": 15, "deploy": 15, "negat": 15, "worri": 15, "about": 15, "These": 15, "instruct": 15, "presum": 15, "instal": 15, "easiest": 15, "sit": 15, "down": 15, "With": 15, "termin": 15, "navig": 15, "cd": 15, "To": 15, "env": 15, "occasion": 15, "softwar": 15, "mai": 15, "prune": 15, "presuppos": 15, "itself": 15, "we": 15, "want": 15, "our": 15, "happen": 15, "src": 15, "m": 15, "mantidworkbench": 15, "editor": 15, "accept": 16, "stateinfo": 16, "64414": 16}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"snapstatemgr": 0, "autostatenam": 1, "availablest": 2, "blueutil": 3, "checkcalibrationstatu": 4, "checkstateexist": 5, "confirmipt": 6, "createst": 7, "exportdata": 8, "overview": [8, 9, 12, 14], "export": 8, "locat": 8, "exportformat": 8, "latestonli": 8, "gsasinstprm": 8, "indexst": 9, "islit": [9, 12], "welcom": 10, "doc": 10, "snapblu": [10, 15], "what": 10, "i": 10, "printcalibrationhom": 11, "propagatedifc": 12, "propag": 12, "pullstatedict": 13, "reduc": 14, "continuenodifc": 14, "continuenonrmc": 14, "reducedata": 14, "verbos": 14, "keepunfocuss": 14, "pixelmaskindex": 14, "emptytrash": 14, "cismod": 14, "ymloverrid": 14, "sampleenv": 14, "set": 15, "up": 15, "conda": 15, "environ": 15, "open": 15, "right": 15, "version": 15, "mantid": 15, "workbench": 15, "run": 15, "statedef": 16}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinxcontrib.bibtex": 9, "sphinx": 57}, "alltitles": {"SNAPStateMgr": [[0, "snapstatemgr"]], "autoStateName": [[1, "autostatename"]], "availableStates": [[2, "availablestates"]], "blueUtils": [[3, "blueutils"]], "checkCalibrationStatus": [[4, "checkcalibrationstatus"]], "checkStateExists": [[5, "checkstateexists"]], "confirmIPTS": [[6, "confirmipts"]], "createState": [[7, "createstate"]], "exportData": [[8, "exportdata"]], "Overview": [[8, "overview"], [9, "overview"], [12, "overview"]], "Export locations": [[8, "export-locations"]], "exportFormats": [[8, "exportformats"]], "latestOnly": [[8, "latestonly"]], "gsasInstPrm": [[8, "gsasinstprm"]], "indexStates": [[9, "indexstates"]], "isLite": [[9, "islite"], [12, "islite"]], "Welcome to the docs for SNAPBlue": [[10, "welcome-to-the-docs-for-snapblue"]], "What is SNAPBlue?": [[10, "what-is-snapblue"]], "printCalibrationHome": [[11, "printcalibrationhome"]], "propagateDifcal": [[12, "propagatedifcal"]], "propagate": [[12, "propagate"]], "pullStateDict": [[13, "pullstatedict"]], "reduce": [[14, "reduce"]], "overview": [[14, "overview"]], "continueNoDifcal": [[14, "continuenodifcal"]], "continueNoNrmcal": [[14, "continuenonrmcal"]], "reduceData": [[14, "reducedata"]], "verbose": [[14, "verbose"]], "keepUnfocussed": [[14, "keepunfocussed"]], "pixelMaskIndex": [[14, "pixelmaskindex"]], "emptyTrash": [[14, "emptytrash"]], "cisMode": [[14, "cismode"]], "YMLOverride": [[14, "ymloverride"]], "sampleEnv": [[14, "sampleenv"]], "Set up": [[15, "set-up"]], "Set up conda environment": [[15, "set-up-conda-environment"]], "Open (the right version of) mantid workbench": [[15, "open-the-right-version-of-mantid-workbench"]], "running SNAPBlue": [[15, "running-snapblue"]], "stateDef": [[16, "statedef"]]}, "indexentries": {}})