"""
SV Center to Global Zero

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Position and axis of the children won't be affected, when setting the parent axis to global zero position

Written for Maxon Cinema 4D 2024.2.0
Python version 3.11.4
"""

import c4d

def ResetObjectPosition(obj):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    children_global_matrices = {}
    for child in obj.GetChildren():
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
        children_global_matrices[child] = child.GetMg()
    
    obj.SetMg(c4d.Matrix())
    
    for child, global_matrix in children_global_matrices.items():
        child.SetMg(global_matrix)

def main():
    doc = c4d.documents.GetActiveDocument()
    
    doc.StartUndo()
    
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    for obj in selected_objects:
        ResetObjectPosition(obj)
    
    doc.EndUndo()
    
    c4d.EventAdd()

if __name__ == '__main__':
    main()