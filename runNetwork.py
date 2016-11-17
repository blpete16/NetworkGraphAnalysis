from ActivityGrouping import CreateActivitySet, PrintASet
from parserone import GenGraph
from VisualizeActivity import drawActivity
import sys



def GenActs(afilename):
    agraph = GenGraph(afilename)
    aset = CreateActivitySet(agraph)
    PrintASet(aset)

    drawActivity(agraph, aset[len(aset) - 30])

if __name__ == "__main__":
    GenActs(sys.argv[1])
