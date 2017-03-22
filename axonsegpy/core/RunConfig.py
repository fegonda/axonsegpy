import importlib

# TODO -- Try catch ?
def runAlgo(name, variables):
	try:
		module = importlib.import_module(name)
		module.run(variables)

	except Exception as e:
		print(str(e))
		print("Error in module '" + name + "' found !")