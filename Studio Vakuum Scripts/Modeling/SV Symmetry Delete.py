"""
SV Symmetry Delete

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Delete Points Symmetry-Wise

Written for Maxon Cinema 4D 2026.2.0
Python version 3.11.4
"""

import c4d
from c4d import gui, utils

ID_DLG_DELETE_SIDE = 1000000

ID_TABRADIO_X = 1000
ID_TABRADIO_Y = 1100
ID_TABRADIO_Z = 1200

ID_TOLERANCE = 1250
ID_AXIS_SPACE = 1260

ID_BTN_OK     = 1300
ID_BTN_CANCEL = 1301

LABEL_WIDTH = 90
CONTROL_WIDTH = 200

class DeleteSideDialog(gui.GeDialog):
    def __init__(self):
        self.x_side = "Off"
        self.y_side = "Off"
        self.z_side = "Off"
        self.tolerance = 0.001
        self.axis_space = "World"

        self.gadget_x = None
        self.gadget_y = None
        self.gadget_z = None
        self.gadget_axis_space = None

    def CreateLayout(self):
        self.SetTitle("Symmetry Delete")

        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols=2)

        # Origin axis
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Origin Axis")

        items_space = c4d.BaseContainer()
        items_space.SetString(1, "World")
        items_space.SetString(2, "Object")

        bc_space = c4d.BaseContainer()
        bc_space.SetContainer(c4d.DESC_CYCLE, items_space)

        self.gadget_axis_space = self.AddCustomGui(
            ID_AXIS_SPACE, 200000281, '', c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_space
        )
        self.gadget_axis_space.SetData(1)          

        # X axis
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="X axis")

        items_x = c4d.BaseContainer()
        items_x.SetString(1, "Off")
        items_x.SetString(2, "-X")
        items_x.SetString(3, "+X")

        bc_x = c4d.BaseContainer()
        bc_x.SetContainer(c4d.DESC_CYCLE, items_x)

        self.gadget_x = self.AddCustomGui(
            ID_TABRADIO_X, 200000281, '', c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_x
        )
        self.gadget_x.SetData(1)

        # Y axis
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Y axis")

        items_y = c4d.BaseContainer()
        items_y.SetString(1, "Off")
        items_y.SetString(2, "-Y")
        items_y.SetString(3, "+Y")

        bc_y = c4d.BaseContainer()
        bc_y.SetContainer(c4d.DESC_CYCLE, items_y)

        self.gadget_y = self.AddCustomGui(
            ID_TABRADIO_Y, 200000281, '', c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_y
        )
        self.gadget_y.SetData(1)

        # Z axis
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Z axis")

        items_z = c4d.BaseContainer()
        items_z.SetString(1, "Off")
        items_z.SetString(2, "-Z")
        items_z.SetString(3, "+Z")

        bc_z = c4d.BaseContainer()
        bc_z.SetContainer(c4d.DESC_CYCLE, items_z)

        self.gadget_z = self.AddCustomGui(
            ID_TABRADIO_Z, 200000281, '', c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_z
        )
        self.gadget_z.SetData(1)

        # Tolerance
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Tolerance")
        self.AddEditNumberArrows(ID_TOLERANCE, c4d.BFH_SCALEFIT, initw=CONTROL_WIDTH)
        self.SetFloat(ID_TOLERANCE, self.tolerance, min=-1000.0, max=1000.0, step=0.001, format=c4d.FORMAT_FLOAT)
        self.GroupEnd()

        self.AddSeparatorH(c4d.BFH_SCALEFIT)

        # OK / Cancel
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols=2)
        self.AddButton(ID_BTN_CANCEL, c4d.BFH_SCALEFIT, name="Cancel")
        self.AddButton(ID_BTN_OK, c4d.BFH_SCALEFIT, name="OK")
        self.GroupEnd()

        return True

    def Command(self, id, msg):
        if id == ID_TABRADIO_X:
            value = msg[c4d.BFM_ACTION_VALUE]
            if value == 1: self.x_side = "Off"
            elif value == 2: self.x_side = "-X"
            elif value == 3: self.x_side = "+X"

        if id == ID_TABRADIO_Y:
            value = msg[c4d.BFM_ACTION_VALUE]
            if value == 1: self.y_side = "Off"
            elif value == 2: self.y_side = "-Y"
            elif value == 3: self.y_side = "+Y"

        if id == ID_TABRADIO_Z:
            value = msg[c4d.BFM_ACTION_VALUE]
            if value == 1: self.z_side = "Off"
            elif value == 2: self.z_side = "-Z"
            elif value == 3: self.z_side = "+Z"

        if id == ID_BTN_OK:
            self.tolerance = self.GetFloat(ID_TOLERANCE)
            self.Close()

        if id == ID_BTN_CANCEL:
            self.x_side = self.y_side = self.z_side = None
            self.Close()

        if id == ID_AXIS_SPACE:
            value = msg[c4d.BFM_ACTION_VALUE]
            if value == 1:
                self.axis_space = "World"
            elif value == 2:
                self.axis_space = "Object"

        return True

    def Message(self, msg, result):
        bc = c4d.BaseContainer()
        ok = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if ok and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(ID_BTN_OK, None)
            return True
        ok = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if ok and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(ID_BTN_CANCEL, None)
            return True
        return super().Message(msg, result)

    def GetSides(self):
        return self.x_side, self.y_side, self.z_side

    def GetTolerance(self):
        return self.tolerance

    def GetAxisSpace(self):
        return self.axis_space

