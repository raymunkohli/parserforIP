import sys, getopt,json,os
import xml.etree.ElementTree as ET
#https://docs.python.org/3/library/xml.etree.elementtree.html
from optparse import *
ESLI = "{http://www.w3.org/2001/XMLSchema-instance}"

def main():
    # match arguments to variables
    args = parser()
    xmlfile = args[0]
    outputdirectory = args[1]
    if not os.path.exists(outputdirectory+"/machines/"):
        os.mkdir(outputdirectory+"/machines/")
    if not os.path.exists(outputdirectory+"/network/"):
        os.mkdir(outputdirectory + "/network/")
    deconstruct_tree(ET.parse(xmlfile),outputdirectory)


def deconstruct_tree(tree, outputdirectory):
    machines = []
    networks = []

    for child in tree.getroot():
        if child.tag == "machine":
            if child.get(ESLI+"type") == "cw:Link":
                a = 1 + 1
            else:
                machines.append(process_machine(child, outputdirectory, machines))
        elif child.tag == "network":
            net = process_networks(child, outputdirectory)
            a = 1+1


def process_networks(network, outputdirectory):
    machine = []
    for child in network:
        if child.tag == "machine":
            machine.append(process_machine(child,outputdirectory))
        if child.tag == "network":
            process_networks(child,outputdirectory)

    return network, machine


def process_machine(machine, outputdirectory, machines):
    states = []
    transitions = {}
    properties = {}
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
                    toid: [
                        {
                            "type": "deterministic",
                            "parameter": child.get("parameter")
                        }
                    ]
                }

            if fromid in transitions:
                a = transitions[fromid]
                transitions[fromid].append(transition)
            else:
                transitions[fromid] = []
                transitions[fromid].append(transition)
        if child.tag =="property":
            prop = {
                "type" : child.get("type"),
                "required": True,
            }
            properties[child.get("name")] = prop
    data = {
        "name": machine.get("name"),
        "type": machine.get("type"),
        "properties": properties,
        "structure": {
            "states": states,
            "initial": states[int(initial)],
            "transitions": transitions
        }
    }
    file = open(outputdirectory+"/machines/"+machine.get("name")+".json", 'w+')
    file.write(str(json.dumps(data)))


def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args


if __name__ == "__main__":
   main()
