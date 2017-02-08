

import numpy as np
import os
from skimage import io
from skimage import color
import time
import cProfile
def formCluster(image,clusterMap):
    id = 1
    clusters = {}
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if (clusterMap[i, j] == 0):

                found = False
                adj = []
                for xDelta in range( -1,1):
                    for yDelta in range( -1, 0-2*xDelta):
                        x = xDelta+i
                        y = yDelta+j
                        if (x >= 0 and x < image.shape[0] and y >= 0 and y < image.shape[1]):
                            if(image[x][y]==image[i][j]):
                                found = clusterMap[x][y]
                            else:
                                adj.append(clusterMap[x][y])

                if(found is False):
                    found = id
                    clusters[id] = [id, image[i, j], [id], {}, 0]
                    id = id + 1

                clusterMap[i,j]= found
                for adjacent in adj:
                    if adjacent not in clusters[found][3]:
                        clusters[found][3][adjacent]=True
                    if found not in clusters[adjacent][3]:
                        clusters[adjacent][3][found]=True

    return clusters

def isMinima(clusters,cluster):
    for adjacent in cluster[3]:
        if clusters[adjacent] is not None:
            if clusters[adjacent][1] < cluster[1]:
                return False
    return True

def merge(clusterA,clusterB,clusters):
    for pixel in clusterB[2]:
        clusterA[2].append(pixel)
    clusterA[4] = max(clusterA[4],clusterB[4])

    for i in clusterB[3]:
        del clusters[i][3][clusterB[0]]
        clusters[i][3][clusterA[0]] = True
        clusterA[3][i] = True

    del clusterA[3][clusterA[0]]
    clusters[clusterB[0]]=None


def getMinAround(cluster, clusters):
    min = 300
    toRemove = []
    for i in cluster[3]:
        if(clusters[i] is not None):
            if clusters[i][1]<min:
                min = clusters[i][1]
        else:
            toRemove.append(i)
    for i in toRemove:
        cluster[3].remove(i)
    ret = []
    for i in cluster[3]:
        if clusters[i][1]==min:
            ret.append(clusters[i])
    return ret

def imExtendedMin(image,h):
    clusterMap = np.zeros(image.shape,int)

    clusters = formCluster(image,clusterMap)
    minimas = []
    for key,cluster in clusters.items():
        if isMinima(clusters,cluster):
            minimas.append(cluster)
    print(len(minimas),len(clusters))


    done = []
    while(len(minimas)!= 0):
        current = minimas.pop()
        if clusters[current[0]]!=None:
            mins = getMinAround(current,clusters)
            if(len(mins)!= 0 ):
                if(current[1]+h-current[4] < mins[0][1]):
                    current[1] = current[1]+h
                    done.append(current)
                else:
                    move = mins[0][1]-current[1]
                    current[4] += move
                    current[1] += move
                    for toMerge in mins:
                        merge(current,toMerge,clusters)
                    if(isMinima(clusters,current)):
                        if(current[4]==h):
                            done.append(current)
                        else:
                            minimas.append(current)
            else:
                current[1] = current[1] + h
                done.append(current)

    ret = np.zeros(image.shape,int)
    minimaFinals = {}
    for current in done:
        for id in current[2]:
            minimaFinals[id]=True

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if clusterMap[i][j] in minimaFinals:
                ret[i][j]=255


    return ret


#cluster = [id value [pixels] [neibourghs id] ,reducedBy ]
def test():
    filename = os.path.join("/home/zihui/Desktop/", 'x.jpg')
    moon = io.imread(filename)
    moon = color.rgb2gray(moon)
    io.imsave('/home/zihui/Desktop/Test1.png', moon)

    for i in range(0, moon.shape[0]):
        for j in range(0, moon.shape[1]):
            moon[i, j] = int(moon[i, j] * 255)

    start = time.time()


    ret = imExtendedMin(moon,2)
    print(time.time()-start)
    io.imsave('/home/zihui/Desktop/Test.png', ret)


cProfile.run("test()")

