# Algorithms should go in separate files and have the method 'algorithm'
class extentedMinima:
    def algorithm(self, imagePath):
        print('minima')  # dummy, to replace with actual results


class axonDeepSeg:
    def algorithm(self, imagePath):
        print('axonDeepSeg')  # dummy, to replace with actual results


class algoRunner:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, imagePath):
        return self.strategy.algorithm(imagePath)

    def changeAlgorithm(self, newAlgorithm):
        self.strategy = newAlgorithm
