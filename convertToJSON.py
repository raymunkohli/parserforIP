import sys, getopt
from optparse import *

def main():
    #define the arguments
    xmlFile = ""
    outputDirectory = ""
    args = parser()
    xmlFile = args[0]
    outputDirectory = args[1]
    print(xmlFile, outputDirectory)

def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args


if __name__ == "__main__":
   main()