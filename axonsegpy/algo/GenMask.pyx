import numpy as np
import os
from skimage import io
from skimage import color
from core.Axon import Axone
from core.AxonList import AxoneList
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
    for axon in axonList.getAxoneList():
        drawAxon(imageC,retImageC,int(axon.getPosx()),int(axon.getPosy()),maskValue)

    return np.array(retImageC)



def run(path):
    from algo import AxonSeg
    testImage = io.imread(path)
    list = AxonSeg.axonSeg(testImage, {"minSize": 30, "Solidity": 0.3, "MinorMajorRatio": 0.1})
    ret = generateAxonMask(testImage,list)
    io.imsave(path+'.png', ret)

