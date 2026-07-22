"""
SV Create Objects Op + Condition

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Select the Objects, which creates Object Operator Nodes connected with Condition Node

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

def create_null_with_xpresso():
    dummy_object = c4d.BaseObject(c4d.Onull)
    dummy_object.SetName("Objects")
    doc.InsertObject(dummy_object)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, dummy_object)

    xpresso_tag = dummy_object.MakeTag(c4d.Texpresso)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, xpresso_tag)

    if xpresso_tag is None:
        gui.MessageDialog('Could not create an Xpresso tag!')
        return None

    return xpresso_tag

def create_object_node(xpressonodemaster, root, obj, x, y):
    object_node = xpressonodemaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=x, y=y)

    if object_node is None:
        return None

    object_node[c4d.GV_OBJECT_OBJECT_ID] = obj
    object_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT)
    object_node.SetBit(c4d.BIT_ACTIVE)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, object_node)

    return object_node

def create_condition_node(xpressonodemaster, root, x, y):
    condition_node = xpressonodemaster.CreateNode(root, c4d.ID_OPERATOR_CONDITION, None, x=x, y=y)
    condition_node[c4d.GV_DYNAMIC_DATATYPE] = c4d.DTYPE_BASELISTLINK

    if condition_node is None:
        gui.MessageDialog('Could not create a condition operator!')
        return None

    condition_node.SetBit(c4d.BIT_ACTIVE)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, condition_node)

    return condition_node

def connect_nodes(object_nodes, condition_node):
    for i, object_node in enumerate(object_nodes):
        output_port = object_node.GetOutPort(0)
        input_port = condition_node.GetInPort(i + 1)

        if output_port and input_port:
            success = output_port.Connect(input_port)
            if not success:
                gui.MessageDialog(f'Could not connect {object_node.GetName()} to the Condition Node.')

def main():
    doc.StartUndo()

    try:
        selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

        if not selected_objects:
            gui.MessageDialog('No objects selected!')
            return

        xpresso_tag = get_selected_xpresso_tag()

        if xpresso_tag is None:
            xpresso_tag = create_null_with_xpresso()
            if xpresso_tag is None:
                return

        xpressonodemaster = xpresso_tag.GetNodeMaster()

        if xpressonodemaster is None:
            gui.MessageDialog('Could not retrieve the Xpresso NodeMaster!')
            return

        root = xpressonodemaster.GetRoot()

        start_x = 100
        start_y = 100
        spacing_y = 50

        object_nodes = []

        for i, obj in enumerate(selected_objects):
            x = start_x
            y = start_y + i * spacing_y
            object_node = create_object_node(xpressonodemaster, root, obj, x, y)
            if object_node:
                object_nodes.append(object_node)

        condition_node = create_condition_node(xpressonodemaster, root, start_x + 200, start_y)

        if condition_node is None:
            return

        num_inputs = len(selected_objects) - 2

        for _ in range(num_inputs):
            condition_node.AddPort(c4d.GV_PORT_INPUT, 2000)

        connect_nodes(object_nodes, condition_node)
        c4d.EventAdd()

    finally:
        doc.EndUndo()

if __name__ == '__main__':
    main()