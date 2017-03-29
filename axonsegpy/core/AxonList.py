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
    def insert(self,axon):
        """
        :param axon: the axone to insert
        :return: none
        """
        self.__listAxone.add(axon)
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
            if axone.getDiameter()<diametre:
                liste.insert(axone)
        return liste
    def getAxoneHigherThanDiametre(self,diametre):
        """
        :param diametre: the diametre minimum
        :return: a new axoneList with all axone below diametre
        """
        liste=AxoneList()
        for axone in self.__listAxone:
            if axone.getDiameter()>diametre:
                liste.insert(axone)
        return liste
    def getDiameterMean(self):
        """
        :return: the mean od the diametre of all axone
        """
        temp=0
        for axone in self.__listAxone:
            temp+=axone.getDiameter()
        return temp/self.getNbrAxone()

    def save(self, output):
        """
        :param output: file where to save
        """
        import _pickle as cPickle
        fileFormat = output.split('.')[-1]
        if fileFormat == "csv":
            # In CSV, we ignore the tags, for now
            # TODO Find an alternative !
            f = open(output, 'w')
            for axon in self.__listAxone:
                current = axon.toArray()
                for i in range(len(current)-1):
                    if "float" in str(type(current[i])):
                        current[i] = "%.10f" % current[i]
                listAxone = ','.join(current[:-1])
                f.write(listAxone + "\n")
            f.seek(0,0)
            f.close()
            
        else:
            if output[-4:] != ".bin":
                output += ".bin"
            cPickle.dump(self.__listAxone, open(output, "wb"))

    def load(self, inputFile):
        """
        :param output: file where to save
        :param format: format to save into
        """
        import _pickle as cPickle
        if inputFile.split('.')[-1] != "bin":
            #  TODO Import CSV ?
            print("Sorry, can only import binary numpy arrays for now !\n\tSo we can't import CSV for the moment.")
        else:
            self.__listAxone = cPickle.load(open(inputFile, "rb"))


