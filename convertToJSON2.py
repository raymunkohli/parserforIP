import sys, getopt,json,os
import xml.etree.ElementTree as ET
#https://docs.python.org/3/library/xml.etree.elementtree.html
from optparse import *
ESLI = "{http://www.w3.org/2001/XMLSchema-instance}"
INDENT = 2

def main():
    # match arguments to variables
    args = parser()
    xmlfile = args[0]
    outputdirectory = args[1]
    if not os.path.exists(outputdirectory+"/machines/"):
        os.mkdir(outputdirectory+"/machines/")
    if not os.path.exists(outputdirectory+"/networks/"):
        os.mkdir(outputdirectory + "/networks/")
    model(ET.parse(xmlfile), outputdirectory)

def parser():
    parser = OptionParser(usage="usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    (help, args) = parser.parse_args()
    if len(args) != 2:
        print("usage: convertToJSON.py <XMLFILE> <OUTPUT_DIRECTORY>")
    return args

def model(filet, folder):
    network = []
    network_instance = []
    group = []
    machine_instance = []
    machine_representation = []
    links = []
    #create initial folder

    file = open(folder + '/' + filet.getroot().get("name")+".json", 'w+')

    for child in filet.getroot():
        # first all machine representations must be created
        if child.tag == "machine_representation":
            a = createMachineRep(child,folder)
            machine_representation.append(a)

    for child in filet.getroot():
        if child.tag == "network":
            if child.get(ESLI+"type") == "cw:Network_Representation":
                a = createNetworkRep(child,network,machine_representation,folder)
                network.append(a)

    for child in filet.getroot():
        if child.tag == "network_instance":
            a = createNetworkInstance(child,network)
            network_instance.append(a)
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                links.append(child)
            else:

                machine_instance.append(createMachineInstance(child,machine_representation,network_instance,machine_instance))
        if child.tag == "network":
            if child.get(ESLI+"type")=="cw:Network_Rep_Instance":
                a = createNetworkRepInstance(child,machine_representation,network,folder)
                network.append(a[0])
                network_instance.append(a[1])
    for child in links:
        print("links")
        machine_instance.append(createMachineInstance(child,machine_representation,network_instance,machine_instance))
    for child in filet.getroot():
        if child.tag == "group":
            group.append(processGroup(child,machine_representation,machine_instance,network,network_instance))
    includemachine = []
    netmachine = []
    allmachines = network + machine_representation

    print(network_instance)
    for machine in allmachines:
        includemachine.append({
            "include":"machines/"+machine["name"]
        })
    
    for network in network:
        netmachine.append({
            "include":"network/"+network["name"]
        })

    input = {
        "machines":includemachine,
        "networks":netmachine + group
    }
    file.write(str(json.dumps(input, indent = INDENT)))

def processGroup(group,machineR,machineI,networks,networkRS):
    allmachines = group.get("groupable").split(" ")
    machinesF = []
    print(networkRS)
    for machine in allmachines:
        m = machine.split(".")
        if m[0] == "//@machine_instance":
            machinesF.append(machineI[int(m[-1])])

        if m[0] == "//@network_instance":
            machinesF.append(networkRS[int(m[-1])])

        if m[0] == "//@network":
            pass

    data = {
        "name": group.get("name"),
        "machines":machinesF
    }
    return data

def createNetworkRepInstance(network,machines, networks, outputfolder):
    machine = []
    nets = []
    links = []
    properties = {}
    for child in network:
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                links.append(child)
            else:
                machine.append(createMachineInstance(child,machines,machine,nets))
        if child.tag == "property_r_c":
            a = calculate_r_c(child)
            properties = a
        if child.tag == "network_instance":
            a = createNetworkInstance(child, networks)
            nets.append(a)

    for child in links:
        machine.append(createMachineInstance(child,machines,machine,nets))
        
    data = {
        "name": network.get("name"),
        "type": "network-machine",
        "properties": properties,
        "structure": network.get("name")
    }

    machine_data = {
        "name": network.get("name"),
        "machines":machine + nets
    }

    file = open(outputfolder+"/networks/"+network.get("name")+".json", 'w+')
    file.write(str(json.dumps(machine_data,indent = INDENT)))
    
    file2 = open(outputfolder+"/machines/"+network.get("name")+".json", 'w+')
    file2.write(str(json.dumps(data, indent = INDENT)))

    return machine_data, {
        "name": network.get("name"),
        "machine": network.get("name"),
        "properties": properties
    }

def createNetworkInstance(network, networks):
    properties = {}
    index = networks[int(network.get("network_representation").split(".")[-1])]
    for child in network:
        if child.tag == "property_i_abstract":
            if child.get(ESLI+"type") == "cw:Property_I":
                properties[child.get("name")] = processProperty(child)
            if child.get(ESLI+"type") == "cw:probabilistic_p":
                properties[child.get("name")] =  processPProperty(child)
            if child.get(ESLI+"type") == "cw:deterministic_p":
                properties[child.get("name")] = processDProperty(child)

    data = {
        "name": network.get("name"),
        "machine": index["name"],
        "properties":properties
    }
    
    return data

def fixLinks():
    pass

def createNetworkRep(network, networks, machinez,outputfolder):
    properties = []
    machines = []
    links= []
    for child in network:
        if child.tag == "property_r_c":
            properties.append(calculate_r_c(child))
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                links.append(child)
            else:
                machines.append(createMachineInstance(child,machinez,None,machines))

    for child in links:
        machines.append(createMachineInstance(child,machinez,None,machines))
    machine_data = {
        "name": network.get("name"),
        "type": "network-machine",
        "properties": properties,
        "structure": network.get("name")
    }
    network_data = {
        "name": network.get("name"),
        "machines":machines
    }
    file = open(outputfolder+"/networks/"+network.get("name")+".json", 'w+')
    file.write(str(json.dumps(network_data, indent = INDENT)))

    file2 = open(outputfolder+"/machines/"+network.get("name")+".json", 'w+')
    file2.write(str(json.dumps(machine_data, indent = INDENT)))

    return network_data
    

def createMachineInstance(machine,machines,localnetworks,localmachines):
    properties = {}
    index = machines[int(machine.get("machine_representation").split(".")[-1])]
    
    for child in machine:
        if child.tag == "property_i_abstract":
            if child.get(ESLI+"type") == "cw:Property_I":
                properties[child.get("name")] = processProperty(child)
            if child.get(ESLI+"type") == "cw:probabilistic_p":
                properties[child.get("name")] =  processPProperty(child)
            if child.get(ESLI+"type") == "cw:deterministic_p":
                properties[child.get("name")] = processDProperty(child)
    
    if machine.get(ESLI+"type") == "cw:Link":
        to = machine.get("target").split("@")[-1].split(".")
        fr0m = machine.get("source").split("@")[-1].split(".")
        print(fr0m)
        if (to[0] == "network_instance") or (to[0] == "network"):
            properties["to"] = localnetworks[int(to[1])].get("name")
        if (fr0m[0] == "network_instance") or (fr0m[0] == "network"):
            properties["from"] = localnetworks[int(fr0m[1])].get("name")
        if (fr0m[0] == "machine_instance"):
            print(localmachines)
            properties["from"] = localmachines[int(fr0m[1])].get("name")
        if (to[0] == "machine_instance"):
            print(localmachines)
            properties["to"] = localmachines[int(to[1])].get("name")

    data = {
        "name": machine.get("name"),
        "machine": index["name"],
        "properties":properties
    }
    return data
    


def processProperty(propertyy):
    data = {
        "value":propertyy.get("value")
    }
    return data

def processPProperty(property):
    return {
        "type": "probabilistic",
        "distribution": property.get("distribution"),
        "parameter": property.get("parameter")
    }
    
def processDProperty(property):
        return {
        "type": "deterministic",
        "parameter": property.get("parameter")
    }

def createMachineRep(machine,outputfolder):
    property_r_c = {}
    transition_unlinked = []
    transition = {}
    state = []
    for child in machine:
        if child.tag == "property_r_c":
            property_r_c = calculate_r_c(child)
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
    data = {
        "name": machine.get("name"),
        "type": "state-machine",
        "properties": property_r_c,
        "structure":{
            "states": state,
            "initial": state[int(machine.get("initial").split(".")[-1])],
            "transitions":transition
        }
    }

    file = open(outputfolder+"/machines/"+machine.get("name")+".json", 'w+')
    file.write(str(json.dumps(data, indent = INDENT)))
    return data
            
        
def calculate_r_c(machine):
    properties = {}
    for child in machine:
        if child.get("required"):
            req = 'true'
        else:
            req = 'false'
        properties[child.get("name")] = {
            "required": req,
            "type": child.get("type"),
            "properties": getNestedProperties(child)

        }
    return properties

def getNestedProperties(properties):
    property = {}
    for child in properties:
        property[child.get("name")] = child.get("value")
    return property


if __name__ == "__main__":
   main()
