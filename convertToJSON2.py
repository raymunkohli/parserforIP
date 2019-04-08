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
    #model gen
    network = []
    network_def = []
    network_instance = []
    
    network_rep = []
    group = []
    groupnets = []
    machine_instance = []
    machines_ordered = {}
    missing = []
    machine_representation = []
    links = []
    pos = 0
    number = 0 
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
                network_rep.append(" ")
                network.append(a[0])
                network_def.append(a[1])

    for child in filet.getroot():
        if child.tag == "network_instance":
            a = createNetworkInstance(child,network,network_def)
            network_instance.append(a)
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                machines_ordered[number] = ""
                links.append(child)
                missing.append(number)
                number += 1
            else:
                machines_ordered[number] = pos
                number += 1
                pos += 1
                machine_instance.append(createMachineInstance(child,machine_representation,network_instance,network_rep,machine_instance))
        if child.tag == "network":
            if child.get(ESLI+"type")=="cw:Network_Rep_Instance":
                a = createNetworkRepInstance(child,machine_representation,network,folder,network_def)
                network.append(a[0])
                network_rep.append(a[1])
    mischeck = 0
    for child in links:
        machines_ordered[missing[mischeck]] = pos
        machine_instance.append(createMachineInstance(child,machine_representation,network_instance,network_rep,machine_instance))
        pos += 1
        mischeck += 1
    for child in filet.getroot():
        if child.tag == "group":
            a = processGroup(child,machine_representation,machine_instance,network_rep,network_instance,group,machines_ordered)
            group.append(a[0])
            groupnets.append(a[1])
    includemachine = []
    netmachine = []
    allmachines = network + machine_representation

    for machine in allmachines:
        includemachine.append({
            "include":"machines/"+machine["name"] +".json"
        })
    
    for network in network:
        netmachine.append({
            "include":"networks/"+network["name"]+".json"
        })

    input = {
        "description":"test",
        "machines":includemachine + groupnets,
        "networks":netmachine + group
    }
    file.write(str(json.dumps(input, indent = INDENT)))

def processGroup(group,machineR,machineI,networks,networkRS,groups,machine_orders):
    print("Creating Group: " + group.get("name"))
    allmachines = group.get("groupable").split(" ")
    machinesF = []
    for machine in allmachines:
        m = machine.split(".")
        if m[0] == "//@machine_instance":
            machinesF.append(machineI[int(machine_orders[int(m[-1])])])
        if m[0] == "//@network_instance":
            machinesF.append(networkRS[int(m[-1])])
        if m[0] == "//@network":
            machinesF.append(networks[int(m[-1])])
        if m[0] == "//@group":
            machinesF.append({
                "name":groups[int(m[-1])]["name"],
                "machine":groups[int(m[-1])]["name"]
            })

    data = {
        "name": group.get("name"),
        "machines":machinesF
    }
    networkinfo = {
        "name":group.get("name"),
        "type": "network-machine",
        "structure": {
            "network": group.get("name")
      }
    }
    return data, networkinfo