def delete_points_by_sides(obj, sides, tolerance, axis_space):
    if not isinstance(obj, c4d.PolygonObject):
        return False

    doc = obj.GetDocument()
    mg = obj.GetMg()
    points = obj.GetAllPoints()

    def make_test(side):
        if side == "-X": return lambda p: p.x < -tolerance
        if side == "+X": return lambda p: p.x > tolerance
        if side == "-Y": return lambda p: p.y < -tolerance
        if side == "+Y": return lambda p: p.y > tolerance
        if side == "-Z": return lambda p: p.z < -tolerance
        if side == "+Z": return lambda p: p.z > tolerance
        return lambda p: False

    tests = [make_test(s) for s in sides if s != "Off"]

    if not tests:
        return True

    point_sel = obj.GetPointS()
    point_sel.DeselectAll()

    selected = 0
    for i, point in enumerate(points):
        test_point = mg * point if axis_space == "World" else point

        if any(t(test_point) for t in tests):
            point_sel.Select(i)
            selected += 1

    if selected == 0:
        return True

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

    bc = c4d.BaseContainer()
    res = utils.SendModelingCommand(
        command=c4d.MCOMMAND_DELETE,
        list=[obj],
        mode=c4d.MODELINGCOMMANDMODE_POINTSELECTION,
        bc=bc,
        doc=doc)

    doc.EndUndo()
    c4d.EventAdd()

    return res

def main():
    dlg = DeleteSideDialog()
    ok = dlg.Open(c4d.DLG_TYPE_MODAL)

    if not ok:
        return

    x_side, y_side, z_side = dlg.GetSides()
    tolerance = dlg.GetTolerance()
    axis_space = dlg.GetAxisSpace()

    if x_side is None:
        return

    doc = c4d.documents.GetActiveDocument()
    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    if not sel:
        gui.MessageDialog("Please select at least one polygon object.")
        return

    obj = sel[0]

    if not isinstance(obj, c4d.PolygonObject):
        gui.MessageDialog("The selected object is not a polygon object.")
        return

    active_sides = [s for s in (x_side, y_side, z_side) if s != "Off"]

    delete_points_by_sides(obj, active_sides, tolerance, axis_space)

if __name__ == '__main__':
    main()