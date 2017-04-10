INF49x0-Projet_4-NeuroPoly

NeuroPoly


# WARNING

## Only working with python 3.5


    * Install miniconda *

        Windows :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Windows-x86_64.exe

        Mac :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-MacOSX-x86_64.sh

        Linux :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh




For windows users : 

    Windows users MUST install miniconda (or anaconda), as scipy is broken and cannot work without the preloaded binaries from conda.

        conda install --yes --file requirements.txt


For Mac and Linux :

    We strongly advise to use miniconda (or anaconda) even for Mac and Linux, but it is not necessary. It will work with any installation of python 3.5, as long you have the correct packages installed :

    Upgrade pip

        python3 -m pip install --upgrade pip 


    Install dependancies

        python3 -m pip install -r requirements.txt 

If you are using a Mac, you might need some extra libraries :

    First install brew (https://brew.sh/)
    
         brew install gcc


For manually editing the congiruation, you may want to create your own JSON, use axonsegpy/user/input/test.json as an example.

The main.py takes a single argument, and its the path to the json. If no argument is provided, it will look for a "test.json" in the same folder.

Example usage : python3 main.py -c ~/axonseg/myConfig.json
