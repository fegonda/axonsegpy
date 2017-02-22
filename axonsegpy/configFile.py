import json

"""
	This class is an example of what we can do with the config file.
	In this instance, we just parse it and output the parameters.
	But in the next iteration, we will actually call the algo and pass them their values too.
"""
class configFile:
    def __init__(self,pathToFile):
    	jstruct = json.loads(open(pathToFile).read())
    	preprocessing = jstruct["preprocessing"]
    	axonSegmentation = jstruct["axonSegmentation"]
    	axonPostProcessing = jstruct["axonPostProcessing"]


    	print("Applying preprocessing algorithms :")
    	for e in preprocessing:
    		print("\tCalling algorithm : '" + e["name"] + "' with params:" )
    		for key, value in e["params"].items():
    			print("\t\t" + key + " : " + str(value))
    	print()
    	print("Applying axonSegmentation algorithms :")
    	for e in axonSegmentation:
    		print("\tCalling algorithm : '" + e["name"]+  "' with params:" )
    		for key, value in e["params"].items():
    			print("\t\t" + key + " : " + str(value))
    	print()
    	print("Applying axonPostProcessing algorithms :")
    	for e in axonPostProcessing:
    		print("\tCalling algorithm : '" + e["name"] + "' with params:" )
    		for key, value in e["params"].items():
    			print("\t\t" + key + " : " + str(value))



configFile("./configFile.json")
