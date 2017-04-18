######################################
# Class AxonList This is a set of   #
# axon. operator "+" and "-" are    #
#               overloaded.          #
######################################
class AxonList:
    #Constructor. You can initialize your AxonListe our leave it empty
    def __init__(self,listAxon=None):
        """
        :param listAxon: axon liste to join. facultative, will be initialized empty if none
        """
        if listAxon is None:
            self.__listAxon=set()
            self.__nbrAxon=0
        else:
            self.__listAxon=set(listAxon)
            self.__nbrAxon=len(listAxon)

    #insert an axon and increment nbrAxon
    def insert(self,axon):
        """
        :param axon: the axon to insert
        :return: none
        """
        self.__listAxon.add(axon)
        self.__nbrAxon+=1
    #Overload + for adding two axonlist. duplicate won't be copied.
    def __add__(self,other):
        """
        :param other: the axonlist to add
        :return: a new axon liste, union of self and other
        """
        liste=self.__listAxon.union(other.getAxonList())
        return AxonList(liste)
    #Overload -, copied all element in self but not in other
    def __sub__(self, other):
        """
        :param other: the axon list to compare
        :return: a new axon list, result of the difference beetween self and other
        """
        liste=self.__listAxon.difference(other.getAxonList)
        return AxonList(liste)
    #Overload == allow axonList comparaison
    def __eq__(self, other):
        """
        :param other: the axonlist to compare self to
        :return: boolean, is both list equals.
        """
        return self.__listAxon, self.__nbrAxon==other.__listAxon,other.__nbrAxon
    #Getter
    def getAxonList(self):
        """
        :return: AxonList for self
        """
        return self.__listAxon
    #Getter
    def getNbrAxon(self):
        """
        :return:nbrAxon for self
        """
        return self.__nbrAxon
    #getAllAxon under  the specified diametre into a new AxonList
    def getAxonUnderDiametre(self,diametre):
        """
        :param diametre: the diametre maximum
        :return: a new axonList with all axon below diametre
        """
        liste=AxonList()
        for axon in self.__listAxon:
            if axon.getDiameter()<diametre:
                liste.insert(axon)
        return liste
    def getAxonHigherThanDiametre(self,diametre):
        """
        :param diametre: the diametre minimum
        :return: a new axonList with all axon below diametre
        """
        liste=AxonList()
        for axon in self.__listAxon:
            if axon.getDiameter()>diametre:
                liste.insert(axon)
        return liste
    def getDiameterMean(self):
        """
        :return: the mean od the diametre of all axon
        """
        temp=0
        for axon in self.__listAxon:
            temp+=axon.getDiameter()
        return temp/self.getNbrAxon()

    def save(self, output):
        """
        :param output: file where to save
        """
        try:
            import _pickle as cPickle
        except:
            import pickle as cPickle
        fileFormat = output.split('.')[-1]
        if fileFormat == "csv":
            # In CSV, we ignore the tags, for now
            # TODO Find an alternative !
            f = open(output, 'w')
            for axon in self.__listAxon:
                current = axon.toArray()
                for i in range(len(current)-1):
                    if "float" in str(type(current[i])):
                        current[i] = "%.10f" % current[i]
                listAxon = ','.join(current[:-1])
                f.write(listAxon + "\n")
            f.seek(0,0)
            f.close()
            
        else:
            if output[-4:] != ".bin":
                output += ".bin"
            cPickle.dump(self.__listAxon, open(output, "wb"))

    def load(self, inputFile):
        """
        :param output: file where to save
        :param format: format to save into
        """
        try:
            import _pickle as cPickle
        except:
            import pickle as cPickle
        if inputFile.split('.')[-1] != "bin":
            #  TODO Import CSV ?
            print("Sorry, can only import binary numpy arrays for now !\n\tSo we can't import CSV for the moment.")
        else:
            self.__listAxon = cPickle.load(open(inputFile, "rb"))


