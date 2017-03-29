import sys
import argparse

# Temporary (to remove !!!) ##TODO
from core import ConfigParser

def main():
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # TODO : replace with config file

    # Parse args
    args = parser.parse_args()
    config = args.config

    if config == "" or config == None:
        config = "./test.json" # Test configuration

    # We initialise the algo runner with an aldo
    ConfigParser.parse(config)

if __name__ == "__main__":
    main()
