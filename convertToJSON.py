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
        if child.get("type") == "state-machine":
            if child.get(ESLI+"type") == "cw:Link":
                a = 1 + 1
            else:
                i = 0
                for x in machines:
                    if child.get("name") == machines[i]:
                        i = i + 1
                print("machine :" + child.get("name"))
                machines.append(process_machine(child, outputdirectory, i))
        elif child.get("type") == "network-machine":
            print("network M :")
            process_networks(child, outputdirectory, machines, networks)
        elif child.tag == "network":
            print("network N :")
            process_networks(child, outputdirectory, machines, networks)
        else:
            sys.exit("unsupported type on:" + child.tag)


def process_networks(network, outputdirectory, machines, networks):
    networks.append(network)
    localmachine = []
    for child in network:
        if child.get("type") == "state-machine":
            i = 0
            for x in machines:
                if child.get("name") == machines[i]:
                    i = i + 1
            machines.append(process_machine(child, outputdirectory, i))
            #localmachine.append()
        if child.get("type") == "network-machine":
            i = 0
            for x in networks:
                if child.get("name") == networks[i]:
                    i = i + 1
            machines.append(process_represents(child, outputdirectory, i, machines))
    return 123

def process_represents(machine, outputdirectory, suffix, machines):
    suffix = str(suffix)
    property = {}
    for child in machine:
        if child.tag == "state" or child.tag == "transition":
            sys.exit("Error, network-machine must have no states at" + machine.get("name"))
        else:
            prop = {
                "type": child.get("type"),
                "required": True,
            }
            property[child.get("name")] = prop

    data = {
        "name": machine.get("name"),
        "type": "network-machine",
        "properties": property
    }
    file = open(outputdirectory+"/machines/"+machine.get("name")+"_"+suffix+".json", 'w+')
    file.write(str(json.dumps(data)))


def process_machine(machine, outputdirectory, suffix):
    suffix = str(suffix)
    states = []
    transitions = {}
    properties = {}
    # get states
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
                    toid: [{
                            "type" : "probabilistic",
                            "distribution": child.get("distribution"),
                            "parameter": child.get("parameter")
                            }]}
            else:
                transition = {
                    toid: [{
                            "type": "deterministic",
                            "parameter": child.get("parameter")
                        }]}
            if fromid in transitions:
                a = transitions[fromid]
                transitions[fromid].append(transition)
            else:
                transitions[fromid] = []
                transitions[fromid].append(transition)
        if child.tag == "property":
            prop = {
                "type": child.get("type"),
                "required": True,
            }
            properties[child.get("name")] = prop
    data = {
        "name": machine.get("name")+"_"+suffix,
        "type": "state-machine",
        "properties": properties,
        "structure": {
            "states": states,
            "initial": int(machine.get("initial").split(".")[-1]),
            "transitions": transitions
        }
    }
    file = open(outputdirectory+"/machines/"+machine.get("name")+"_"+suffix+".json", 'w+')
    file.write(str(json.dumps(data)))


def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args


if __name__ == "__main__":
   main()
