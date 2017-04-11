
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
from skimage.segmentation import active_contour
try:
    import cython
    import pyximport
    pyximport.install()
    from cythonLib import GenMask
except:
    from lib import GenMask

def segMyelin(axon,image,labeledMask,deltaVecs,snake = False, verbose = False,maxMyelinWidth = 15,diffDegree = 1, outlierDifinition = 1, nbIterations = 5):
    myelin = np.zeros((2, 72, 2),dtype = np.int)


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
                        myelin[0][i] = [x, y]
                        progress[i] = 1
            else:
                myelin[0][i][0] = max(0, min(x, image.shape[0] - 1))
                myelin[0][i][1] = max(0, min(y, image.shape[1] - 1))
                progress[i] = 1
        progressValue = np.sum(progress)
    # initiate radial value map
    currentPos = myelin[0].copy()

    pixels = np.zeros((72, maxMyelinWidth), dtype=np.float)
    coords = np.zeros((72, maxMyelinWidth, 2), dtype=np.int)
    for i in range(maxMyelinWidth):
        rounded = np.around(currentPos)
        currentPos = currentPos + thisDelta
        for j in range(72):
            x = int(rounded[j][0])
            y = int(rounded[j][1])
            if image.shape[0] > x >= 0 and image.shape[1] > y >= 0:
                coords[j][i] = [x, y]
                pixels[j][i] = image[x][y]
            else:
                coords[j][i] = [-1, -1]
                pixels[j][i] = 0

    pixels = filters.gaussian(pixels,sigma =1)
    dif = np.diff(pixels, n=diffDegree)
    np.set_printoptions(threshold=np.nan)
    sizes = np.zeros(72)
    for i in range(72):
        index = np.argmin(dif[i])
        if coords[i][index][0] == -1:
            index -= 1
        myelin[1][i] = coords[i][index]
        sizes[i] = index

    for i in range(nbIterations):
        average = np.average(sizes)
        std = max(np.std(sizes) * outlierDifinition,1)
        minSlice = max(int(average - std),0)
        maxSlice = min(int(average + std),maxMyelinWidth)
        #print(minSlice,maxSlice,average,average + std)
        for i in range(72):
            if sizes[i]< minSlice or sizes[i]> maxSlice:
                slice = dif[i][minSlice:maxSlice]
                index = np.argmin(slice) + minSlice
                if coords[i][index][0] != -1:
                    myelin[1][i] = coords[i][index]
                    sizes[i] = index

    if(snake):
        myelin[0] = active_contour(image, myelin[0].astype(dtype = np.float64), alpha=0.015, beta=10, gamma=0.001, w_line=0, w_edge=1, bc='periodic',
                       max_px_move=1.0, max_iterations=3, convergence=0.1).astype(dtype = np.int)
        myelin[1] = active_contour(image, myelin[1].astype(dtype = np.float64), alpha=0.015, beta=10, gamma=0.001, w_edge=1 , bc='periodic',
                       max_px_move=1.0, max_iterations=3, convergence=0.1).astype(dtype = np.int)

    axon.setMyelin(myelin)



def MyelinSeg(image, axonList,verbose = False, maxWidth = 15, diff = 1, outlier = 1):
    unitVec = np.array([1,0])
    deltaVecs = np.zeros((72,2))
    if(verbose):
        print("Myelin segmentation Started")
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
                #print(round(c*100),'%')
                c+=0.1

        #print(i,len(axonList.getAxoneList()))
        segMyelin(axon,image,labeledMask,deltaVecs,maxMyelinWidth = maxWidth, diffDegree= diff, outlierDifinition = outlier)

def MyelinVisualisation(image, axonList,size = 1):
    retImage = np.zeros(image.shape,dtype=np.uint8)
    dist = int((size-1)/2)
    a = 0
    for axon in axonList.getAxonList():
        a+=1
        for i in range(72):
            for x in range(axon.getMyelin()[0][i][0]-dist,axon.getMyelin()[0][i][0]+dist+1):
                for y in range(axon.getMyelin()[0][i][1]-dist,axon.getMyelin()[0][i][1]+dist+1):
                    if(x>=0 and x< retImage.shape[0] and y>=0 and y<retImage.shape[1]):
                        retImage[x][y] = 127

            for x in range(axon.getMyelin()[1][i][0]-dist,axon.getMyelin()[1][i][0]+dist+1):
                for y in range(axon.getMyelin()[1][i][1]-dist,axon.getMyelin()[1][i][1]+dist+1):
                    if(x>=0 and x< retImage.shape[0] and y>=0 and y<retImage.shape[1]):
                        retImage[x][y] = 255

    return retImage

def MyelinVisualisationFancy(image, axonList):
    retImage = np.zeros(image.shape, dtype=np.uint8)
    a = 0
    for axon in axonList.getAxonList():
        #print(a)
        a += 1
        for i in range(72):
            for vertex in range(72):
                startpoint = axon.getMyelin()[0][vertex]
                try:
                    endpoint = axon.getMyelin()[0][vertex + 1]
                except IndexError:
                    endpoint = axon.getMyelin()[0][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc] = val * 255

            for vertex in range(72):
                startpoint = axon.getMyelin()[1][vertex]
                try:
                    endpoint = axon.getMyelin()[1][vertex + 1]
                except IndexError:
                    endpoint = axon.getMyelin()[1][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc] = val * 255

    return retImage

