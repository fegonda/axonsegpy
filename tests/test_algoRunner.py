import sys
sys.path.insert(1, '../axonsegpy')

from algoRunner import runAlgo  

# TODO : replace with ref to actual algos
from algoRunner import extentedMinima
from algoRunner import axonDeepSeg  

# Add axonsegpy brother folder to path


# TODO : add des assers @moncef

def test(imagePath = ".", algorithm = "minima"):

    if imagePath == "":
        print("Invalid path")
        assert(False)

    # We initialise the algo runner with an aldo
    if algorithm == "minima":
        algo =  runAlgo(extentedMinima())
    elif algorithm == "axonDeepSeg":
        algo = runAlgo(axonDeepSeg())
    else:
        # No algo was passed
        assert(False)
    # Run algorithm
    algo.execute(imagePath)

    # We can change algo at runtime
    algo.changeAlgorithm(axonDeepSeg())

    # Run algorithm
    algo.execute(imagePath)
