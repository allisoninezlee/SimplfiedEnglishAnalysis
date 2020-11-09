import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True, help='path to file to parse and add to database.')
    args = parser.parse_args()
    
    file_path = args.file
    print("Processing file: " + args.file)