"""
SV Create Material Op + Condition

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Select the Materials, which creates Material Operator Nodes wired with Condition Node

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
from c4d import gui

def get_selected_xpresso_tag():
    selected_tags = doc.GetActiveTags()
    
    for tag in selected_tags:
        if tag.GetType() == c4d.Texpresso:
            return tag
    return None

def create_dummy_object(name):
    dummy_object = c4d.BaseObject(c4d.Onull)
    dummy_object.SetName(name)
    doc.InsertObject(dummy_object)
    doc.AddUndo(c4d.UNDOTYPE_NEW, dummy_object)
    return dummy_object

def create_xpresso_tag(dummy_object):
    xpresso_tag = dummy_object.MakeTag(c4d.Texpresso)
    if xpresso_tag is None:
        gui.MessageDialog('Could not create Xpresso tag!')
    return xpresso_tag

def create_material_node(xpressonodemaster, material, x, y):
    material_node = xpressonodemaster.CreateNode(
        xpressonodemaster.GetRoot(), 
        c4d.ID_OPERATOR_OBJECT, 
        None, 
        x=x, 
        y=y
    )
    if material_node:
        material_node[c4d.GV_OBJECT_OBJECT_ID] = material
        material_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT)
        material_node.SetBit(c4d.BIT_ACTIVE) 
    return material_node

def create_condition_node(xpressonodemaster, x, y):
    condition_node = xpressonodemaster.CreateNode(
        xpressonodemaster.GetRoot(), 
        c4d.ID_OPERATOR_CONDITION, 
        None, 
        x=x, 
        y=y
    )
    if condition_node:
        condition_node[c4d.GV_DYNAMIC_DATATYPE] = c4d.DTYPE_BASELISTLINK
        condition_node.SetBit(c4d.BIT_ACTIVE)
    return condition_node

def connect_nodes(material_nodes, condition_node):
    num_inputs = len(material_nodes) - 2
    for _ in range(num_inputs):
        condition_node.AddPort(c4d.GV_PORT_INPUT, 2000)

    for i, material_node in enumerate(material_nodes):
        output_port = material_node.GetOutPort(0)
        input_port = condition_node.GetInPort(i + 1)

        if output_port and input_port:
            success = output_port.Connect(input_port)
            if not success:
                gui.MessageDialog(f'Could not establish a connection between {material_node.GetName()} and Condition Node.')

def main():
    selected_materials = doc.GetActiveMaterials()

    if not selected_materials:
        gui.MessageDialog('No materials selected!')
        return

    doc.StartUndo()

    try:
        xpresso_tag = get_selected_xpresso_tag()

        if xpresso_tag is None:
            dummy_object = create_dummy_object("Materials")
            xpresso_tag = create_xpresso_tag(dummy_object)
            if xpresso_tag is None:
                return
        else:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, xpresso_tag)

        xpressonodemaster = xpresso_tag.GetNodeMaster()
        if xpressonodemaster is None:
            gui.MessageDialog('Could not retrieve the Xpresso NodeMaster!')
            return

        start_x = 100
        start_y = 100
        spacing_y = 50

        material_nodes = []

        for i, mat in enumerate(selected_materials):
            x = start_x
            y = start_y + i * spacing_y
            material_node = create_material_node(xpressonodemaster, mat, x, y)
            if material_node:
                material_nodes.append(material_node)

        condition_node = create_condition_node(xpressonodemaster, start_x + 200, start_y)
        if condition_node is None:
            return

        connect_nodes(material_nodes, condition_node)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, xpresso_tag)

    finally:
        doc.EndUndo()

    c4d.EventAdd()

if __name__ == '__main__':
    main()
