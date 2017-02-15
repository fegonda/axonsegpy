######################################
# Class Axone This is the main object#
# for  our program.  All the Axone   #
# are listed with AxoneList          #
######################################
class Axone:
    def __init__(self,posxCentroide,posyCentroide,diametre):
        """
        :param posxCentroide: position x, of the centroide for this axone. In pixel
        :param posyCentroide: position y, of the centroide for this axone. In pixel
        :param diametre: daimetre of the axone
        :return: no return
        """
        self.__posxCentroide=posxCentroide#en pixel
        self.__posyCentroide=posyCentroide
        self.__diametre=diametre

    def getDiametre(self):
        """
        :return: diametre for this axone
        """
        return self.__diametre

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
        return hash((self.__diametre,self.__posxCentroide,self.__posyCentroide))

    def __eq__(self, other):
        """
         :return: boolean. allow to compare axone beetween them.
         """
        return self.__diametre,self.__posxCentroide,self.__posyCentroide==other.__diametre,other.__posxCentroide,other.__posyCentroide
