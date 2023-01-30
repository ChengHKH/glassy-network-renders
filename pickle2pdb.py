#!/usr/bin/env python3

import argparse
import pathlib
import pickle

def load_data(file):
    with file.open("rb") as f:
        data = pickle.load(f)
        print(data)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "data_path",
        type = pathlib.Path,
    )

    args = parser.parse_args()

    in_files = sorted(args.data_path.glob("*.pickle"))
    for in_file in in_files:
        load_data(in_file)
    

if __name__ == "__main__":
    main()