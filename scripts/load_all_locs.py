#!/usr/bin/env python

import os
from os.path import dirname, abspath

import argparse
import subprocess

BASE_DIR = dirname(dirname(abspath(__file__)))
LOADER_PATH = os.path.join(BASE_DIR, "scripts", "load_locations.py")

parser = argparse.ArgumentParser(description="Load all location data from csv files")
parser.add_argument("dirpath", help="Path to directory containing location data")
args = parser.parse_args()

loc_types = ["states", "districts", "subdistricts"]
subargs = []
for loc_type in loc_types:
    subargs.append("--" + loc_type)
    subargs.append(os.path.join(args.dirpath, loc_type + ".csv"))

subprocess.check_call(["python", LOADER_PATH] + subargs)
