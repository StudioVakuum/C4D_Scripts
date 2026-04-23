"""
SV Manage Inputs

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Adds or removes Input Ports (Condition Node or Math Node)

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
from c4d import gui

def GetSelectedXPressoNode():
    gv_master = c4d.modules.graphview.GetMaster(0)
    
    if gv_master is None:
        return None
    
    for node in gv_master.GetRoot().GetChildren():
        if node.GetBit(c4d.BIT_ACTIVE):
            return node
    
    return None

def get_current_node_height(node):
    bc = node.GetDataInstance()
    bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER)
    bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER)
    
    current_height = bcd.GetReal(109)
    return current_height

def adjust_node_size(node, num_inputs):
    height_per_input = 20
    min_height = 100
    new_height = max(min_height, min_height + (num_inputs * height_per_input))
    
    bc = node.GetDataInstance()
    bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER)
    bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER)
    bcd.SetReal(109, new_height)

def remove_last_input(node):
    input_ports = [port for port in node.GetInPorts() if port.GetMainID() == 2000]
    if input_ports:
        last_input = input_ports[-1]
        node.RemovePort(last_input)
        return True
    return False

class InputManagerDialog(gui.GeDialog):
    def __init__(self, node):
        super(InputManagerDialog, self).__init__()
        self.node = node
        self.current_inputs = len([port for port in node.GetInPorts() if port.GetMainID() == 2000])
        self.modified = False

    def CreateLayout(self):
        self.SetTitle("Manage Inputs")
        self.GroupBegin(1000, c4d.BFH_SCALEFIT, 3, 1, "Actions")
        self.AddEditNumber(2001, c4d.BFH_SCALEFIT, initw=80, inith=0)
        self.SetInt32(2001, 1)
        self.AddButton(2002, c4d.BFH_SCALEFIT, name="Add")
        self.AddButton(2003, c4d.BFH_SCALEFIT, name="Remove")
        self.GroupEnd()
        self.AddStaticText(1004, c4d.BFH_LEFT, 10, 10, "")
        self.AddButton(4000, c4d.BFH_SCALEFIT, name="Close")
        return True

    def Command(self, id, msg):
        if id == 2002:
            count = self.GetInt32(2001)
            for _ in range(count):
                self.node.AddPort(c4d.GV_PORT_INPUT, 2000)
            self.current_inputs += count
            self.modified = True
            self.Close()
        elif id == 2003:
            count = self.GetInt32(2001)
            for _ in range(min(count, self.current_inputs)):
                if remove_last_input(self.node):
                    self.current_inputs -= 1
            self.modified = True
            self.Close()
        elif id == 4000:
            self.Close()
        
        self.SetString(1001, str(self.current_inputs))
        c4d.EventAdd()
        return True

def manage_inputs():
    node = GetSelectedXPressoNode()
    
    if node is None:
        gui.MessageDialog("Please select a node in the Xpresso Editor.")
        return
    
    dlg = InputManagerDialog(node)
    dlg.Open(c4d.DLG_TYPE_MODAL)
    
    if dlg.modified:
        adjust_node_size(node, dlg.current_inputs)
        c4d.EventAdd()

if __name__ == '__main__':
    manage_inputs()
