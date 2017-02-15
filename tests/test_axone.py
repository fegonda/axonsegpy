
import sys
import Axone
import AxoneList
sys.path.insert(1, '../axonsegpy')

######################################
# Class AxoneTest will test methode  #
# from Axone  and AxoneList          #
######################################

#The call our test#
def test():
    testAxone()
    testAxoneListe()
    testEqAxoneList()
    testAxoneListAdd()
    testAxoneUnderDiametre()
#Check if the axone object works#
def testAxone():
    axone1 = Axone.Axone(33,47,12)
    assert(axone1.getDiametre()==12)

#Check if the axoneList object works#
def testAxoneListe():
    axone1 = Axone.Axone(33, 47, 12)
    axoneList1=AxoneList.AxoneList()
    axoneList1.insert(axone1)
    assert(axoneList1.getNbrAxone()==1)

#Check if the overloading of == works#
def testEqAxoneList():
    # Creating Axone
    axone1 = Axone.Axone(33, 47, 12)

    axoneList1 = AxoneList.AxoneList()
    axoneList1.insert(axone1)

    axoneList2 = AxoneList.AxoneList()
    axoneList2.insert(axone1)

    assert(axoneList2==axoneList1)

#Check if the overloading of + works#
def testAxoneListAdd():
    # Creating Axone
    axone1 = Axone.Axone(33,47,12)
    axone2= Axone.Axone(74,21,47)

    axoneList1=AxoneList.AxoneList()
    axoneList1.insert(axone1)

    axoneList2 = AxoneList.AxoneList()
    axoneList2.insert(axone2)

    axoneList3 = AxoneList.AxoneList()
    axoneList3=axoneList1+axoneList2

    axoneList1.insert(axone2)
    assert(axoneList3==axoneList1)
#Check if the function getAxoneUnderDiametre works#
def testAxoneUnderDiametre():
    #Creating Axone
    axone1 = Axone.Axone(33, 47, 12)
    axone2 = Axone.Axone(74, 21, 47)
    axone3 = Axone.Axone(33, 47, 25)

    axoneList1=AxoneList.AxoneList()
    axoneList1.insert(axone1)
    axoneList1.insert(axone2)
    axoneList1.insert(axone3)

    axoneList2 = AxoneList.AxoneList()
    axoneList2 = axoneList1.getAxoneUnderDiametre(30)

    axoneList3 = AxoneList.AxoneList()
    axoneList3.insert(axone1)
    axoneList3.insert(axone3)

    assert(axoneList3==axoneList1)
