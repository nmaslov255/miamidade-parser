#!/usr/bin/python3
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(
    description='Contracts parser from miamidade.gov')

parser.add_argument('csv', type=str,
    help='route to csv file with folios numbers')
parser.add_argument('out', type=str,
    help='filename for save results (in xlsx)')
parser.add_argument('-wso', '--with-second-owner', action='store_true', 
    help='makes columns "seller 2" and "buyer 2" in Excel table')
parser.add_argument('-my', '--min-year',  type=int,
    help='filter for old contracts')

args = parser.parse_args()

if args.min_year:
    args.min_year = datetime(args.min_year, 1, 1)

# alias for "with_second_owner"
if args.with_second_owner:
    args.wso = True 
else:
    args.wso = False
