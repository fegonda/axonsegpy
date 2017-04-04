INF49x0-Projet_4-NeuroPoly
NeuroPoly

For windows and linux : 

1- Clone this repo with "git clone https://github.com/neuropoly/axonsegpy"
2- Download and install Anaconda3 at (https://www.continuum.io/downloads)
3- Launch GUI.py with the anaconda python3.


FOR MAC USERS : 

There is a problem with some of the cython library, and you will need to recompile / bootstrap GCC.
Here are the steps :

1- Install brew (http://brew.sh/)
2- In the terminal, enter : "brew install gcc --without-multilib" (grab a coffee, this takes quite a while - but needed because default brew installation of gcc doesn't have OpenMP support)
3- "export CXX=/usr/local/Cellar/gcc/6.1.0/bin/g++-6" (use the path from the output of brew gcc install. at the time of writing the above is correct, but may change. Do this or otherwise osx still uses clang to compile)
3- "brew install eigen"
4- "brew install anaconda3"
5- Run the main.py with the anaconda3 python interpeter.

NB : The GUI dosent work YET on Mac. Work in progess.


For manually editing the congiruation, you may want to create your own JSON, use axonsegpy/user/input/test.json as an example.
The main.py takes a single argument, and its the path to the json. If no argument is provided, it will look for a "test.json" in the same folder.
Example usage : python3 main.py -c ~/axonseg/myConfig.json
