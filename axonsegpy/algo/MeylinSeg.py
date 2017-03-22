import pyximport;pyximport.install()
from Axon import Axone
from AxonList import AxoneList
import numpy as np
import os
from skimage import io
from skimage import color
from skimage import measure
from skimage import draw
from skimage import segmentation
from skimage import filters
import time
import AxonSeg
import GenMask
from skimage.segmentation import active_contour

def segMeylin(axon,image,labeledMask,deltaVecs,snake = False, verbose = False):
    meylin = np.zeros((2, 72, 2),dtype = np.int)
    thisDelta = deltaVecs.copy()
    pos = np.array([[axon.getPosx(), axon.getPosy()]])
    currentPos = np.zeros((72, 2))
    myLabel = labeledMask[int(axon.getPosx())][int(axon.getPosy())]
    for i in range(72):
        currentPos[i] = pos
    progress = np.zeros(72, dtype = np.uint8)
    lastVal = np.zeros(72,dtype = np.int)
    progressValue = np.sum(progress)
    while(progressValue != 72*2):
        currentPos = currentPos + thisDelta
        rounded = np.around(currentPos)
        for i in range(72):
            x = int(rounded[i][0])
            y = int(rounded[i][1])

            if progress[i]==0:
                if (x >= 0 and x < image.shape[0] and y >= 0 and y < image.shape[1]):
                    labelVal = labeledMask[x][y]
                    if labelVal != myLabel:
                        progress[i] +=1
                        meylin[0][i][0] = x
                        meylin[0][i][1] = y
                        lastVal[i] = image[x][y]
                else:
                    progress[i] +=2
                    meylin[0][i][0] = max(0, min(x, image.shape[0]-1))
                    meylin[0][i][1] = max(0, min(y, image.shape[1]-1))
                    meylin[1][i][0] = max(0, min(x, image.shape[0]-1))
                    meylin[1][i][1] = max(0, min(y, image.shape[1]-1))

            elif progress[i]==1:
                if (x >= 0 and x < image.shape[0] and y >= 0 and y < image.shape[1] and progressValue < 150):
                    deltaVal = image[x][y]-lastVal[i]
                    lastVal[i] = image[x][y]
                    if deltaVal<-20 or lastVal[i]<29:
                        progress[i] += 1
                        meylin[1][i][0] = int(rounded[i][0])
                        meylin[1][i][1] = int(rounded[i][1])
                else:
                    progress[i] +=1
                    meylin[1][i][0] = max(0, min(x, image.shape[0]-1))
                    meylin[1][i][1] = max(0, min(y, image.shape[1]-1))
                progressValue = np.sum(progress)

    if(snake):
        meylin[0] = active_contour(image, meylin[0].astype(dtype = np.float64), alpha=0.015, beta=10, gamma=0.001, w_line=0, w_edge=1, bc='periodic',
                       max_px_move=1.0, max_iterations=3, convergence=0.1).astype(dtype = np.int)
        meylin[1] = active_contour(image, meylin[1].astype(dtype = np.float64), alpha=0.015, beta=10, gamma=0.001, w_edge=1 , bc='periodic',
                       max_px_move=1.0, max_iterations=3, convergence=0.1).astype(dtype = np.int)

    axon.setMeylin(meylin)


def MeylinSeg(image, axonList,verbose = False):
    unitVec = np.array([1,0])
    deltaVecs = np.zeros((72,2))
    if(verbose):
        print("Meylin segmentation Started")
    labeledMask = measure.label(axonList.axonMask)
    if(verbose):
        print("Labeled mask created")

    for a in range(72):
        rotMat = np.array([[np.cos(a/36*np.pi),-np.sin(a/36*np.pi)],[np.sin(a/36*np.pi),np.cos(a/36*np.pi)]])
        deltaVecs[a] = np.matmul(unitVec,rotMat)
    i = 0

    b= 0
    c = 0
    total = len(axonList.getAxoneList())

    for axon in axonList.getAxoneList():
        if(verbose):
            b+=1
            if(c*total<b):
                print(round(c*100),'%')
                c+=0.1

        #print(i,len(axonList.getAxoneList()))
        i+=1
        segMeylin(axon,image,labeledMask,deltaVecs,snake = True)


def MeylinVisualisation(image, axonList,size = 1):
    retImage = np.zeros(image.shape,dtype=np.uint8)
    dist = int((size-1)/2)
    a = 0
    for axon in axonList.getAxoneList():
        a+=1
        for i in range(72):
            for x in range(axon.getMeylin()[0][i][0]-dist,axon.getMeylin()[0][i][0]+dist+1):
                for y in range(axon.getMeylin()[0][i][1]-dist,axon.getMeylin()[0][i][1]+dist+1):
                    if(x>=0 and x< retImage.shape[0] and y>=0 and y<retImage.shape[1]):
                        retImage[x][y] = 127

            for x in range(axon.getMeylin()[1][i][0]-dist,axon.getMeylin()[1][i][0]+dist+1):
                for y in range(axon.getMeylin()[1][i][1]-dist,axon.getMeylin()[1][i][1]+dist+1):
                    if(x>=0 and x< retImage.shape[0] and y>=0 and y<retImage.shape[1]):
                        retImage[x][y] = 255

    return retImage

