#!/usr/bin/env python3

import argparse
import pathlib
import pickle


from chemfiles import Frame, Atom, UnitCell, Trajectory, Selection


def load_data(file):
    with file.open("rb") as f:
        data = pickle.load(f)
    
    glass_structure = Frame()
    # glass_structure.cell = UnitCell(data['box'])
    
    for i in range(4096):
        if any(data['positions'][i] > data['box'] / 2):
            continue

        if data['types'][i] == 0:
            glass_structure.add_atom(Atom("Ni"), data['positions'][i])
        elif data['types'][i] == 1:
            glass_structure.add_atom(Atom("P"), data['positions'][i])

    AA = "two: name(#1) == Ni and name(#2) == Ni and " \
        "distance(#1, #2) > 0.03 and distance(#1, #2) < (0.6 * 2.5 * 1)"
    
    AB = "two: name(#1) == Ni and name(#2) == P and " \
        "distance(#1, #2) > 0.03 and distance(#1, #2) < (0.6 * 2.5 * 0.8)"

    BB = "two: name(#1) == P and name(#2) == P and " \
        "distance(#1, #2) > 0.03 and distance(#1, #2) < (0.6 * 2.5 * 0.88)"

    selection = Selection(AA)
    to_bond = selection.evaluate(glass_structure)
    for pair in to_bond:
        (i, j) = pair
        glass_structure.add_bond(i, j)

    selection = Selection(AB)
    to_bond = selection.evaluate(glass_structure)
    for pair in to_bond:
        (i, j) = pair
        glass_structure.add_bond(i, j)

    selection = Selection(BB)
    to_bond = selection.evaluate(glass_structure)
    for pair in to_bond:
        (i, j) = pair
        glass_structure.add_bond(i, j)

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