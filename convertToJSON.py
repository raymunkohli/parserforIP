import sys, getopt,json
import xml.etree.ElementTree as ET
#https://docs.python.org/3/library/xml.etree.elementtree.html
from optparse import *
ESLI = "{http://www.w3.org/2001/XMLSchema-instance}"

def main():
    # match arguments to variables
    args = parser()
    xmlfile = args[0]
    outputdirectory = args[1]
    deconstruct_tree(ET.parse(xmlfile))


def deconstruct_tree(tree):
    for child in tree.getroot():
        if child.tag == "machine":
            if child.get(ESLI+"type") == "cw:Link":
                a = 1+ 1
            else:
                processMachine(child)
        elif child.tag == "network":
            a = 1+1


def processMachine(machine):
    states = []
    transitions = {}
    # get states
    initial = machine.get("initial").split(".")[-1]
    #  get initial state
    for child in machine:
        #check if child is a state
        if child.tag == "state":
            states.append(child.get("name"))
        # check if child is a transition
        if child.tag == "transition":
            fromid = states[int(child.get("from").split(".")[-1])]
            toid = states[int((child.get("to").split(".")[-1]))]
            #check if transition is probabilistic  or not
            if child.get(ESLI+"type") == "cw:probabilistic":
                transition = {
                    toid: [
                        {
                            "type" : "probabilistic",
                            "distribution": child.get("distribution"),
                            "parameter": child.get("parameter")
                            }
                        ]
                    }
            else:
                transition = {
                    states[toid]: [
                        {
                            "type": "deterministic",
                            "parameter": child.get("parameter")
                        }
                    ]
                }

            if fromid in transitions:
                transitions[fromid] = transitions[fromid] + transition
                print("old")
            else:
                print("new")
                transitions[fromid] = transition


    # get initial state
    data = {
        "name": machine.get("name"),
        "type": machine.get("type"),
        "structure": {
            "states": states,
            "initial": states[int(initial)],
            "transitions": transitions
        }
    }
    print(json.dumps(data))



def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args


if __name__ == "__main__":
   main()
