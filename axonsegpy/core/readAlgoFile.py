import json

def readAlgo(nameAlgo):
    """
    Retrieve the algo from the algo.json. Needed to update the GUI
    :param nameAlgo: the algo you want to retrieve
    :return: a dic, the algo.
    """
    with open("./algo.json","r") as jsonFile:
      data = json.load(jsonFile)
    return data[nameAlgo]
def getAlgoList():
    """
    :return: get a list of algo
    """
    with open("./algo.json","r") as jsonFile:
      data = json.load(jsonFile)
    return data.keys()