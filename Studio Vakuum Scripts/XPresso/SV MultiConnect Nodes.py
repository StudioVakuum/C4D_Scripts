"""
SV MultiConnect Nodes

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Only works with Nodes, that have one Output port, which are wired to a Nodes with multiple Input ports

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
from math import sqrt

class nodeObject:
    def __init__(self, obj, px, py):
        self.node = obj
        self.px = px
        self.py = py

def GetFreePort(ports):
    for port in ports:
        if port.GetNrOfConnections() == 0:
            return port
    return None

def Distance(node1, node2):
    return sqrt((node2.px - node1.px) ** 2 + (node2.py - node1.py) ** 2)

def ConnectNodes(nodeMaster, doc):
    nodes = []
    root = nodeMaster.GetRoot()
    for node in root.GetChildren():
        if node.GetBit(c4d.BIT_ACTIVE):
            bc = node.GetDataInstance()
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER)
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER)
            px = bcd.GetReal(100)
            py = bcd.GetReal(101)
            nodes.append(nodeObject(node, px, py))
    
    if len(nodes) > 1:
        targetNode = max(nodes, key=lambda n: (n.px, n.py))
        sourceNodes = [n for n in nodes if n != targetNode]
        inputPorts = targetNode.node.GetInPorts()
        inputIndex = 0
        sourceNodes.sort(key=lambda n: Distance(n, targetNode))
        
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, targetNode.node)
        
        for sourceNode in sourceNodes:
            outPort = GetFreePort(sourceNode.node.GetOutPorts())
            if outPort is None:
                continue
            while inputIndex < len(inputPorts):
                if inputPorts[inputIndex].GetNrOfConnections() == 0:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, sourceNode.node)
                    outPort.Connect(inputPorts[inputIndex])
                    inputIndex += 1
                    break
                inputIndex += 1
            if inputIndex >= len(inputPorts):
                break

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()
    
    nodeMaster = c4d.modules.graphview.GetMaster(0)
    if nodeMaster is None:
        return
    
    ConnectNodes(nodeMaster, doc)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()