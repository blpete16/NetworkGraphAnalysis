#trivially, we can see each edge as an activity
# by what do we combined two edges into one activity?
# 1.  common ip addresses
# 2.  common timeframe (how big?)
# 3.  common ports (available for most communication)



#first try, exact match on:
# ports - both must be present
# IPs - both must be present
# timeframe ignored.
def sg0(act1, act2):
    for ekey1 in act1.edges:
        e1 = act1.edges[ekey1]
        for ekey2 in act2.edges:
            e2 = act2.edges[ekey2]
            #if(e1.sourcePort == e2.sourcePort or e1.sourcePort == e2.destPort):
            #    if(e1.destPort == e2.sourcePort or e1.destPort == e2.destPort):
            if(e1.sourceid == e2.sourceid or e1.sourceid == e2.destid):
                if(e1.destid == e2.sourceid or e1.destid == e2.destid):
                    return True
    return False

def shouldGroup(act1, act2):
    return sg0(act1, act2)

def AnnealActivities(agraph, acts):
    i = 0
    resultActs = []
    while( i < len(acts)):
        baseAct = acts[i]
        j = len(acts) - 1
        while( j > i):
            subAct = acts[j]
            if(shouldGroup(baseAct, subAct)):
                baseAct.ConsumeActivity(subAct)
                del acts[j]
            j = j - 1
        i = i + 1
        resultActs.append(baseAct)
    return resultActs

def CreateActivitySet(agraph):
    activities = []
    for key in agraph.edges:
        a = Activity()
        a.AddEdge(agraph.edges[key],
                  agraph.nodes[agraph.edges[key].sourceid],
                  agraph.nodes[agraph.edges[key].destid])
        activities.append(a)

    activities = AnnealActivities(agraph, activities)
    
    return activities
    
def MergeTwoActivities(aone, atwo):
    aresult = Activity()
    aresult.ConsumeActivity(aone)
    aresult.ConsumeActivity(atwo)
    return aresult

def PrintASet(acts):
    print("act_count:"+str(len(acts)))
    acounts = []
    actotal = 0
    for a in acts:
        acounts.append(len(a.edges))
        actotal = actotal + len(a.edges)
    ave = actotal / float(len(acounts))
    print("act_ave:"+str(ave))
    countsActs = zip(acounts, acts)
    countsActs.sort()
    midind = len(acounts)//2
    print("act_median:"+str(countsActs[midind][0]))
    print("last")
    for i in range(30):
        ind = len(acounts)-i-1
        print("  "+str(countsActs[ind][0]))
        print("    "+str(countsActs[ind][1].endtime - countsActs[ind][1].starttime))
class Activity():
    def __init__(self):
        self.starttime = None
        self.endtime = None
        self.nodes = {}
        self.edges = {}

    def ConsumeActivity(self, atoeat):
        if(self.starttime is None):
            self.starttime = atoeat.starttime
        elif(self.starttime > atoeat.starttime):
            self.starttime = atoeat.starttime
        if(self.endtime is None):
            self.endtime = atoeat.endtime
        elif(self.endtime < atoeat.endtime):
            self.endtime = atoeat.endtime

        for key in atoeat.edges:
            self.edges[key] = atoeat.edges[key]
        for key in atoeat.nodes:
            self.nodes[key] = atoeat.nodes[key]

    def AddEdge(self, aedge, srcNode, dstNode):
        if(len(self.edges) == 0):
            self.starttime = aedge.timesig
            self.endtime = aedge.timesig
        else:
            if(aedge.timesig < self.starttime):
                self.starttime = aedge.timesig
            if(aedge.timesig > self.endtime):
                self.endtime = aedge.timesig
        self.edges[aedge.idval] = aedge
        self.nodes[srcNode.idval] = srcNode
        self.nodes[dstNode.idval] = dstNode

    def IsEdgeIn(self, aedge):
        return aedge.idval in self.edges

    
