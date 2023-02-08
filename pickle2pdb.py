#!/usr/bin/env python3

import argparse
import pathlib
import pickle


from chemfiles import Topology, Frame, Atom, UnitCell, Trajectory


def load_data(file):
    with file.open("rb") as f:
        data = pickle.load(f)
    
    glass_structure = Frame()
    glass_structure.cell = UnitCell(data['box'] / 3)
    for i in range(4096):
        if any(data['positions'][i] > data['box'] / 3):
            continue

        if data['types'][i] == 0:
            glass_structure.add_atom(Atom("Si"), data['positions'][i])
        elif data['types'][i] == 1:
            glass_structure.add_atom(Atom("O"), data['positions'][i])
    glass_structure.guess_bonds()

    return glass_structure


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "data_path",
        type = pathlib.Path,
    )

    args = parser.parse_args()

    in_files = sorted(args.data_path.glob("**/*.pickle"))
    for in_file in in_files:
        data = load_data(in_file)
        index = in_file.parts.index('pickle') + 1
        out_file = pathlib.Path('data/pdb').joinpath(*in_file.parts[index:]).with_suffix(".pdb")
        pathlib.Path(out_file.parent).mkdir(parents=True, exist_ok=True)
        with Trajectory(str(out_file), "w") as trajectory:
            trajectory.write(data)

 
if __name__ == "__main__":
    main()