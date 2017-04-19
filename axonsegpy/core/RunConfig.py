from algo import *
from core import *
from sys import modules

def runAlgo(name, variables):
#	try:
		modules["algo."+name].run(variables)

#	except Exception as e:
#		print(str(e))
#		print("Error in module '" + name + "' found !")
