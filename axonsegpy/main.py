import datetime
import sys
import argparse
from algoRunner import algoRunner

# TODO : replace with ref to actual algos
from algoRunner import extentedMinima
from algoRunner import axonDeepSeg


def main():
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    parser.add_argument('-a', '--algorithm')  # TODO : replace with config file

    # Parse args
    args = parser.parse_args()
    imagePath = args.source
    algorithm = args.algorithm

    if imagePath == "":
        print("Invalid path")
        sys.exit(2)

    # We initialise the algo runner with an aldo
    if algorithm == "minima":
        algo = algoRunner(extentedMinima())
    elif algorithm == "axonDeepSeg":
        algo = algoRunner(axonDeepSeg())

    # Run algorithm
    algo.execute(imagePath)

    # We can change algo at runtime
    algo.changeAlgorithm(axonDeepSeg())

    # Run algorithm
    algo.execute(imagePath)


if __name__ == "__main__":
    main()
