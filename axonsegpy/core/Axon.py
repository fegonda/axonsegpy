import numpy as np
######################################
# Class Axon This is the main object#
# for  our program.  All the Axon   #
# are listed with AxonList          #
######################################
class Axon:
    def __init__(self,tags,posxCentroide=None,posyCentroide=None,diameter=None):
        """
        :param posxCentroide: position x, of the centroide for this axon. In pixel
        :param posyCentroide: position y, of the centroide for this axon. In pixel
        :param diametre: daimetre of the axon
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
        :return: diametre for this axon
        """
        return self.__diameter

    def getPosx(self):
        """
        :return: position x for this axon
        """
        return self.__posxCentroide

    def getPosy(self):
        """
        :return: position Y for this axon
        """
        return self.__posyCentroide

    def __hash__(self):
        """
        :return: a (unique?) hash for the axon. Every hash is calculate with all 3 three parameters for each axon
        """
        return hash((self.__diameter,self.__posxCentroide,self.__posyCentroide))

    def __eq__(self, other):
        """
         :return: boolean. allow to compare axon beetween them.
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
        return [
            self.__posxCentroide,
            self.__posyCentroide,
            self.__diameter,
            self.__tags]