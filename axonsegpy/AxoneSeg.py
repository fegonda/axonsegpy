
from Axon import Axone
from AxonList import AxoneList
import numpy as np
import os
from skimage import io
from skimage import color
from skimage import measure
import time
import cProfile


def axonSeg(image, params):
    """
    Segmentation d'axon
    :param image: Image lu
    :param params:
    :return:AxonList de tous les axon trouves
    """
    print("WWW")
    image = measure.label(image)
    props = (measure.regionprops(image))
    list = AxoneList();
    b= 0
    for region in props:
        current = Axone(region)
        valid = True
        if "minSize" in params:
            if(region.area<params["minSize"]):
                valid = False
        if valid:
            if "-" in params:
                if(region.solidity< params["Solidity"]):
                    valid = False

        if valid:
            if "MinorMajorRatio" in params:
                if(region.eccentricity< params["MinorMajorRatio"]):
                    valid = False
        if valid:
            list.insert(current)
            b = b+1
    print(b)
    return list


def test():
    filename = os.path.join('../test/SegTest/', 'w1.png')
    testImage =     moon = io.imread(filename)
    list=axonSeg(testImage,{"minSize":30,"Solidity":0.3,"MinorMajorRatio":0.1})
    mean=list.getDiameterMean();
    print(mean)
test()

