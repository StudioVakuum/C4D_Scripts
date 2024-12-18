"""
SV Create Folder Tex Path

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Create a string of the tex folder path

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
import os

def main():
    doc = c4d.documents.GetActiveDocument()
    project_path = doc.GetDocumentPath()

    if not project_path:
        c4d.gui.MessageDialog("The document is not saved yet.")
        return

    tex_path = os.path.join(project_path, "tex")
    obj = doc.GetActiveObject()

    if obj is None:
        c4d.gui.MessageDialog("Please select an object.")
        return

    bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = "Folder Tex Path"
    bc[c4d.DESC_DEFAULT] = tex_path

    userdata_id = obj.AddUserData(bc)
    obj.SetParameter(userdata_id, tex_path, c4d.DESCFLAGS_SET_0)

    c4d.EventAdd()

if __name__ == '__main__':
    main()