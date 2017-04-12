INF49x0-Projet_4-NeuroPoly

NeuroPoly


# WARNING

## Only working with python 3.5 and 3.6


    * Install miniconda *

        Windows :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Windows-x86_64.exe

        Mac :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-MacOSX-x86_64.sh

        Linux :

            https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh

If you decide to use anaconda (or miniconda), we suggest to install the libgcc package as well :

        conda install libgcc


For windows users (and *conda) : 

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


NB : If yo uwant to compile your own cython modules (isntead of using the precompiled ones), you will need to install visualstudio on windows, or gcc, on linux, and on mac, it is a bit more complicated since no support for openmp.

To install on mac, you will need : 

1- Install brew (http://brew.sh/)
2- In the terminal, enter : "brew install gcc --without-multilib" (grab a coffee, this takes quite a while - but needed because default brew installation of gcc doesn't have OpenMP support)
3- "export CXX=/usr/local/Cellar/gcc/6.1.0/bin/g++-6" (use the path from the output of brew gcc install. at the time of writing the above is correct, but may change. Do this or otherwise osx still uses clang to compile)
4- "export CC=/usr/local/Cellar/gcc/6.1.0/bin/gcc+-6" (samething again, use the good path)
5- "brew install eigen"
6- "brew install anaconda3"
7- Run the main.py with the anaconda3 python interpeter.



For manually editing the congiruation, you may want to create your own JSON, use axonsegpy/user/input/test.json as an example.

The main.py takes a single argument, and its the path to the json. If no argument is provided, it will look for a "test.json" in the same folder.

Example usage : python3 main.py -c ~/axonseg/myConfig.json

You can also use the integrity test mode, wich will run the program with a batch of pre set files and a hardcoded configuration file.
It will try to detect any crash or incomplete step, and also will output the number of axon found vs the known number.
And a dice compare between the original iamge and the binary mask we would apply on it.
