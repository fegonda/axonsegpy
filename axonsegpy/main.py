
import sys, os

### OS WINDOWS MAGIC ###
if sys.platform == "win32" and sys.version_info < (3, 0): # We are running python 2 on windows
    import datetime
    year = datetime.date.today().year
    stop = False
    for y in range(2000, year + 1 ):
        y = str(y)[-2:]
        try:
            print("Detecting visual studio [" + "%VS"+y+"0" + "] installation in : " + os.environ["VS"+y+"0COMNTOOLS"])
            os.environ["VS90COMNTOOLS"] = "%VS"+y+"0COMNTOOLS%"
            stop = True
        except:
            pass
        if stop:
            break
    if not stop:
        print("Will use binary files instead of cython") # If we dont find them, we wont use cython then.
    # Actually, we are detecting the OS and python version, if its windows and python2
    # We must add to the current path the link to the build tools.
    # Since we dont know wich one we have, we go through every possible path
    # (aka current year - 2000) and we check if it exists.
    # If it does, we add it then we stop searching.
### END OF OS MAGIC ###

import argparse
from core import ConfigParser

def IntegrityTest():
    import json, os
    from skimage import io
    import numpy as np

    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def dice(path1, path2):
        # https://gist.github.com/JDWarner/6730747
        im1 = io.imread(path1, as_grey=True)
        im2 = io.imread(path2, as_grey=True)

        im1 = np.asarray(im1).astype(np.bool)
        im2 = np.asarray(im2).astype(np.bool)

        if im1.shape != im2.shape:
            raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

        # Compute Dice coefficient
        intersection = np.logical_and(im1, im2)

        return 2. * intersection.sum() / (im1.sum() + im2.sum())


    j_name = "__IntegrityTest__.json"
    j_file = """{
   "preprocessing":[
      {
         "name":"AxonSeg",
         "params":{
            "input":".../config/input/20160830_CARS_Begin_07.tif",
            "output":"Simulation_img.csv",
            "outputImage":"Simulation_img.png",

            "minSize":10,
            "maxSize":1500,
            "Solidity":0.5,
            "MinorMajorRatio":0.25
         }
      }
   ],
   "axonSegmentation":[
   ],
   "axonPostProcessing":[
      {
         "name":"MyelinSeg",
         "params":{
            "input":"../config/input/20160830_CARS_Begin_07.tif",
            "outputImage":"Simulation_img.melyn.png",
            "outputList":"Simulation_img.melyn.csv",

            "minSize":10,
            "maxSize":1500,
            "Solidity":0.5,
            "MinorMajorRatio":0.25
         }
      }
   ]
}"""
    with open(j_name, 'w') as f:
        f.write(j_file)

    blockPrint()
    failure = False
    try:
        ConfigParser.parse(j_name)
    except:
        failure = True
    enablePrint()
    if failure:
        print("Error running tests, crash detected !")

    if (not os.path.isfile("Simulation_img.csv")) or (not os.path.isfile("Simulation_img.png")) :
        failure = True
        print("Error, failed the segmentation phase !")
    if (not os.path.isfile("Simulation_img.melyn.csv")) or (not os.path.isfile("Simulation_img.melyn.png")) :
        failure = True
        print("Error, failed the melyn phase !")

    if failure:
        try:
            os.remove(j_name)
            os.remove("Simulation_img.csv")
            os.remove("Simulation_img.png")
            os.remove("Simulation_img.melyn.png")
            os.remove("Simulation_img.melyn.csv")
        except:
            pass
        exit(-1)

    axon = open("Simulation_img.csv").readlines()
    axon = list(filter(None, axon))

    melyn = open("Simulation_img.melyn.csv").readlines()
    melyn = list(filter(None, melyn))

    EXPECTED_AXON = 200
    axonFound = len(axon)
    print("Found %i/%i axon with current algorithmes. This is a %f%% difference !" % ( axonFound, EXPECTED_AXON, (EXPECTED_AXON - axonFound)/EXPECTED_AXON*100))

    dicing = dice("../tests/SegTest/Simulation_img.tif", "Simulation_img.melyn.png")
    print("And Mask is %f%% similar to original image." % (dicing * 100.0))

    os.remove(j_name)
    os.remove("Simulation_img.csv")
    os.remove("Simulation_img.png")
    #os.remove("Simulation_img.melyn.png")
    os.remove("Simulation_img.melyn.csv")



def main():
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config') 
    parser.add_argument('-t', '--test', action='store_true')

    # Parse args
    args = parser.parse_args()
    config = args.config
    test  = args.test

    if test == True:
        IntegrityTest()
    else :
        if config == "" or config == None:
            config = os.getcwd() + "/config.json" # Local configuration

        # We initialise the algo runner with an aldo
        ConfigParser.parse(config)

if __name__ == "__main__":
    main()
