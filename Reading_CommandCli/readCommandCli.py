#This Script reads command from the Cli using argparse, sys library

#The expected commands are "ProjectStake" and "Training" else throws an error

import argparse, sys


argpaser= argparse.ArgumentParser(description="content tracker")
argsubparser= argpaser.add_subparsers(title="Commands", dest="command")
argsubparser.required=True
parser_name = argsubparser.add_parser("ProjectStake", help="Description of the 'name' command.")
parser_name = argsubparser.add_parser("Training", help="Description of the 'name' command.")



def main(argv=sys.argv[1:]):
    args= argpaser.parse_args(argv)
    match args.command:
       case "ProjectStake": print("I love projectstake")
       case "Training":print("this is WYAG course") 