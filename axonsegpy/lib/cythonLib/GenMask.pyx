import numpy as np
import os
from skimage import io
from skimage import color
from core.Axon import Axon
from core.AxonList import AxonList
import skimage
from libcpp.pair cimport pair
from libcpp.stack cimport stack
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void drawAxon(char[:,:]& image,char[:,:]& maskImage,int posX,int posY,int maskValue = 255) nogil:
    maskImage[posX][posY] = maskValue
    cdef int x,y,currentX,currentY
    x = posX
    y = posY
    cdef pair[int, int] p
    cdef stack[int] qX
    cdef stack[int] qY
    qX.push(x)
    qY.push(y)
    while(qX.size()!=0):
        currentX = qX.top()
        currentY = qY.top()
        qX.pop()
        qY.pop()
        for x in range(currentX-1,currentX+2):
            for y in range(currentY-1,currentY+2):
                if x>=0 and y >=0 and x<image.shape[0] and y<image.shape[1] and (not(x==currentX and y == currentY)):
                    if maskImage[x][y] == 0 and image[x][y] == -1:
                        maskImage[x][y] = maskValue
                        qX.push(x)
                        qY.push(y)


def generateAxonMask(image,axonList,maskValue = 255):
    cdef char[:, :] imageC = image.astype(np.uint8)
    cdef char [:,:] retImageC = np.zeros(image.shape, dtype=np.uint8)
    for axon in axonList.getAxonList():
        drawAxon(imageC,retImageC,int(axon.getPosx()),int(axon.getPosy()),maskValue)

    return np.array(retImageC)

def axonVisualisation(image,axonList,parameterDic, colorLow,colorHigh):

    cdef char[:, :] imageC = image.astype(np.uint8)
    cdef char [:,:] retImageC = np.zeros(image.shape, dtype=np.uint8)
    retImageTotal = np.zeros([image.shape[0],image.shape[1],3], dtype=np.uint8)
    min = 999
    max = -1
    for axon in axonList.getAxonList():
        current = parameterDic[axon]
        if current < min:
            min = current
        if current > max:
            max = current
    for axon in axonList.getAxonList():
        value = parameterDic[axon]
        value = int(((value - min)/(max-min))*254)+1
        drawAxon(imageC,retImageC,int(axon.getPosx()),int(axon.getPosy()),value)
        if(value<0):
            print(value)
    cdef x = image.shape[0]
    cdef y = image.shape[1]

    for i in range(x):
        for j in range(y):
            if retImageC[i][j] != 0:
                if(128<retImageC[i][j] < -128 ):
                    print(retImageC[i][j])
                retImageTotal[i][j] = (float(retImageC[i][j]+128)/255)*colorHigh + (1-float(retImageC[i][j]+128)/255)*colorLow
    return retImageTotal


def run(path):
    from algo import AxonSeg
    testImage = io.imread(path)
    list = AxonSeg.axonSeg(testImage, {"minSize": 30, "Solidity": 0.3, "MinorMajorRatio": 0.1})
    ret = generateAxonMask(testImage,list)
    io.imsave(path+'.png', ret)

