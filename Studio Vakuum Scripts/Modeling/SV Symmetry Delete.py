"""
SV Symmetry Delete

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US: Delete Points Symmetry-Wise

Written for Maxon Cinema 4D 2026.3.2
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

ID_BTN_OK = 1300
ID_BTN_CANCEL = 1301

LABEL_WIDTH = 90
CONTROL_WIDTH = 90
BUTTON_WIDTH = 90
CONTROL_FLAGS = c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT
DEFAULT_TOLERANCE = 0.001
OBJECT_DIRTY_FLAGS = c4d.DIRTYFLAGS_DATA | c4d.DIRTYFLAGS_MATRIX

class DeleteSideDialog(gui.GeDialog):
    def __init__(self, objects):
        self.doc = objects[0].GetDocument()
        self.x_side = "Off"
        self.y_side = "Off"
        self.z_side = "Off"
        self.tolerance = DEFAULT_TOLERANCE
        self.axis_space = "World"
        self._handling_core_message = False

        self.clone_flags = (
            c4d.COPYFLAGS_NO_ANIMATION
            | c4d.COPYFLAGS_NO_HIERARCHY
            | c4d.COPYFLAGS_NO_BITS
        )
        self.object_records = self.CaptureObjects(objects)
        self.expected_states = []
        self.CaptureExpectedStates()
        self.copy_flags = self.clone_flags | getattr(
            c4d, "COPYFLAGS_PRIVATE_IDENTMARKER", 0
        )
        self._initializing = True

        self.gadget_x = None
        self.gadget_y = None
        self.gadget_z = None
        self.gadget_axis_space = None

    def CaptureObjects(self, objects):
        return [
            (obj, obj.GetClone(self.clone_flags), obj.GetMg())
            for obj in objects
        ]

    def GetCurrentSelection(self):
        doc = c4d.documents.GetActiveDocument()
        selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        polygon_objects = [
            obj for obj in selected if isinstance(obj, c4d.PolygonObject)
        ]
        return doc, polygon_objects

    def SelectionMatchesRecords(self, objects):
        if len(objects) != len(self.object_records):
            return False

        remaining = list(objects)
        for record_obj, _, _ in self.object_records:
            match_index = next(
                (
                    index for index, obj in enumerate(remaining)
                    if obj == record_obj
                ),
                None,
            )
            if match_index is None:
                return False
            remaining.pop(match_index)
        return True

    def RefreshSelection(self):
        doc, objects = self.GetCurrentSelection()
        if doc == self.doc and self.SelectionMatchesRecords(objects):
            return False

        self.RestorePreviewState(notify=False)
        document_changed = doc != self.doc
        self.doc = doc
        self.object_records = self.CaptureObjects(objects)
        if document_changed:
            self.expected_states = []
        return True

    def CaptureExpectedStates(self):
        self.expected_states = [
            (
                obj.GetDirty(OBJECT_DIRTY_FLAGS),
                obj.GetPointCount(),
                obj.GetPolygonCount(),
            )
            for obj, _, _ in self.object_records
            if obj.GetDocument() is not None
        ]

    def ObjectStateChanged(self):
        active_records = [
            record for record in self.object_records
            if record[0].GetDocument() is not None
        ]
        if len(active_records) != len(self.expected_states):
            return True

        for (obj, _, _), expected in zip(
            active_records, self.expected_states
        ):
            current = (
                obj.GetDirty(OBJECT_DIRTY_FLAGS),
                obj.GetPointCount(),
                obj.GetPolygonCount(),
            )
            if current != expected:
                return True
        return False

    def ResetControls(self):
        self._initializing = True
        self.x_side = "Off"
        self.y_side = "Off"
        self.z_side = "Off"
        self.axis_space = "World"
        self.tolerance = DEFAULT_TOLERANCE

        self.gadget_axis_space.SetData(1)
        self.gadget_x.SetData(1)
        self.gadget_y.SetData(1)
        self.gadget_z.SetData(1)
        self.SetFloat(
            ID_TOLERANCE,
            self.tolerance,
            min=-1000.0,
            max=1000.0,
            step=0.001,
            format=c4d.FORMAT_FLOAT,
        )
        self._initializing = False

    def HandleExternalObjectChange(self):
        doc, objects = self.GetCurrentSelection()
        self.doc = doc
        self.object_records = self.CaptureObjects(objects)
        self.ResetControls()
        self.CaptureExpectedStates()
        c4d.EventAdd()

    def CreateLayout(self):
        self.SetTitle("Symmetry Delete")

        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols=2)
        self.GroupBorderSpace(8, 8, 6, 0)

        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Origin Axis")

        items_space = c4d.BaseContainer()
        items_space.SetString(1, "World")
        items_space.SetString(2, "Object")

        bc_space = c4d.BaseContainer()
        bc_space.SetContainer(c4d.DESC_CYCLE, items_space)

        self.gadget_axis_space = self.AddCustomGui(
            ID_AXIS_SPACE, 200000281, '', CONTROL_FLAGS, CONTROL_WIDTH, 0, bc_space
        )

        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="X axis")

        items_x = c4d.BaseContainer()
        items_x.SetString(1, "Off")
        items_x.SetString(2, "-X")
        items_x.SetString(3, "+X")

        bc_x = c4d.BaseContainer()
        bc_x.SetContainer(c4d.DESC_CYCLE, items_x)

        self.gadget_x = self.AddCustomGui(
            ID_TABRADIO_X, 200000281, '', CONTROL_FLAGS, CONTROL_WIDTH, 0, bc_x
        )

        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Y axis")

        items_y = c4d.BaseContainer()
        items_y.SetString(1, "Off")
        items_y.SetString(2, "-Y")
        items_y.SetString(3, "+Y")

        bc_y = c4d.BaseContainer()
        bc_y.SetContainer(c4d.DESC_CYCLE, items_y)

        self.gadget_y = self.AddCustomGui(
            ID_TABRADIO_Y, 200000281, '', CONTROL_FLAGS, CONTROL_WIDTH, 0, bc_y
        )

        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Z axis")

        items_z = c4d.BaseContainer()
        items_z.SetString(1, "Off")
        items_z.SetString(2, "-Z")
        items_z.SetString(3, "+Z")

        bc_z = c4d.BaseContainer()
        bc_z.SetContainer(c4d.DESC_CYCLE, items_z)

        self.gadget_z = self.AddCustomGui(
            ID_TABRADIO_Z, 200000281, '', CONTROL_FLAGS, CONTROL_WIDTH, 0, bc_z
        )

        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="Tolerance")
        self.AddEditNumberArrows(ID_TOLERANCE, c4d.BFH_LEFT, initw=CONTROL_WIDTH)
        self.GroupEnd()

        self.AddStaticText(0, c4d.BFH_SCALEFIT, 0, 8, "")

        self.GroupBegin(0, c4d.BFH_LEFT, cols=2)
        self.GroupBorderSpace(6, 0, 6, 8)
        self.AddButton(
            ID_BTN_CANCEL, c4d.BFH_LEFT, initw=BUTTON_WIDTH, name="Cancel"
        )
        self.AddButton(
            ID_BTN_OK, c4d.BFH_LEFT, initw=BUTTON_WIDTH, name="OK"
        )
        self.GroupEnd()

        return True

    def InitValues(self):
        self.ResetControls()
        self.UpdatePreview()
        return True

    def CoreMessage(self, id, msg):
        if (
            id == c4d.EVMSG_CHANGE
            and not self._handling_core_message
            and self.CheckCoreMessage(msg)
        ):
            self._handling_core_message = True
            try:
                if self.ObjectStateChanged():
                    self.HandleExternalObjectChange()
                elif self.RefreshSelection():
                    self.UpdatePreview()
            finally:
                self._handling_core_message = False

        return super().CoreMessage(id, msg)

    def UpdatePreview(self):
        if self._initializing:
            return

        self.RefreshSelection()

        c4d.StopAllThreads()

        sides = [
            side for side in (self.x_side, self.y_side, self.z_side)
            if side != "Off"
        ]
        self.RestorePreviewState(notify=False)
        for obj, original, world_matrix in self.object_records:
            if obj.GetDocument() is None:
                continue
            point_ids = get_matching_point_ids(
                original,
                sides,
                self.tolerance,
                self.axis_space,
                world_matrix,
            )
            delete_point_ids(obj, point_ids, add_undo=False, notify=False)
            obj.Message(c4d.MSG_UPDATE)
        self.CaptureExpectedStates()
        c4d.EventAdd()

    def RestorePreviewState(self, notify=True):
        c4d.StopAllThreads()
        for obj, original, _ in self.object_records:
            if obj.GetDocument() is None:
                continue
            original.CopyTo(obj, self.copy_flags)
            obj.Message(c4d.MSG_UPDATE)

        if notify:
            self.CaptureExpectedStates()
            c4d.EventAdd()

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
            if self.Finalize():
                self.CommitCurrentState()

        if id == ID_BTN_CANCEL:
            self.x_side = self.y_side = self.z_side = None
            self.RestorePreviewState()
            self.Close()

        if id == ID_AXIS_SPACE:
            value = msg[c4d.BFM_ACTION_VALUE]
            if value == 1:
                self.axis_space = "World"
            elif value == 2:
                self.axis_space = "Object"

        if id == ID_TOLERANCE:
            self.tolerance = self.GetFloat(ID_TOLERANCE)

        if id in (
            ID_TABRADIO_X,
            ID_TABRADIO_Y,
            ID_TABRADIO_Z,
            ID_TOLERANCE,
            ID_AXIS_SPACE,
        ):
            self.UpdatePreview()

        return True

    def CommitCurrentState(self):
        objects = [
            obj for obj, _, _ in self.object_records
            if obj.GetDocument() is not None
        ]
        self.object_records = self.CaptureObjects(objects)
        self.CaptureExpectedStates()

    def Finalize(self):
        self.RefreshSelection()
        sides = [
            side for side in (self.x_side, self.y_side, self.z_side)
            if side != "Off"
        ]

        point_ids_by_object = [
            (obj, get_matching_point_ids(
                original,
                sides,
                self.tolerance,
                self.axis_space,
                world_matrix,
            ))
            for obj, original, world_matrix in self.object_records
            if obj.GetDocument() is not None
        ]

        self.RestorePreviewState(notify=False)
        changed = [
            (obj, point_ids)
            for obj, point_ids in point_ids_by_object
            if point_ids
        ]
        if not changed:
            c4d.EventAdd()
            return True

        success = True
        self.doc.StartUndo()
        try:
            for obj, point_ids in changed:
                self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                result = delete_point_ids(
                    obj, point_ids, add_undo=False, notify=False
                )
                if result is False:
                    success = False
        finally:
            self.doc.EndUndo()

        c4d.EventAdd()
        if not success:
            self.UpdatePreview()
            gui.MessageDialog(
                "The symmetry deletion could not be applied to every object."
            )
            return False
        return True

    def DestroyWindow(self):
        self.RestorePreviewState()

    def GetSides(self):
        return self.x_side, self.y_side, self.z_side

    def GetTolerance(self):
        return self.tolerance

    def GetAxisSpace(self):
        return self.axis_space

def get_matching_point_ids(
    obj, sides, tolerance, axis_space, world_matrix=None
):
    if not isinstance(obj, c4d.PolygonObject):
        return []

    mg = world_matrix if world_matrix is not None else obj.GetMg()

    def make_test(side):
        if side == "-X": return lambda p: p.x < -tolerance
        if side == "+X": return lambda p: p.x > tolerance
        if side == "-Y": return lambda p: p.y < -tolerance
        if side == "+Y": return lambda p: p.y > tolerance
        if side == "-Z": return lambda p: p.z < -tolerance
        if side == "+Z": return lambda p: p.z > tolerance
        return lambda p: False

    tests = [make_test(side) for side in sides if side != "Off"]
    if not tests:
        return []

    result = []
    for index, point in enumerate(obj.GetAllPoints()):
        test_point = mg * point if axis_space == "World" else point
        if any(test(test_point) for test in tests):
            result.append(index)

    return result


def delete_point_ids(obj, point_ids, add_undo=True, notify=True):
    if not isinstance(obj, c4d.PolygonObject):
        return False

    if not point_ids:
        return True

    doc = obj.GetDocument()
    c4d.StopAllThreads()
    if add_undo:
        doc.StartUndo()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

    try:
        point_sel = obj.GetPointS()
        point_sel.DeselectAll()
        for point_id in point_ids:
            point_sel.Select(point_id)

        bc = c4d.BaseContainer()
        res = utils.SendModelingCommand(
            command=c4d.MCOMMAND_DELETE,
            list=[obj],
            mode=c4d.MODELINGCOMMANDMODE_POINTSELECTION,
            bc=bc,
            doc=doc)
    finally:
        if add_undo:
            doc.EndUndo()

    if notify:
        c4d.EventAdd()

    return res


def delete_points_by_sides(obj, sides, tolerance, axis_space):
    point_ids = get_matching_point_ids(obj, sides, tolerance, axis_space)
    return delete_point_ids(obj, point_ids)

_dlg = None


def main():
    global _dlg
    doc = c4d.documents.GetActiveDocument()
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    if not selected:
        gui.MessageDialog("Please select at least one polygon object.")
        return

    polygon_objects = [
        obj for obj in selected if isinstance(obj, c4d.PolygonObject)
    ]
    if not polygon_objects:
        gui.MessageDialog("Please select at least one polygon object.")
        return

    _dlg = DeleteSideDialog(polygon_objects)
    _dlg.Open(c4d.DLG_TYPE_ASYNC, pluginid=ID_DLG_DELETE_SIDE)

if __name__ == '__main__':
    main()