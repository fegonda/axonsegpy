import sys
import argparse

# Temporary (to remove !!!) ##TODO
sys.path.insert(1, './algo')
sys.path.insert(1, './core')
sys.path.insert(1, './lib')

import ConfigParser

def main():
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # TODO : replace with config file

    # Parse args
    args = parser.parse_args()
    config = args.config

    if config == "" or config == None:
        config = "../user/input/test.json" # Test configuration

    # We initialise the algo runner with an aldo
    ConfigParser.parse(config)

if __name__ == "__main__":
    main()
