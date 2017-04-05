import json
from core.RunConfig import runAlgo

"""
    This function will parse and execute the configFile
    # TODO Drop the 3 preprocessing / axonSegmentation / axonSPostSegmentation and use an array instead
"""
def parse(pathToFile):
    jstruct = json.loads(open(pathToFile).read())
    preprocessing = jstruct["preprocessing"]
    axonSegmentation = jstruct["axonSegmentation"]
    axonPostProcessing = jstruct["axonPostProcessing"]


    print("Applying preprocessing algorithms :")
    for e in preprocessing:
        print("\tCalling algorithm : '" + e["name"] + "' with params:" )
        for key, value in e["params"].items():
            print("\t\t" + key + " : " + str(value))
        runAlgo(e["name"], e["params"])
    print()
    print("Applying axonSegmentation algorithms :")
    for e in axonSegmentation:
        print("\tCalling algorithm : '" + e["name"]+  "' with params:" )
        for key, value in e["params"].items():
            print("\t\t" + key + " : " + str(value))
        runAlgo(e["name"], e["params"])
    print()
    print("Applying axonPostProcessing algorithms :")
    for e in axonPostProcessing:
        print("\tCalling algorithm : '" + e["name"] + "' with params:" )
        for key, value in e["params"].items():
            print("\t\t" + key + " : " + str(value))
        runAlgo(e["name"], e["params"])