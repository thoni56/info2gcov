#! /usr/bin/env python3

# Convert an lcov info-file to separate .gcov-files for all sources.
# The output is written to the full path of the files named in the
# info-file.
#
# Usage:
#
#    info2gcov [-q] <info-file>
#
# Rationale:
#
# If you run tests and collect the coverage data in different sets (as
# is necessary if you want to run your testcases in parallel) then neither
# gcov nor gcovr can aggregate them. `lcov` does have "-a" to add info-files
# into a new one.
#
# As I wanted to use cov-mode in emacs and that only can handle gcov formatted
# data, I needed a way to extract the necessary bits from the aggregated
# info-file. Turns out that the parser of gcov-files in cov-mode only looks for
# basic "<frequency>:<line>:" so that could easily be replicated. Also the
# aggregated info-file is nothing more than all info-files concatenated so
# collation of executions had to be done.
#
# Algorithm:
#
# Read the info-file from beginning to end. Lines starting with "SF:" indicates
# start of source file data. There are more "fields" available (function/branch)
# but we only need "DA:" which has the format "<line>:<frequency>". Obviously, if
# a file occurs multiple times the <frequency>'s has to be accumulated.


import argparse


def collate(info_content):
    coverage = {}
    for info_line in info_content:
        if info_line.startswith("SF:"):
            # Source Filename
            filename = info_line.split(":")[1].rstrip("\n")
            try:
                coverage[filename]
            except KeyError:
                coverage[filename] = {}
        if info_line.startswith("DA:"):
            # DAta
            [line, executions] = info_line.split(":")[1].split(",")
            add_execution_data_for_line(
                coverage[filename], (int(line), int(executions)))
    return coverage


def add_execution_data_for_line(data, line_data):
    (line, executions) = line_data
    try:
        data[line] = executions + data[line]
    except KeyError:
        data[line] = executions


if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Read an info file from lcov and convert it to aggregated single files or all source files in it')
    argparser.add_argument(
        'inputfile', help='name of the info file from lcov')
    argparser.add_argument(
        '-q', '--quiet', help='be quiet', action='store_true')

    args = argparser.parse_args()

    with open(args.inputfile) as f:
        coverage = collate(f.readlines())
    for filename in coverage.keys():
        if not args.quiet:
            print(filename)
        with open(filename+".gcov", "w") as gcov_file:
            for line in coverage[filename].keys():
                gcov_file.write("{}:{}:\n".format(
                    coverage[filename][line], line))
