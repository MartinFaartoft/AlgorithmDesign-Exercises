import filecmp, sys
from os import listdir
from os.path import join, splitext,basename
from rdam_stable_marriage import GSsolve


def compare_files(file_1, file_2):
    if filecmp.cmp(file_1, file_2, shallow=False):
        print "Correct! " + file_1 + " and " + file_2 + " are the same"
    else:
        print "WRONG! " + file_1 + " and " + file_2 + " are NOT the same"


def get_data_files(path):
    input = []
    output = []
    data_files = listdir(path)
    for file in data_files:
        if file.endswith(".out"):
            output.append(join(path, file))
        elif file.endswith(".in"):
            input.append(join(path, file))
    return input, output


data_path = "data"
our_out_prefixes = "Group7_"

in_files, out_files = get_data_files(data_path)
our_out_files = []

# Runs our algorithm on each .in file
for in_file in in_files:
    out_file = basename(in_file)  # Get the filename
    out_file = splitext(out_file)[0]  # Remove the extension and add extension
    out_file = our_out_prefixes + out_file + ".out"
    out_file = join(data_path, out_file)
    our_out_files.append(out_file)
    GSsolve(in_file, out_file)


# Compares each of our .out-files with the given out-files
pairs = zip(our_out_files, out_files)
for (our_out_file, given_out_file) in pairs:
    compare_files(our_out_file, given_out_file)