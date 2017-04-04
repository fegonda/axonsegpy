import pyximport;pyximport.install()
from core.Axon import Axon
from core.AxonList import AxonList
import numpy as np
import os
from skimage import io
from skimage import color
from skimage import measure
from skimage import draw
from skimage import segmentation
from skimage import filters
import time
from algo import AxonSeg
from algo import GenMask
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



def segMeylinExperimental(axon,image,labeledMask,deltaVecs,snake = False, verbose = False,maxMeylinWidth = 15,diffDegree = 1):
    meylin = np.zeros((2, 72, 2),dtype = np.int)


    thisDelta = deltaVecs.copy()
    pos = np.array([[axon.getPosx(), axon.getPosy()]])
    currentPos = np.zeros((72, 2))
    myLabel = labeledMask[int(axon.getPosx())][int(axon.getPosy())]

    for i in range(72):
        currentPos[i] = pos
    progress = np.zeros(72, dtype = np.uint8)
    progressValue = np.sum(progress)

    while(progressValue != 72):
        currentPos = currentPos + thisDelta
        rounded = np.around(currentPos)
        for i in range(72):
            x = int(rounded[i][0])
            y = int(rounded[i][1])
            if x >= 0 and x < image.shape[0] and y >= 0 and y < image.shape[1] :
                if progress[i]==0:
                    labelVal = labeledMask[x][y]
                    if labelVal != myLabel:
                        meylin[0][i] = [x, y]
                        progress[i] = 1
            else:
                meylin[0][i][0] = max(0, min(x, image.shape[0] - 1))
                meylin[0][i][1] = max(0, min(y, image.shape[1] - 1))
                progress[i] = 1
        progressValue = np.sum(progress)
    # initiate radial value map
    currentPos = meylin[0].copy()

    pixels = np.zeros((72, maxMeylinWidth), dtype=np.float)
    coords = np.zeros((72, maxMeylinWidth, 2), dtype=np.int)
    for i in range(maxMeylinWidth):
        currentPos = currentPos + thisDelta
        rounded = np.around(currentPos)
        for j in range(72):
            x = int(rounded[j][0])
            y = int(rounded[j][1])
            if image.shape[0] > x >= 0 and image.shape[1] > y >= 0:
                coords[j][i] = [x, y]
                pixels[j][i] = image[x][y]
            else:
                coords[j][i] = [-1, -1]
                pixels[j][i] = 0

    dif = np.diff(pixels, n=diffDegree)
    np.set_printoptions(threshold=np.nan)
    for i in range(72):
        index = np.argmin(dif[i])
        meylin[1][i]= coords[i][index]

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
    total = len(axonList.getAxonList())

    for axon in axonList.getAxonList():
        if(verbose):
            b+=1
            if(c*total<b):
                print(round(c*100),'%')
                c+=0.1

        #print(i,len(axonList.getAxoneList()))
        segMeylinExperimental(axon,image,labeledMask,deltaVecs)



def MeylinVisualisation(image, axonList,size = 1):
    retImage = np.zeros(image.shape,dtype=np.uint8)
    dist = int((size-1)/2)
    a = 0
    for axon in axonList.getAxonList():
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
    for axon in axonList.getAxonList():
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
    for axon in axonList.getAxonList():
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
    for axon in axonList.getAxonList():
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
    print(mean,len(axonList.getAxonList()))

    MeylinSeg(testImage,axonList,verbose = True)

    meylinVisual = MeylinVisualisation(testImage,axonList)
    meylinVisual = meylinVisual*0.5+testImage*0.5
    meylinVisual = np.maximum(meylinVisual.astype(np.int),axonList.axonMask)
    io.imsave('../../test/meylinVisual.png', meylinVisual)

    io.imsave('../../test/minima.png', axonList.minima)



def run(params):
    filename = params["input"]
    testImage = io.imread(filename)
    outputImg = params["outputImage"]
    outputLst = params["outputList"]

    if "inputList" in params:
        melynList=AxonList.load(params["inputList"])
    else:
        melynList=AxonSeg.axonSeg(testImage,{"minSize":30,"maxSize":1000,"Solidity":0.7,"MinorMajorRatio":0.85},True)

    MeylinSeg(testImage,melynList,verbose = True)

    meylinVisual = MeylinVisualisation(testImage,melynList)
    meylinVisual = meylinVisual*0.5+testImage*0.5
    meylinVisual = np.maximum(meylinVisual.astype(np.int),melynList.axonMask)
    io.imsave(outputImg, meylinVisual)

    melynList.save(outputLst)

#test()
