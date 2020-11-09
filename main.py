import argparse
import os
from os import path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True, help='path to file to parse and add to database.')
    args = parser.parse_args()
    
    file_path = args.file

    # check for valid path
    if not path.exists(file_path):
        print("File " + file_path + " does not exist. Exiting...")
        exit()
    
    print("Processing file: " + args.file)