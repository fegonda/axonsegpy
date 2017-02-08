cimport cython
import numpy as np
from cython.parallel import parallel, prange

import os
from skimage import io
from skimage import color
import time

from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp.pair cimport pair
from libcpp.set cimport set

from libc.stdlib cimport malloc,free
from cython.operator cimport dereference as deref,preincrement as inc

cdef struct group:
    int id
    int value
    vector[int] pixels
    set[int] adjacent
    int reducedBy
@cython.boundscheck(False)
@cython.wraparound(False)

#cluster = [id value [pixels] [neibourghs id] ,reducedBy ]
cdef group constructor( int id, int value) nogil:
    cdef group g
    g.id = id
    g.value = value
    g.pixels.push_back(id)
    g.reducedBy = 0
    return g
@cython.boundscheck(False)
@cython.wraparound(False)

cdef inline bint isMinima(vector[group]& groups, int current) nogil:

    cdef set[int].iterator it = groups[current].adjacent.begin()
    while it != groups[current].adjacent.end():
        if(groups[deref(it)].value<groups[current].value):
            return False
        inc(it)
    return True
@cython.boundscheck(False)
@cython.wraparound(False)

cdef inline vector[int] getMinAround(vector[group]& groups, int current) nogil:
    cdef int min = 300
    cdef vector[int] mins
    cdef set[int].iterator it = groups[current].adjacent.begin()
    while it != groups[current].adjacent.end():
        if(groups[deref(it)].value<min):
            min = groups[deref(it)].value
        inc(it)
    it = groups[current].adjacent.begin()
    while it != groups[current].adjacent.end():
        if(groups[deref(it)].value==min):
            min = groups[deref(it)].value
            mins.push_back(deref(it))
        inc(it)
    return mins

@cython.boundscheck(False)
@cython.wraparound(False)

cdef inline void merge(int A, int B,vector[group]& groups) nogil:
    cdef vector[int].iterator it = groups[B].pixels.begin()
    while it != groups[B].pixels.end():
        groups[A].pixels.push_back(deref(it))
        inc(it)

    groups[A].reducedBy = max(groups[A].reducedBy ,groups[B].reducedBy )

    for i in groups[B].adjacent:
        groups[i].adjacent.erase(B)
        groups[i].adjacent.insert(A)
        groups[A].adjacent.insert(i)

    groups[A].adjacent.erase(A)
    groups[B].id = 0

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void imExtendedMinC(int[:,:]& myArray,int[:,:]& clusterMap, int minx,int miny, int maxx, int maxy,int h) nogil:
    cdef int i,j
    cdef int id = 1
    cdef int xDelta,yDelta,x,y
    cdef int zero = 0
    cdef bint found = False
    cdef int foundIndex = 0
    cdef vector[group] groups
    groups.push_back(constructor(0,0))
    cdef vector[int] adj
    cdef int tmp

    cdef set[int].iterator it
    for i in range(minx,maxx):
        for j in range(miny,maxy):
            if (clusterMap[i][j] == 0):
                found = False

                for xDelta in range( -1,1):
                    for yDelta in range( -1, 0-2*xDelta):
                        x = xDelta+i
                        y = yDelta+j
                        if (x >= minx and x < maxx and y >= miny and y < maxy):
                            if(myArray[x][y]==myArray[i][j]):
                                foundIndex = clusterMap[x][y]
                                found = True
                                break
                            else:
                                adj.push_back(clusterMap[x][y])
                    if found:
                        break

                if(found is False):
                    foundIndex = id
                    groups.push_back(constructor(id,myArray[i][j]))
                    id = id + 1

                clusterMap[i][j]= foundIndex

                while not adj.empty():
                    tmp = adj.back()
                    adj.pop_back()
                    it = (groups[foundIndex]).adjacent.find(tmp)
                    if  it == groups[foundIndex].adjacent.end():
                        groups[foundIndex].adjacent.insert(tmp)
                        groups[tmp].adjacent.insert(foundIndex)


    cdef vector[int] minimas
    cdef vector[group].iterator groupIt = groups.begin()
    inc(groupIt)
    while groupIt != groups.end():

        if isMinima(groups,deref(groupIt).id) :
            minimas.push_back(deref(groupIt).id)
        inc(groupIt)


    cdef vector[int] done
    cdef vector[int] mins
    cdef vector[int].iterator vecIt
    cdef int move
    cdef int hInt = h
    cdef int current

    while minimas.size()!=0:
        current = minimas.back()
        minimas.pop_back()
        if groups[current].id!=0:
            mins = getMinAround(groups,current)
            if(mins.size()!= 0 ):
                if(groups[current].value+hInt-groups[current].reducedBy < groups[mins[0]].value):

                    groups[current].value = groups[current].value+hInt - groups[current].reducedBy
                    groups[current].reducedBy = hInt
                    done.push_back(current)
                else:
                    move = groups[mins[0]].value-groups[current].value
                    groups[current].reducedBy += move
                    groups[current].value += move
                    vecIt = mins.begin()
                    while vecIt != mins.end():
                        merge(current,deref(vecIt),groups)
                        inc(vecIt)

                    if(isMinima(groups,current)):
                        if(groups[current].reducedBy==hInt):
                            done.push_back(current)
                        else:
                            minimas.push_back(current)
            else:
                groups[current].value = groups[current].value + hInt
                done.push_back(current)



    cdef set[int] minimaFinals
    cdef vector[int].iterator vecItB

    vecIt = done.begin()
    while vecIt != done.end():
        vecItB = groups[deref(vecIt)].pixels.begin()
        while vecItB != groups[deref(vecIt)].pixels.end():
            minimaFinals.insert(deref(vecItB))
            inc(vecItB)
        inc(vecIt)

    for i in range(minx,maxx):
        for j in range(miny,maxy):
            it = minimaFinals.find(clusterMap[i][j])
            if it != minimaFinals.end():
                clusterMap[i][j]=255
            else:
                clusterMap[i][j]=0

def imExtendedMin(image,hDepth, nbThreads= 4 ):
    cdef int[:, :] clusterMap = np.zeros(image.shape, np.int32)
    cdef int [:,:] imageC = image.astype(np.int32)
    cdef int h = hDepth


    t = time.time()
    cdef int it
    cdef int max = nbThreads

    with nogil, parallel():
        for it in prange(0,max):
            imExtendedMinC(imageC,clusterMap,imageC.shape[0]/max*it,0,imageC.shape[0]/max*(it+1),imageC.shape[1],h)
    print(time.time()-t)
    return np.array(clusterMap)


def test():
    filename = os.path.join('../test/Source/', 'bigTest.jpg')
    moon = io.imread(filename)
    moon = color.rgb2gray(moon)
    for i in range(0, moon.shape[0]):
        for j in range(0, moon.shape[1]):
            moon[i, j] = int(moon[i, j] * 255)
    t = time.time()
    a = imExtendedMin(moon,30)
    print("Test Extended Minima Executed",time.time()-t)
#    ret = imExtendedMin(moon,20)
    io.imsave('../test/TestMinima.png', a)
	






