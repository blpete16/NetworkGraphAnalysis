
from datetime import datetime
import os
import sys

idbasis = 0
def genid():
    global idbasis
    idbasis = idbasis + 1
    return idbasis

class Graph():
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def AddNode(self, anode):
        self.nodes[anode.idval] = anode

    def AddEdge(self, aedge):
        self.edges[aedge.idval] = aedge

    def findNode(self, ip, port):
        for key in self.nodes:
            if(self.nodes[key].ipportmatch(ip, port)):
                return self.nodes[key]
        return None

    def PrintGraphInfo(self):
        print("NodeCount:"+str(len(self.nodes))+ "\n")
        print("EdgeCount:"+str(len(self.edges))+ "\n")
        

class Edge():
    def __init__(self):
        self.idval = genid()
        self.sourceid = 0
        self.destid = 0
        self.sourcePort = ""
        self.destPort = ""
        self.timesig = None

class Node():
    def __init__(self):
        self.idval = genid()
        self.sourceedges = []
        self.destedges = []
        self.ip = ""
        
    def ipportmatch(self, aip, aport):
        if(self.ip == aip):
            return True
        return False

    def AddSourceEdge(self, aedge):
        self.sourceedges.append(aedge)

    def AddDestEdge(self, aedge):
        self.destedges.append(aedge)

def BuildNode(aip, aport):
    n = Node()
    n.ip = aip
    #n.port = aport
    return n

def AddSetToGraph(agraph, aset, lcount):
    commline = aset[2]
    comms = commline.split(" ")
    source = comms[1].split(":")
    timestr = comms[0]
    dest = comms[3].split(":")
    sourceip = source[0]
    sourceport = ""
    try:
        sourceport = source[1]
    except IndexError:
        sourceport = ""
    destip = dest[0]
    destport = ""
    try:
        destport = dest[1]
    except IndexError:
        destport = ""
    snode = agraph.findNode(sourceip, sourceport)
    if(snode == None):
        snode = BuildNode(sourceip, sourceport)
        agraph.AddNode(snode)
    dnode = agraph.findNode(destip, destport)
    if(dnode == None):
        dnode = BuildNode(destip, destport)
        agraph.AddNode(dnode)

    aedge = Edge()
    aedge.sourceid = snode.idval
    aedge.destid = dnode.idval
    aedge.sourcePort = sourceport
    aedge.destPort = destport
    timeform = '%m/%d-%H:%M:%S.%f'
    try:
        aedge.timesig = datetime.strptime(timestr, timeform)
    except ValueError:
        print("ERRDATETIME")
        print(str(aset))
        print("")
        raise ValueError("Bad Thing")
    snode.AddSourceEdge(aedge)
    dnode.AddDestEdge(aedge)
    agraph.AddEdge(aedge)
        

def GenGraph(filename):
    subset = []
    gret = Graph()
    with open(filename, 'r') as ifile:
        lcount = 0
        for line in ifile:
            if(line.startswith("[**]")):
                if(len(subset) > 0):
                    AddSetToGraph(gret, subset, lcount)
                subset = [line]
            else:
                subset.append(line)
            lcount = lcount + 1
    return gret

if __name__ == "__main__":
    rgraph = GenGraph(sys.argv[1])
    rgraph.PrintGraphInfo()
