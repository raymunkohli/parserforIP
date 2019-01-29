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
    deconstruct_tree(ET.parse(xmlfile), outputdirectory)

def calculate_suffix(name,array):
    i = 0
    count = 0
    for x in  array:
        if name+'_'+str(count) == array[i]:
            count +=1
        i += 1
    return count

def deconstruct_tree(tree, outputdirectory):
    machines = []
    networks = []
    notnestednetworks = []
    notnestedmachines = []
    file = open(outputdirectory + '/' + tree.getroot().get("name")+".json", 'w+')
    for child in tree.getroot():
        if child.get("type") == "state-machine":
            if child.get(ESLI+"type") == "cw:Link":
                a = 1 + 1
            else:
                u = process_machine(child, outputdirectory, calculate_suffix(child.get("name"),machines), machines, notnestednetworks, notnestedmachines)
                #instance the machine ** to do
        elif child.tag == "network":
            process_networks(child, outputdirectory, machines, networks,False, notnestednetworks, notnestedmachines)
        else:
            sys.exit("unsupported type on:" + child.tag)
    m = []
    for mach in machines:
        d = {
            "include": "machines/"+str(mach)
        }
        m.append(d)

    n = []
    for net in networks:
        d = {
            "include": "networks/"+str(net)
        }
        n.append(d)
    n.append({
        "name": "baseline",
        "machines": [{
            "name": "Substations"
        }]
    })
    print(notnestednetworks)
    thenetworks = []
    for nnest in notnestednetworks:
        d = {

        }
        n.append(d)
    info = {
        "description": "All_Networks",
        "machines": m,
        "networks": n
    }
    file.write(json.dumps(info))


def process_networks(network, outputdirectory, machines, networks, isnested, nnestednetworks, nnmachines):
    localmachine = []
    a = "null"
    for child in network:
        if child.get("type") == "state-machine":
            m = process_machine(child, outputdirectory, calculate_suffix(child.get("name"), machines), machines,nnestednetworks, nnmachines)
            a = m[2]
            if child.tag != 'represented':
                localmachine.append({
                    "name:": m[3],
                    "machine": m[2],
                    "properties": m[1]
                })

        if child.get("type") == "network-machine":
            a = process_netmachine(child, outputdirectory, calculate_suffix(child.get("name"), machines), machines)
            machines.append(a)
        elif child.tag == "network":
            process_networks(child, outputdirectory, machines, networks, True, nnestednetworks, nnmachines)
    if not isnested:
        nnestednetworks.append({
            "name": m[0].get("name"),
            "machine": m[2],
        })
    net = {
        "name": a,
        "machines": localmachine,
        "properties": m[1]
    }

    file = open(outputdirectory+"/network/"+a+".json", 'w+')
    networks.append("network/"+a+".json")
    file.write(str(json.dumps(net)))


def process_netmachine(machine, outputdirectory, suffix, machines):
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
        "name": machine.get("name")+'_'+suffix,
        "type": "network-machine",
        "properties": property
    }
    file = open(outputdirectory+"/machines/"+machine.get("name")+"_"+suffix+".json", 'w+')
    file.write(str(json.dumps(data)))
    return machine.get("name")+'_'+suffix


def process_machine(machine, outputdirectory, suffix, machines,nnestednetworks, nnmachines):
    suffix = str(suffix)
    states = []
    transitions = {}
    properties = {}
    init = {}
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
                    toid: {
                            "type": "probabilistic",
                            "distribution": child.get("distribution"),
                            "parameter": child.get("parameter")
                            }}
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
                "name": child.get("name"),
                "type": child.get("type"),
                "required": True,
            }
            init[child.get("name")] = child.get("value")
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
    names = {
        "name":machine.get("name"),
        "machine":machine.get("name")+"_"+suffix
    }
    file = open(outputdirectory+"/machines/"+machine.get("name")+"_"+suffix+".json", 'w+')
    file.write(str(json.dumps(data)))
    machines.append(machine.get("name")+"_"+suffix)
    return names, init, machine.get("name")+"_"+suffix, machine.get("name")


def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args


if __name__ == "__main__":
   main()
