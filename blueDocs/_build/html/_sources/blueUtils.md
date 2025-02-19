# blueUtils 

blueUtils is the main scripting layer for SNAPBlue and contains the function `reduce` which uses SNAPRed to reduce neutron diffraction data measured on SNAP.

Once imported, its various functions are available as methods, each method will typically have a set of arguments. Wherever possible, these arguments are given sensible defaults so, often times, they can be ignored. However, whenever more complicated, non-standard requirements exist, these are supported by customising the parameters. 

The available methods are: 

* `reduce`: reduces data using SNAPRed
* `exportData`: exports reduced data to various format outputs for subsequent refinement/analysis
* `propagateDifcal`: a utility to copy a diffraction calibration from one state to another compatible state (i.e. one with the same detector positions)
* `indexState`: outputs a list of defined states and their calibration status

