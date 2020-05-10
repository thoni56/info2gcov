#! /usr/bin/env python3

import argparse


def collate(info_content, filename):
    data = {}
    collecting = False
    for info_line in info_content:
        if not collecting:
            if info_line.startswith("SF:") and info_line.endswith("/"+filename):
                collecting = True
        else:
            if info_line.startswith("DA:"):
                [line, executions] = info_line.split(":")[1].split(",")
                add_execution_data_for_line(data, (int(line), int(executions)))
            else:
                if info_line.startswith("SF:"):
                    collecting = False
    return data


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

    args = argparser.parse_args()

    with open(args.inputfile) as f:
        collate(f.readlines())
