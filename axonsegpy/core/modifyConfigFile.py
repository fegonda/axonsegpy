import json

def modifyPreprocessing(configFile):
    """
    Should be use by the GUI to modifiy the configFile for the preprocessing
    :param configFile:
    :return:
    """
    with open(configFile,"r") as jsonFile:
      data = json.load(jsonFile)
    tmp=data["preprocessing"]
def addAlgorithme(name,params):
    """
    :param name: name of the algorthme
    :param params: a arrayof nameparam/value
    :return:
    """
    temp= "{\"name\":\""+name+"\",\t\"params\":{"
    #now add the param
    for i,data in params:
        if i!=len(params)-1:
            temp += "\""+data[0]+":\""+data[1]+"\",\t"#Need to know if last param
        else:
            temp += "\"" + data[0] + ":\"" + data[1] + "\"\t"
    temp += "}\t}\t"
    return temp
