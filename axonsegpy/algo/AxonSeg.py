#import pyximport;pyximport.install()
from core.Axon import Axon
from core.AxonList import AxonList
import numpy as np
import os
from skimage import io
from skimage import color
from skimage import measure
import time
import cProfile
from decimal import *

try:
    import cython
    import pyximport
    pyximport.install()
    from cythonLib import GenMask
    from cythonLib import minima
except:
    from lib import minima
    from lib import GenMask



def axonSeg(image, params,verbose = True):
    """
    Segmentation d'axon
    :param image: Image lu
    :param params:
    :return:AxonList de tous les axon trouves
    """

    h = 0
    if('h' in params):
        h= params['h']
    else:
        h = image.std()
    if verbose:
        print("Axon seg started, params=",params)
    minImage = minima.imExtendedMin(image, h)

    if verbose:
        print("Minima ended")
    props = (measure.regionprops(measure.label(minImage)))

    if verbose:
        print("RegionProps ended regions found:",len(props))
    axonList = AxonList();
    axonList.axonMask = minImage
    b= 0
    c = Decimal(0)
    total = len(props)
    for region in props:
        if(verbose):
            b+=1
            if(c*total<b):
                print(round(c*Decimal(100)),'%')
                c+=Decimal(0.1)


        current = Axon(region)
        valid = True
        if "minSize" in params:
            if(region.area<params["minSize"]):
                valid = False

        if valid:
            if "maxSize" in params:
                if (region.area > params["maxSize"]):
                    valid = False

        if valid:
            if "Solidity" in params:
                if(region.solidity< params["Solidity"]):
                    valid = False

        if valid:
            if "MinorMajorRatio" in params:
                if(region.eccentricity> params["MinorMajorRatio"]):
                    valid = False
        if valid:
            axonList.insert(current)

    if verbose:
        print("Axon seg ended, axon found:",len(axonList.getAxonList()))
        print("generating mask")
    axonList.axonMask = GenMask.generateAxonMask(axonList.axonMask, axonList)
    axonList.minima = minImage
    if verbose:
        print("AxonSeg ended")

    return axonList



def run(params):
    """
    " this methods run the algo
    :param params:  input for the alogo
    :return: no return , axonlist saved
    """
    f_input = params["input"]
    try:
        f_output = params["output"]
    except KeyError:
        f_output = f_input + ".list.bin"
    image = io.imread(f_input, as_grey=True)
    axonList=axonSeg(image,params)
    axonList.save(f_output)

    if "display" in params and params["display"] == "full":
        axonVisual = GenMask.axonVisualisation(axonList.axonMask, axonList)
    else:
        axonVisual = axonList.axonMask

    if "outputImage" in params:
        outputImg = params["outputImage"]
    else:
        outputImg = os.path.join(f_input,"axonMask")
    io.imsave(outputImg, axonVisual)




def test():
    """
    Test the algorithme
    :return:
    """
    filename = os.path.join('../../test/SegTest/', '20160830_CARS_Begin_07.tif')
    testImage = io.imread(filename, as_grey=True)
    list=axonSeg(testImage,{"minSize":30,"Solidity":0.75,"MinorMajorRatio":0.8})
    mean=list.getDiameterMean();
    print(mean,len(list.getAxonList()))
    io.imsave('../../test/axonMask.png', list.axonMask)
