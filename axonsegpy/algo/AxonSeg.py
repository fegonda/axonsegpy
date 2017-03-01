
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
    props = (measure.regionprops(measure.label(image)))
    axonList = AxoneList();
    b= 0
    for region in props:
        current = Axone(region)
        valid = True
        if "minSize" in params:
            if(region.area<params["minSize"]):
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
            b = b+1
    return axonList


def run(params):
    f_input = params["input"]
    try:
        f_output = params["output"]
    except KeyError:
        f_output = f_input + ".list.bin"
    image = io.imread(f_input)
    axonList=axonSeg(image,{"minSize":30,"Solidity":0.3,"MinorMajorRatio":0.1})
    axonList.save(f_output)
