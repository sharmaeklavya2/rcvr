#!/usr/bin/env python

from __future__ import print_function

import os
from os.path import dirname, abspath
import sys

BASE_DIR = dirname(dirname(abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from six import text_type
from typing import Any, List, Tuple
from lib.str_utils import force_text

import argparse
import csv

loc_types = ["states", "districts", "subdistricts"]

parser = argparse.ArgumentParser(description="Load location data into database from .csv or .tsv files")
for loc_type in loc_types:
    parser.add_argument("--" + loc_type, help="Path to .csv or .tsv file containing " + loc_type)
args = parser.parse_args()

def get_csv_reader(fpath):
    # type: (str) -> Any

    ext = os.path.splitext(fpath)[1]
    if ext not in ['.csv', '.tsv']:
        raise TypeError("File extension should be '.csv' or '.tsv'. Found {} instead".format(repr(ext)))

    fobj = open(fpath)
    if ext == '.csv':
        return csv.reader(fobj, delimiter=',', quotechar='"')
    else:
        return csv.reader(fobj, delimiter='\t', quotechar='"')

def get_state_dicts(fpath):
    # type: (str) -> List[Dict[str, Any]]
    csv_reader = get_csv_reader(fpath)
    data = [] # type: List[Dict[str, Any]]
    for row in csv_reader:
        if len(row) == 2:
            scode, name = [force_text(x) for x in row]
            data.append({"scode": scode.upper(), "name": name})
        else:
            raise ValueError("Invalid CSV format")
    return data

def get_district_dicts(fpath):
    # type: (str) -> List[Dict[str, Any]]
    csv_reader = get_csv_reader(fpath)
    data = [] # type: List[Dict[str, Any]]
    for raw_row in csv_reader:
        row = [force_text(x) for x in raw_row]
        if len(row) == 2 or len(row) == 3:
            item = {
                "pin": int(row[0]),
                "state_id": row[1].upper(),
                "name": row[2] if len(row) == 3 else u'',
            }
            data.append(item)
        else:
            raise ValueError("Invalid CSV format")
    return data

def get_subdistrict_dicts(fpath):
    # type: (str) -> List[Dict[str, Any]]
    csv_reader = get_csv_reader(fpath)
    data = [] # type: List[Dict[str, Any]]
    for row in csv_reader:
        if len(row) == 1 or len(row) == 2:
            pincode = int(row[0])
            item = {
                "pincode": pincode,
                "name": force_text(row[1]) if len(row) == 2 else u'',
                "pin": pincode % 1000,
                "district_id": pincode // 1000,
            }
            data.append(item)
        else:
            raise ValueError("Invalid CSV format")
    return data


if "DJANGO_SETTINGS_MODULE" not in os.environ:
    # Set up django
    print("Setting up Django")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_conf.settings")
    import django
    django.setup()

from django.db.utils import IntegrityError
from main.models import State, District, SubDistrict

fail_message = "bulk_create on {} failed. Falling back to individual saves."
pass_message = "bulk_create on {} succeeded."

if args.states is not None:
    state_dicts = get_state_dicts(args.states)
    states = [State(**d) for d in state_dicts]
    try:
        State.objects.bulk_create(states)
        print(pass_message.format('State'))
    except IntegrityError:
        print(fail_message.format('State'))
        for state in states:
            state.save()

if args.districts is not None:
    district_dicts = get_district_dicts(args.districts)
    districts = [District(**d) for d in district_dicts]
    try:
        District.objects.bulk_create(districts)
        print(pass_message.format('District'))
    except IntegrityError:
        print(fail_message.format('District'))
        for district in districts:
            district.save()

if args.subdistricts is not None:
    subdistrict_dicts = get_subdistrict_dicts(args.subdistricts)
    subdistricts = [SubDistrict(**d) for d in subdistrict_dicts]
    try:
        SubDistrict.objects.bulk_create(subdistricts)
        print(pass_message.format('SubDistrict'))
    except IntegrityError:
        print(fail_message.format('SubDistrict'))
        for subdistrict in subdistricts:
            subdistrict.save()
