"""
SV Create Material Op

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Select the Materials, which creates Material Operator Nodes

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

def main():
    doc.StartUndo()

    selected_materials = doc.GetActiveMaterials()

    if not selected_materials:
        gui.MessageDialog('No materials selected!')
        doc.EndUndo()
        return

    xp_tag = get_selected_xpresso_tag()

    if xp_tag is None:
        gui.MessageDialog('No Xpresso tag selected!')
        doc.EndUndo()
        return

    xpressonodemaster = xp_tag.GetNodeMaster()
    root = xpressonodemaster.GetRoot()

    start_x = 100
    start_y = 100
    spacing_y = 50

    created_nodes = []

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, xp_tag)

    for i, mat in enumerate(selected_materials):
        x = start_x
        y = start_y + i * spacing_y

        material_node = xpressonodemaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=x, y=y)

        if material_node is None:
            continue

        material_node[c4d.GV_OBJECT_OBJECT_ID] = mat
        material_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT)
        created_nodes.append(material_node)

    xp_tag.SetDirty(c4d.DIRTYFLAGS_ALL)

    for node in created_nodes:
        node.SetBit(c4d.BIT_ACTIVE)

    c4d.EventAdd()
    doc.EndUndo()

if __name__ == '__main__':
    main()