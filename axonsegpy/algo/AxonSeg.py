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
    from lib.cythonLib import GenMask
    from lib.cythonLib import minima
except:
    try:
        from lib.compiledLib import minima
        from lib.compiledLib import GenMask
    except: 
        from lib.compiledLib.osxpy2 import minima
        from lib.compiledLib.osxpy2 import GenMask



def axonSeg(image, params):
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
    verbose = False
    if "verbose" in params:
        verbose = params["verbose"]=="True"
    if verbose:
        print("Axon seg started, params=",params)
    axonMask  = None

    if "isMask" in params:
        if params["isMask"] == "True":
            axonMask = image

    if axonMask == None:
        axonMask = minima.imExtendedMin(image, h)


    if verbose:
        print("Minima ended")
    props = (measure.regionprops(measure.label(axonMask)))

    if verbose:
        print("RegionProps ended regions found:",len(props))
    axonList = AxonList();
    axonList.setAxonMask(axonMask)
    b= 0
    c = Decimal(0)
    total = len(props)
    isFilter = False
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
        else:
            isFilter = True

    if verbose:
        print("Axon seg ended, axon found:",len(axonList.getAxonList()))
        print("generating mask")
    if isFilter:
        axonList.setAxonMask(GenMask.generateAxonMask(axonList.getAxonMask(), axonList))
    if verbose:
        print("AxonSeg ended")

    return axonList



def run(params):
    """
    " this methods run the algo
    :param params:  input for the alogo
        input = input image
        output = output binary
        outputImage = output image path
        display = if == full color display, else axon mask only
        displayParam = Parameter to use for display "diameter" is default, no other parameters yet
        displayColorLow = color for the low part display, expects "R,G,B"
        displayColorHigh = color for the high part display, expects "R,G,B"
        minSize = minSize, if absent, not checked
        maxSize = maxSize, if absent, not checked 
        Solidity = solidity , if absent, not checked
        MinorMajorRatio = ratio between 90 degree lines, if absent, not checked
        verbose = if need verbose True/False, default false
        isMask = if the input image is already a axon mask, if == "True" will direcly get axon from it, for use with for instance axonDeepSeg
        
    :return: no return , axonlist saved
    """
    f_input = params["input"]
    try:
        f_output = params["output"]
    except KeyError:
        f_output = f_input + ".list.bin"
    image = io.imread(f_input, as_grey=True)
    axonList=axonSeg(image,params)

    if "display" in params and params["display"] == "full":
        dic = {}
        if "displayParam" in params:
            if params["displayParam"] == "diameter":
                for axon in axonList.getAxonList():
                    dic[axon] = axon.getDiameter()
            #elif to add more conditions
        if dic == {}:
            # default
            for axon in axonList.getAxonList():
                dic[axon] = axon.getDiameter()


        low = np.zeros(3)
        high = np.zeros(3)
        if "displayColorLow" in params:
            lowColors = params["displayColorLow"].split(",")
        else:
            lowColors = [0,0,255]
        if "displayColorHigh" in params:
            highColors = params["displayColorHigh"].split(",")
        else:
            highColors = [255, 0, 0]
        for i in range(3):
            low[i] = int(lowColors[i])
            high[i] = int(highColors[i])
        axonVisual = GenMask.axonVisualisation(axonList.getAxonMask(), axonList,dic,low,high)
    else:
        axonVisual = axonList.getAxonMask()

    if "outputImage" in params:
        outputImg = params["outputImage"]
    else:
        outputImg = os.path.join(f_input,"axonMask")
    io.imsave(outputImg, axonVisual)
    axonList.save(f_output)

    return axonList


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
    io.imsave('../../test/axonMask.png', list.getAxonMask())
