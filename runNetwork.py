from ActivityGrouping import CreateActivitySet, PrintASet
from parserone import GenGraph
import sys



def GenActs(afilename):
    agraph = GenGraph(afilename)
    aset = CreateActivitySet(agraph)
    PrintASet(aset)

if __name__ == "__main__":
    GenActs(sys.argv[1])
