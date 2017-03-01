import pyximport;pyximport.install()
from Axon import Axone
from AxonList import AxoneList
import numpy as np
import os
from skimage import io
from skimage import color
from skimage import measure
from skimage import draw
import time
import AxonSeg
import GenMask


def segMeylin(axon,image,labeledMask,deltaVecs):
    meylin = np.zeros((2, 72, 2),dtype = np.int)
    thisDelta = deltaVecs.copy()
    pos = np.array([[axon.getPosx(), axon.getPosy()]])
    currentPos = np.zeros((72, 2))
    myLabel = labeledMask[int(axon.getPosx())][int(axon.getPosy())]
    for i in range(72):
        currentPos[i] = pos
    progress = np.zeros(72, dtype = np.uint8)

    while(np.sum(progress)!=72*2):
        currentPos = currentPos + thisDelta
        rounded = np.around(currentPos)
        for i in range(72):
            if progress[i]==0:
                labelVal = labeledMask[int(rounded[i][0])][int(rounded[i][1])]
                if labelVal != myLabel:
                    progress[i] +=1
                    meylin[0][i][0] = int(rounded[i][0])
                    meylin[0][i][1] = int(rounded[i][1])
            elif progress[i]==1:
                meylinMaskVal = image[int(rounded[i][0])][int(rounded[i][1])]
                if meylinMaskVal == 0:
                    progress[i] += 1
                    meylin[1][i][0] = int(rounded[i][0])
                    meylin[1][i][1] = int(rounded[i][1])
    axon.setMeylin(meylin)


def MeylinSeg(image, axonList, mask):
    unitVec = np.array([1,0])
    deltaVecs = np.zeros((72,2))
    labeledMask = measure.label(mask)

    for a in range(72):
        rotMat = np.array([[np.cos(a/36*np.pi),-np.sin(a/36*np.pi)],[np.sin(a/36*np.pi),np.cos(a/36*np.pi)]])
        deltaVecs[a] = np.matmul(unitVec,rotMat)
    i = 0
    for axon in axonList.getAxoneList():
        #print(i,len(axonList.getAxoneList()))
        i+=1
        segMeylin(axon,image,labeledMask,deltaVecs)



def MeylinVisualisation(image, axonList):
    retImage = np.zeros(image.shape,dtype=np.int)
    for axon in axonList.getAxoneList():
        for i in range(72):
            retImage[axon.getMeylin()[0][i][0]-1][axon.getMeylin()[0][i][1]-1] = 127
            retImage[axon.getMeylin()[0][i][0]-1][axon.getMeylin()[0][i][1]] = 127
            retImage[axon.getMeylin()[0][i][0]-1][axon.getMeylin()[0][i][1]+1] = 127
            retImage[axon.getMeylin()[0][i][0]][axon.getMeylin()[0][i][1]-1] = 127
            retImage[axon.getMeylin()[0][i][0]][axon.getMeylin()[0][i][1]] = 127
            retImage[axon.getMeylin()[0][i][0]][axon.getMeylin()[0][i][1]+1] = 127
            retImage[axon.getMeylin()[0][i][0]+1][axon.getMeylin()[0][i][1]-1] = 127
            retImage[axon.getMeylin()[0][i][0]+1][axon.getMeylin()[0][i][1]] = 127
            retImage[axon.getMeylin()[0][i][0]+1][axon.getMeylin()[0][i][1]+1] = 127

            retImage[axon.getMeylin()[1][i][0]-1][axon.getMeylin()[1][i][1]-1] = 127
            retImage[axon.getMeylin()[1][i][0]-1][axon.getMeylin()[1][i][1]] = 127
            retImage[axon.getMeylin()[1][i][0]-1][axon.getMeylin()[1][i][1]+1] = 127
            retImage[axon.getMeylin()[1][i][0]][axon.getMeylin()[1][i][1]-1] = 127
            retImage[axon.getMeylin()[1][i][0]][axon.getMeylin()[1][i][1]] = 127
            retImage[axon.getMeylin()[1][i][0]][axon.getMeylin()[1][i][1]+1] = 127
            retImage[axon.getMeylin()[1][i][0]+1][axon.getMeylin()[1][i][1]-1] = 127
            retImage[axon.getMeylin()[1][i][0]+1][axon.getMeylin()[1][i][1]] = 127
            retImage[axon.getMeylin()[1][i][0]+1][axon.getMeylin()[1][i][1]+1] = 127
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
        if diam>maxV:
            maxV = diam
        if diam<minV:
            minV = diam
    #print(minV,maxV)
    meylinVisual = MeylinVisualisation(testImage,melynList)
    melynList.save(outputLst)
    io.imsave(outputImg, meylinVisual)