def MeylinVisualisationFancy(image, axonList):
    retImage = np.zeros(image.shape, dtype=np.uint8)
    a = 0
    for axon in axonList.getAxoneList():
        #print(a)
        a += 1
        for i in range(72):
            for vertex in range(72):
                startpoint = axon.getMeylin()[0][vertex]
                try:
                    endpoint = axon.getMeylin()[0][vertex + 1]
                except IndexError:
                    endpoint = axon.getMeylin()[0][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc] = val * 255

            for vertex in range(72):
                startpoint = axon.getMeylin()[1][vertex]
                try:
                    endpoint = axon.getMeylin()[1][vertex + 1]
                except IndexError:
                    endpoint = axon.getMeylin()[1][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc] = val * 255

    return retImage

def MeylinVisualisationSuperFancy(image, axonList,min,max):
    retImage = np.zeros((image.shape[0],image.shape[1],3), dtype=np.uint8)
    a = 0
    for axon in axonList.getAxoneList():
        #print(a)
        a += 1
        axonDiam = axon.getAvMeylinDiameter()
        redValue = 1- (max-axonDiam)/(max-min)
        blueValue = 1 - (axonDiam-min) / (max - min)

        for i in range(72):
            for vertex in range(72):
                startpoint = axon.getMeylin()[0][vertex]
                try:
                    endpoint = axon.getMeylin()[0][vertex + 1]
                except IndexError:
                    endpoint = axon.getMeylin()[0][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc,0] = val * 255*redValue
                retImage[rr, cc,2] = val * 255*blueValue

            for vertex in range(72):
                startpoint = axon.getMeylin()[1][vertex]
                try:
                    endpoint = axon.getMeylin()[1][vertex + 1]
                except IndexError:
                    endpoint = axon.getMeylin()[1][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc,0] = val * 255*redValue
                retImage[rr, cc,2] = val * 255*blueValue

    return retImage

def MeylinVisualisationSuperDuperFancy(image, axonList,min,max):
    retImage = np.zeros((image.shape[0],image.shape[1],3), dtype=np.uint8)
    a = 0
    for axon in axonList.getAxoneList():
        #print(a)
        a += 1
        axonDiam = axon.getAvMeylinDiameter()
        redValue = 1- (max-axonDiam)/(max-min)
        blueValue = 1 - (axonDiam-min) / (max - min)

        xs = axon.getMeylin()[1][:,0]
        ys = axon.getMeylin()[1][:,1]
        for i in range(72):
            rr, cc = draw.polygon(xs,ys)
            retImage[rr, cc,0] =  255*redValue
            retImage[rr, cc,2] =  255*blueValue
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(image[i][j]!=0):
                retImage[i][j][0]= 0
                retImage[i][j][2]=0
    return retImage


def test():
    filename = os.path.join('../../test/SegTest/', '20160830_CARS_Begin_07.tif')
    testImage = io.imread(filename)

    axonList=AxonSeg.axonSeg(testImage,{"minSize":30,"maxSize":1000,"Solidity":0.7,"MinorMajorRatio":0.85},True)

    io.imsave('../../test/axonMask.png', axonList.axonMask)

    mean=axonList.getDiameterMean();
    print(mean,len(axonList.getAxoneList()))

    MeylinSeg(testImage,axonList,verbose = True)

    meylinVisual = MeylinVisualisation(testImage,axonList)
    meylinVisual = meylinVisual*0.5+testImage*0.5
    meylinVisual = np.maximum(meylinVisual.astype(np.int),axonList.axonMask)
    io.imsave('../../test/meylinVisual.png', meylinVisual)

    io.imsave('../../test/minima.png', axonList.minima)



def run(params):
    filename = params["input"]
    meylinFile = params["meylinImage"]
    outputImg = params["outputImage"]
    outputLst = params["outputList"]

    testImage = io.imread(filename)
    meylinImage = io.imread(meylinFile)
    melynList=AxonSeg.axonSeg(testImage,{"minSize":30,"Solidity":0.3,"MinorMajorRatio":0.1})
    mask = GenMask.generateAxonMask(testImage,melynList)


    MeylinSeg(meylinImage,melynList,mask)
    minV = 9999
    maxV = -1
    for axon in melynList.getAxoneList():
        diam = axon.getAvMeylinDiameter()
        if diam>max:
            max = diam
        if diam<min:
            min = diam
    print(min,max)
    meylinVisual = MeylinVisualisation(testImage,list)
    io.imsave('../../test/meylinVisual.png', meylinVisual)

    melynList.save(outputLst)
    io.imsave(outputImg, meylinVisual)