def createNetworkRepInstance(network,machines, networks, outputfolder, network_def):
    print("Creating Non-defined Network: "+network.get("name"))
    machine = []
    nets = []
    links = []
    properties = {}
    for child in network:
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                links.append(child)
            else:
                machine.append(createMachineInstance(child,machines,nets,nets,machine))
        if child.tag == "property_r_c":
            a = calculate_r_c(child)
            properties = a
        if child.tag == "network_instance":
            a = createNetworkInstance(child, networks,network_def)
            nets.append(a)

    for child in links:
        machine.append(createMachineInstance(child,machines,nets,nets,machine))
        
    data = {
        "name": network.get("name"),
        "type": "network-machine",
        "properties": properties,
        "structure": {
            "Network" : network.get("name")
        }
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

def createNetworkInstance(network, networks,networkdef):
    print("Creating Network Instance: "+network.get("name"))
    properties = {}
    index = networks[int(network.get("network_representation").split(".")[-1])]
    for child in network:
        property_r = child.get("property_r").split(".")[1].split("/")[0]
        if child.tag == "property_i_abstract":
            pIndex = networkdef[int(property_r)]["properties"][child.get("name")]["type"]
            if child.get(ESLI+"type") == "cw:Property_I":
                properties[child.get("name")] = processProperty(child,pIndex)
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


def createNetworkRep(network, networks, machinez,outputfolder):
    print("Creating Network Representation: "+ network.get("name"))
    properties = {}
    machines = []
    links= []
    for child in network:
        if child.tag == "property_r_c":
            properties=(calculate_r_c(child))
        if child.tag == "machine_instance":
            if child.get(ESLI+"type") == "cw:Link":
                links.append(child)
            else:
                machines.append(createMachineInstance(child,machinez,None,None,machines))

    for child in links:
        machines.append(createMachineInstance(child,machinez,None,None,machines))
    machine_data = {
        "name": network.get("name"),
        "type": "network-machine",
        "properties": properties,
        "structure": {
            "Network" : network.get("name")
        }
    }
    network_data = {
        "name": network.get("name"),
        "machines":machines
    }
    file = open(outputfolder+"/networks/"+network.get("name")+".json", 'w+')
    file.write(str(json.dumps(network_data, indent = INDENT)))

    file2 = open(outputfolder+"/machines/"+network.get("name")+".json", 'w+')
    file2.write(str(json.dumps(machine_data, indent = INDENT)))

    return network_data,machine_data
    

def createMachineInstance(machine,machines,localnetworks,localnetinstances,localmachines):
    print("Creating Machine Instance: "+machine.get("name"))
    properties = {}
    index = machines[int(machine.get("machine_representation").split(".")[-1])]
    for child in machine:
        if child.tag == "property_i_abstract":
            pIndex = index["properties"][child.get("name")]["type"]
            if child.get(ESLI+"type") == "cw:Property_I":
                properties[child.get("name")] = processProperty(child,pIndex)
            if child.get(ESLI+"type") == "cw:probabilistic_p":
                properties[child.get("name")] =  processPProperty(child)
            if child.get(ESLI+"type") == "cw:deterministic_p":
                properties[child.get("name")] = processDProperty(child)
    
    if machine.get(ESLI+"type") == "cw:Link":
        to = machine.get("target").split("@")[-1].split(".")
        fr0m = machine.get("source").split("@")[-1].split(".")
        if (to[0] == "network_instance"):
            properties["to"] = localnetworks[int(to[1])].get("name")
        if (fr0m[0] == "network_instance"):
            properties["from"] = localnetworks[int(fr0m[1])].get("name")
        if (to[0] == "network"):
            properties["to"] = localnetinstances[int(to[1])].get("name")
        if (fr0m[0] == "network"):
            properties["from"] = localnetinstances[int(fr0m[1])].get("name")
        
        if (fr0m[0] == "machine_instance"):
            properties["from"] = localmachines[int(fr0m[1])].get("name")
        if (to[0] == "machine_instance"):
            properties["to"] = localmachines[int(to[1])].get("name")

    data = {
        "name": machine.get("name"),
        "machine": index["name"],
        "properties":properties
    }
    return data
    


def processProperty(propertyy,type):
    if type == "Boolean" or type == "boolean":
        if propertyy.get("value") == "True" or propertyy.get("value") == "true":
            value = True
        if propertyy.get("value") == "False" or propertyy.get("value") == "false":
            value = False
    elif type == "Number":
        value = float(propertyy.get("value"))
    else:
        value = str(propertyy.get("value"))
    
    data = value
    
    return data

def processPProperty(property):
    return {
        "type": "probabilistic",
        "distribution": property.get("distribution"),
        "parameter": float(property.get("parameter"))
    }
    
def processDProperty(property):
        return {
        "type": "deterministic",
        "parameter": float(property.get("parameter"))
    }

def createMachineRep(machine,outputfolder):
    print("Creating Machine Representation: "+machine.get("name"))
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
           trns =  {toid:[{
                    "type":"probabilistic",
                    "distribution": tr.get("distribution"),
                    "parameter": float(tr.get("parameter")),
                    "comment": tr.get("comment")
               }]}
           transition[fromid] = trns
        if tr.get(ESLI+"type") == "cw:deterministic":
           trns = {
               toid: [{
                    "type":"deterministic",
                    "parameter": float(tr.get("parameter")),
                    "comment": tr.get("comment")
               }]
           }
           transition[fromid] = trns
        if tr.get(ESLI+"type") == "cw:Property_Tr":
           trns = {
               toid: [{
                    "type":"property",
                    "property": tr.get("name")
               }]
           }
           property_r_c[tr.get("name")] = {
                "required": True,
                "type": tr.get("type"),
           }
           transition[fromid] = trns
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
            req = True
        else:
            req = False
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
