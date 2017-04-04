import json

def addAlgorithme(configFile,placeToAdd,algorithme):
    """
    :param configFile: path to File
    :param placeToAdd: string for the step of the pipeline to modify
    :param algorithme: algo to add.
    :return: none
    """
    with open(configFile,"r") as jsonFile:
      data = json.load(jsonFile)
    tmp=data[placeToAdd]
    tmp.append(algorithme)
    data[placeToAdd]=tmp
    with open('./newConfigFile.json',"w") as outFile:
      print(data)
      json.dump(data,outFile)
def main():
    """
    Just to test our class
    :return:
    """
    print("letsgo")
    parametre= {'jack': 4098, 'sape': 4139}
    algorithme={'name': 'test', 'parametre': parametre}
    addAlgorithme("../test.json",algorithme)
if __name__ == "__main__":
    main()