######################################
# Class AxoneList This is a set of   #
# axone. operator "+" and "-" are    #
#               overloaded.          #
######################################
class AxoneList:
    #Constructor. You can initialize your AxoneListe our leave it empty
    def __init__(self,listAxone=None):
        """
        :param listAxone: axone liste to join. facultative, will be initialized empty if none
        """
        if listAxone is None:
            self.__listAxone=set()
            self.__nbrAxone=0
        else:
            self.__listAxone=set(listAxone)
            self.__nbrAxone=len(listAxone)

    #insert an axone and increment nbrAxone
    def insert(self,axone):
        """
        :param axone: the axone to insert
        :return: none
        """
        self.__listAxone.add(axone)
        self.__nbrAxone+=1
    #Overload + for adding two axonelist. duplicate won't be copied.
    def __add__(self,other):
        """
        :param other: the axonlist to add
        :return: a new axone liste, union of self and other
        """
        liste=self.__listAxone.union(other.getAxoneList())
        return AxoneList(liste)
    #Overload -, copied all element in self but not in other
    def __sub__(self, other):
        """
        :param other: the axone list to compare
        :return: a new axone list, result of the difference beetween self and other
        """
        liste=self.__listAxone.difference(other.getAxoneList)
        return AxoneList(liste)
    #Overload == allow axoneList comparaison
    def __eq__(self, other):
        """
        :param other: the axonlist to compare self to
        :return: boolean, is both list equals.
        """
        return self.__listAxone, self.__nbrAxone==other.__listAxone,other.__nbrAxone
    #Getter
    def getAxoneList(self):
        """
        :return: AxonList for self
        """
        return self.__listAxone
    #Getter
    def getNbrAxone(self):
        """
        :return:nbrAxone for self
        """
        return self.__nbrAxone
    #getAllAxone under  the specified diametre into a new AxoneList
    def getAxoneUnderDiametre(self,diametre):
        """
        :param diametre: the diametre maximum
        :return: a new axoneList with all axone below diametre
        """
        liste=AxoneList()
        for axone in self.__listAxone:
            if axone.getDiametre()<diametre:
                liste.insert(axone)
        return liste
    def getAxoneHigherThanDiametre(self,diametre):
        """
        :param diametre: the diametre minimum
        :return: a new axoneList with all axone below diametre
        """
        liste=AxoneList()
        for axone in self.__listAxone:
            if axone.getDiametre()>diametre:
                liste.insert(axone)
        return liste
    def getDiametreMean(self):
        """
        :return: the mean od the diametre of all axone
        """
        temp=0
        for axone in self.__listAxone:
            temp+=axone.getDiametre()
        return temp/self.getNbrAxone()