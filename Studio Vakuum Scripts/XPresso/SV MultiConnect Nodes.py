"""
SV MultiConnect Nodes

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US: Only works with Nodes, that have one Output port, which are wired to a Nodes with multiple Input ports

Written for Maxon Cinema 4D 2026.2.0
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

        sourceNodes.sort(key=lambda n: n.py)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, targetNode.node)

        failed = []

        for sourceNode in sourceNodes:
            outPort = GetFreePort(sourceNode.node.GetOutPorts())
            if outPort is None:
                continue

            connected = False
            while inputIndex < len(inputPorts):
                inPort = inputPorts[inputIndex]
                inputIndex += 1

                if inPort.GetNrOfConnections() != 0:
                    continue

                result = outPort.Connect(inPort)

                if result:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, sourceNode.node)
                    connected = True
                    break

            if not connected:
                failed.append(f"• '{sourceNode.node.GetName()}': no compatible input port found")
            
        if failed:
            msg = "Connection failed:\n\n" + "\n".join(failed)
            c4d.gui.MessageDialog(msg)
    
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