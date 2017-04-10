INF49x0-Projet_4-NeuroPoly

NeuroPoly


# WARNING

## Only working with python 3.5



For windows users : 

	Install miniconda

		https://repo.continuum.io/miniconda/Miniconda-3.5.5-Windows-x86_64.exe


	conda install --yes --file requirements.txt


For Mac and Linux :


	Upgrade pip

		python3 -m pip install --upgrade pip


	Install dependancies

		python3 -m pip install -r requirements.txt





For manually editing the congiruation, you may want to create your own JSON, use axonsegpy/user/input/test.json as an example.

The main.py takes a single argument, and its the path to the json. If no argument is provided, it will look for a "test.json" in the same folder.

Example usage : python3 main.py -c ~/axonseg/myConfig.json