def MyelinVisualisationSuperFancy(image, axonList,min,max):
    retImage = np.zeros((image.shape[0],image.shape[1],3), dtype=np.uint8)
    a = 0
    for axon in axonList.getAxonList():
        #print(a)
        a += 1
        axonDiam = axon.getAvMyelinDiameter()
        redValue = 1- (max-axonDiam)/(max-min)
        blueValue = 1 - (axonDiam-min) / (max - min)

        for i in range(72):
            for vertex in range(72):
                startpoint = axon.getMyelin()[0][vertex]
                try:
                    endpoint = axon.getMyelin()[0][vertex + 1]
                except IndexError:
                    endpoint = axon.getMyelin()[0][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc,0] = val * 255*redValue
                retImage[rr, cc,2] = val * 255*blueValue

            for vertex in range(72):
                startpoint = axon.getMyelin()[1][vertex]
                try:
                    endpoint = axon.getMyelin()[1][vertex + 1]
                except IndexError:
                    endpoint = axon.getMyelin()[1][0]
                # The exception means We have reached the end and need to complete the polygon
                rr, cc, val = draw.line_aa(startpoint[0], startpoint[1], endpoint[0], endpoint[1])
                retImage[rr, cc,0] = val * 255*redValue
                retImage[rr, cc,2] = val * 255*blueValue

    return retImage

def MyelinVisualisationSuperDuperFancy(image, axonList):
    min = 999
    max = -1
    for axon in axonList.getAxonList():
        if axon.getAvMyelinDiameter()<min:
            min = axon.getAvMyelinDiameter()
        if axon.getAvMyelinDiameter()>max:
            max = axon.getAvMyelinDiameter()
    retImage = np.zeros((image.shape[0],image.shape[1],3), dtype=np.uint8)
    a = 0
    for axon in axonList.getAxonList():
        #print(a)
        a += 1
        axonDiam = axon.getAvMyelinDiameter()
        redValue = 1- (max-axonDiam)/(max-min)
        blueValue = 1 - (axonDiam-min) / (max - min)

        xs = axon.getMyelin()[1][:,0]
        ys = axon.getMyelin()[1][:,1]
        for i in range(72):
            rr, cc = draw.polygon(xs,ys)
            retImage[rr, cc,0] =  255*redValue
            retImage[rr, cc,2] =  255*blueValue

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j]!=0:
                retImage[i][j][0]= 0
                retImage[i][j][2]= 0
    return retImage


def test():
    filename = os.path.join('C:\\Users\\Zihui\\PycharmProjects\\INF49x0-Projet_4-NeuroPoly\\tests\\SegTest', '20160830_CARS_Begin_07.tif')
    testImage = io.imread(filename, as_grey=True)

    axonList=AxonSeg.axonSeg(testImage,{"minSize":30,"maxSize":1000,"Solidity":0.7,"MinorMajorRatio":0.85},True)

    io.imsave('C:\\Users\\Zihui\\PycharmProjects\\INF49x0-Projet_4-NeuroPoly\\tests\\SegTest\\axonMask.png', axonList.axonMask)

    mean=axonList.getDiameterMean();
    print(mean,len(axonList.getAxonList()))

    MyelinSeg(testImage,axonList,verbose = True)

    myelinVisual = MyelinVisualisationSuperDuperFancy(axonList.axonMask,axonList)
#    myelinVisual = myelinVisual*0.5+testImage*0.5
#    myelinVisual = np.maximum(myelinVisual.astype(np.int),axonList.axonMask)
    io.imsave('C:\\Users\\Zihui\\PycharmProjects\\INF49x0-Projet_4-NeuroPoly\\tests\\SegTest\\myelinVisual.png', myelinVisual)

    io.imsave('C:\\Users\\Zihui\\PycharmProjects\\INF49x0-Projet_4-NeuroPoly\\tests\\SegTest\\minima.png', axonList.minima)






def run(params):
    """
    Run function for myelin segmentation
    :param params: All the parameters inside a dictionnary
    input: path to input image REQUIRED
    inputList : path to input axonList with the axon segmented, if absent, will generate own. 
    outputImage : path to output image REQUIRED
    outputList: path to output axonList REQUIRED
    verbose : default false
    maxWidth: max myelin thickness, default = 15
    diff: the number times values are differenced in a numpy.diff, default = 1
    outlier: the number of times outlier detection is run, default = 1
    display: the type of output image it to save. normal or full. Default = normal
    :return: 
    """
    filename = params["input"]
    testImage = io.imread(filename, as_grey=True)
    outputImg = params["outputImage"]
    outputLst = params["outputList"]

    if "inputList" in params:
        melynList=AxonList.load(params["inputList"])
    else:
        melynList=AxonSeg.axonSeg(testImage,{"minSize":30,"maxSize":1000,"Solidity":0.7,"MinorMajorRatio":0.85},True)

    if "verbose" in params:
        v = params["verbose"] is "True"
    else:
        v = False

    if "maxWidth" in params:
        w = int(params["maxWidth"])
    else:
        w = 15

    if "diff" in params:
        d = int(params["diff"])
    else:
        d = 1

    if "outlier" in params:
        o = int(params["outlier"])
    else:
        o = 1


    MyelinSeg(testImage,melynList,verbose = v,maxWidth=w,diff=d,outlier=o)

    if "display" in params and params["display"] == "full":
        myelinVisual = MyelinVisualisationSuperDuperFancy(melynList.axonMask,melynList)
    else:
        myelinVisual = MyelinVisualisation(testImage,melynList)
        myelinVisual = myelinVisual*0.5+testImage*0.5
        myelinVisual = np.maximum(myelinVisual.astype(np.int),melynList.axonMask)
    io.imsave(outputImg, myelinVisual)

    melynList.save(outputLst)


#test()
