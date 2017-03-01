import numpy as np
######################################
# Class Axone This is the main object#
# for  our program.  All the Axone   #
# are listed with AxoneList          #
######################################
class Axone:
    def __init__(self,tags,posxCentroide=None,posyCentroide=None,diameter=None):
        """
        :param posxCentroide: position x, of the centroide for this axone. In pixel
        :param posyCentroide: position y, of the centroide for this axone. In pixel
        :param diametre: daimetre of the axone
        :return: no return
        """
        if posxCentroide==None:
            self.__posxCentroide=tags.centroid[0]#en pixel
            self.__posyCentroide=tags.centroid[1]
            self.__diameter=tags.equivalent_diameter
            self.__tags = tags
        else:#just for testing ?
            self.__posxCentroide=posxCentroide#en pixel
            self.__posyCentroide=posyCentroide
            self.__diameter=diameter
            self.__tags = tags

    def getDiameter(self):
        """
        :return: diametre for this axone
        """
        return self.__diameter

    def getPosx(self):
        """
        :return: position x for this axone
        """
        return self.__posxCentroide

    def getPosy(self):
        """
        :return: position Y for this axone
        """
        return self.__posyCentroide

    def __hash__(self):
        """
        :return: a (unique?) hash for the axone. Every hash is calculate with all 3 three parameters for each axone
        """
        return hash((self.__diameter,self.__posxCentroide,self.__posyCentroide))

    def __eq__(self, other):
        """
         :return: boolean. allow to compare axone beetween them.
         """
        return self.__diameter,self.__posxCentroide,self.__posyCentroide==other.__diametre,other.__posxCentroide,other.__posyCentroide

    def setMeylin(self, meylin):
        self.meylin = meylin
        temp = 0

        for a in range(72):
            delta = meylin[0][a]-meylin[1][a]
            temp += np.linalg.norm(delta)
        temp/=72
        self.meylinDiameter = temp


    def getMeylin(self):
        return self.meylin

    def getAvMeylinDiameter(self):
        return self.meylinDiameter

    def toArray(self):
        try:
            return [
                self.__posxCentroide,
                self.__posyCentroide,
                self.__diameter,
                self.meylin,
                self.__tags]
        except:
            return [
                self.__posxCentroide,
                self.__posyCentroide,
                self.__diameter,
                self.__tags]