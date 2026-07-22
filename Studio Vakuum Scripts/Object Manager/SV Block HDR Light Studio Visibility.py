"""Adds a Python tag with a User Data dropdown (Default/On/Off) that locks
editor/render visibility on every selected object.
"""
import c4d

# Template with a placeholder for the User Data ID, filled in at runtime.
TAG_CODE_TEMPLATE = '''import c4d

doc: c4d.documents.BaseDocument
op: c4d.BaseTag
flags: int
priority: int
tp: c4d.modules.thinkingparticles.TP_MasterSystem

MODE_MAP = {{
    0: c4d.MODE_UNDEF,
    1: c4d.MODE_ON,
    2: c4d.MODE_OFF,
}}

ID_UD_MODE = {ud_id}

UD_DESCID = c4d.DescID(
    c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0),
    c4d.DescLevel(ID_UD_MODE, c4d.DTYPE_LONG, 0)
)


def main() -> None:
    obj: c4d.BaseObject = op.GetObject()
    if obj is None:
        return

    ud_value: int = op[UD_DESCID]
    mode: int = MODE_MAP.get(ud_value, c4d.MODE_UNDEF) if ud_value is not None else c4d.MODE_UNDEF

    obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = mode
    obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = mode
'''

TAG_NAME = "Visibility Lock"


def add_user_data_dropdown(tag: c4d.BaseTag) -> int:
    """Creates a User Data cycle dropdown (Default/On/Off) on the tag.
    Returns the actual sub-ID Cinema 4D assigned to it.
    """
    bc: c4d.BaseContainer = c4d.GetCustomDataTypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = "Visibility Mode"
    bc[c4d.DESC_SHORT_NAME] = "Visibility Mode"
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLE
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF

    cycle: c4d.BaseContainer = c4d.BaseContainer()
    cycle[0] = "Default"
    cycle[1] = "On"
    cycle[2] = "Off"
    bc[c4d.DESC_CYCLE] = cycle

    element_descid: c4d.DescID = tag.AddUserData(bc)
    tag[element_descid] = 0  # Default to "Default" (index 0)

    # Pull out the actual sub-ID Cinema 4D assigned (last DescLevel's id).
    ud_id: int = element_descid[-1].id
    return ud_id


def main() -> None:
    doc: c4d.documents.BaseDocument = c4d.documents.GetActiveDocument()
    objects: list[c4d.BaseObject] = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)

    if not objects:
        c4d.gui.MessageDialog("Please select at least one object.")
        return

    doc.StartUndo()

    for obj in objects:
        tag: c4d.BaseTag = c4d.BaseTag(c4d.Tpython)
        if tag is None:
            continue

        tag.SetName(TAG_NAME)

        ud_id: int = add_user_data_dropdown(tag)
        tag[c4d.TPYTHON_CODE] = TAG_CODE_TEMPLATE.format(ud_id=ud_id)

        obj.InsertTag(tag)
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()