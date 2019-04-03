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
    model(ET.parse(xmlfile), outputdirectory)

def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args

def model(filet, folder):
    pass
    network = []
    network_instance = []
    group = []
    machine_instance = []
    machine_representation = []
    #create initial folder
    file = open(folder + '/' + filet.getroot().get("name")+".json", 'w+')

    for child in filet.getroot():
        if child.tag == "machine_instance":
            machine_instance.append(child)
            createMachineInstance(child)
        if child.tag == "machine_representation":
            print(json.dumps(createMachineRep(child)))
            machine_representation.append(child)
            createMachineRep(child)
        if child.tag == "network":
            network.append(child)
        if child.tag == "group":
            group.append(child)
        if child.tag == "network_instance":
            network_instance.append(child)
    fixLinks()


def fixLinks():
    pass

def createMachineInstance(machine):
    print("machine instance")


def createMachineRep(machine):
    print("machine rep")
    property_r_c = []
    transition_unlinked = []
    transition = {}
    state = []
    for child in machine:
        if child.tag == "property_r_c":
            property_r_c.append(calculate_r_c(child))
        if child.tag == "transition":
            transition_unlinked.append(child)
        if child.tag == "state":
            transition[child.get("name")] = []
            state.append(child.get("name"))
    for tr in transition_unlinked:
        fromid = state[int(tr.get("From").split(".")[-1])]
        toid = state[int((tr.get("To").split(".")[-1]))]
        if tr.get(ESLI+"type") == "cw:probabilistic":
           trns = {
               toid: {
                    "type":"probabilistic",
                    "distribution": tr.get("distribution"),
                    "parameter": tr.get("parameter"),
                    "comment": tr.get("comment")
               }
           }
           transition[fromid].append(trns)
        if tr.get(ESLI+"type") == "cw:deterministic":
           trns = {
               toid: {
                    "type":"deterministic",
                    "parameter": tr.get("parameter"),
                    "comment": tr.get("comment")
               }
           }
           transition[fromid].append(trns)
        if tr.get(ESLI+"type") == "cw:Property_Tr":
           trns = {
               toid: {
                    "type":"property",
                    "property": tr.get("name")
               }
           }
           transition[fromid].append(trns)
    return {
        "name": machine.get("name"),
        "type": "state-machine",
        "structure":{
            "states": state,
            "initial": state[int(machine.get("initial").split(".")[-1])],
            "transitions":transition
        }
    }
        

            
        
def calculate_r_c(machine):
    properties = []
    for child in machine:
        properties.append({
            "name": child.get("name"),
            "required": child.get("required"),
            "properties": getNestedProperties(child)
        })
    return properties

def getNestedProperties(properties):
    property = []
    for child in properties:
        properties.append({
            child.get("name"): child.get("value")
        })
    return property


if __name__ == "__main__":
   main()
