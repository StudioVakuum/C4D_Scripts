"""
SV Axis Orientation

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Rotate Object Axis Orientation without affecting the Object itself

Written for Maxon Cinema 4D 2026.2.0
Python version 3.11.4
"""

import c4d
import math
from c4d import gui

# ─── DIALOG IDs ───────────────────────────────────────────────────────────────
ID_DLG_AXIS_FIX = 1000001
ID_TABRADIO_X = 2000
ID_TABRADIO_Y = 2100
ID_TABRADIO_Z = 2200
ID_BTN_OK = 2300
ID_BTN_CANCEL = 2301
LABEL_WIDTH = 90
CONTROL_WIDTH = 200

# ──────────────────────────────────────────────────────────────────────────────
# ─── CORE LOGIC ───────────────────────────────────────────────────────────────
def mode_to_axis_angle(mode):
    if mode in (None, "Off"):
        return None, None
    sign = -180.0 if mode[0] == "-" else 180.0
    letter = mode[1]
    
    mapping = {"X": "H", "Y": "B", "Z": "P"}
    return mapping[letter], sign

def get_delta_matrix(axis, angle_rad):
    if axis == "H":
        return c4d.utils.MatrixRotY(angle_rad)
    elif axis == "P":
        return c4d.utils.MatrixRotX(angle_rad)
    elif axis == "B":
        return c4d.utils.MatrixRotZ(angle_rad)
    raise ValueError("axis must be 'H', 'P', or 'B'")

def rotate_normals(obj, inv_delta):
    normal_tag = obj.GetTag(c4d.Tnormal)
    if normal_tag is None:
        return
    rot = c4d.Matrix(c4d.Vector(0, 0, 0), inv_delta.v1, inv_delta.v2, inv_delta.v3)
    data = normal_tag.GetDataAddressW()
    for i in range(obj.GetPolygonCount()):
        ns = c4d.NormalTag.Get(data, i)
        ns["a"] = rot * ns["a"]
        ns["b"] = rot * ns["b"]
        ns["c"] = rot * ns["c"]
        ns["d"] = rot * ns["d"]
        c4d.NormalTag.Set(data, i, ns)
    normal_tag.Message(c4d.MSG_UPDATE)

def rotate_axis_mesh(obj, delta):
    inv_delta = ~delta
    obj.SetAllPoints([inv_delta * p for p in obj.GetAllPoints()])
    obj.Message(c4d.MSG_POINTS_CHANGED)
    rotate_normals(obj, inv_delta)

def rotate_axis_object(obj, delta):
    world_mg = obj.GetMg()
    pos = world_mg.off
    new_mg = c4d.Matrix(
        pos,
        world_mg.v1 * delta,
        world_mg.v2 * delta,
        world_mg.v3 * delta,
    )
    inv_new_mg = ~new_mg
    child_worlds = []
    child = obj.GetDown()
    while child:
        child_worlds.append((child, child.GetMg()))
        child = child.GetNext()
    obj.SetMg(new_mg)
    for child, child_world in child_worlds:
        child.SetMl(inv_new_mg * child_world)
    obj.Message(c4d.MSG_UPDATE)

def process_object(obj, axis, angle_deg):
    angle_rad = math.radians(angle_deg)
    delta = get_delta_matrix(axis, angle_rad)
    if obj.CheckType(c4d.Opolygon) or obj.CheckType(c4d.Ospline):
        rotate_axis_mesh(obj, delta)
    rotate_axis_object(obj, delta)

# ─── SNAPSHOT HELPERS ─────────────────────────────────────────────────────────
def _snapshot_object(obj):
    """Return a dict with everything needed to restore obj to its current state."""
    snap = {
        "mg": obj.GetMg(),
        "points": obj.GetAllPoints() if obj.CheckType(c4d.Opolygon) or obj.CheckType(c4d.Ospline) else None,
    }
    children = []
    child = obj.GetDown()
    while child:
        children.append((child, child.GetMl()))
        child = child.GetNext()
    snap["children"] = children
    
    normal_tag = obj.GetTag(c4d.Tnormal)
    if normal_tag:
        data_r = normal_tag.GetDataAddressR()
        normals = []
        for i in range(obj.GetPolygonCount()):
            ns = c4d.NormalTag.Get(data_r, i)
            normals.append({k: c4d.Vector(v) for k, v in ns.items()})
        snap["normals"] = normals
    else:
        snap["normals"] = None
    return snap

def _restore_object(obj, snap):
    """Restore obj to the state captured by _snapshot_object."""
    obj.SetMg(snap["mg"])
    if snap["points"] is not None:
        obj.SetAllPoints(snap["points"])
        obj.Message(c4d.MSG_POINTS_CHANGED)
    for child, ml in snap["children"]:
        child.SetMl(ml)
    if snap["normals"] is not None:
        normal_tag = obj.GetTag(c4d.Tnormal)
        if normal_tag:
            data_w = normal_tag.GetDataAddressW()
            for i, ns in enumerate(snap["normals"]):
                c4d.NormalTag.Set(data_w, i, ns)
            normal_tag.Message(c4d.MSG_UPDATE)
    obj.Message(c4d.MSG_UPDATE)

# ─── ASYNC DIALOG ─────────────────────────────────────────────────────────────
class AxisOrientationDialog(gui.GeDialog):
    def __init__(self, doc, selected, snapshots):
        self.doc = doc
        self.selected = selected
        self.snapshots = snapshots
        self.x_mode = "Off"
        self.y_mode = "Off"
        self.z_mode = "Off"
        self._cancelled = False
        self.gadget_x = None
        self.gadget_y = None
        self.gadget_z = None
        self.gadget_axis_space = None

    def CreateLayout(self):
        self.SetTitle("SV Axis Orientation Fix")
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols=2, title="Axis Rotation")
        self.GroupBorderSpace(8, 8, 6, 0)
        
        # X axis
        self.AddStaticText(0, c4d.BFH_LEFT, initw=LABEL_WIDTH, name="X axis")
        items_x = c4d.BaseContainer()
        items_x.SetString(1, "Off")
        items_x.SetString(2, "-X")
        items_x.SetString(3, "+X")
        bc_x = c4d.BaseContainer()
        bc_x.SetContainer(c4d.DESC_CYCLE, items_x)
        self.gadget_x = self.AddCustomGui(
            ID_TABRADIO_X, 200000281, '',
            c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_x
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
            ID_TABRADIO_Y, 200000281, '',
            c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_y
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
            ID_TABRADIO_Z, 200000281, '',
            c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, CONTROL_WIDTH, 0, bc_z
        )
        self.gadget_z.SetData(1)
        
        self.GroupEnd()
        self.AddSeparatorH(c4d.BFH_SCALEFIT)
        
        # Buttons
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols=2)
        self.GroupBorderSpace(6, 0, 6, 8)
        self.AddButton(ID_BTN_CANCEL, c4d.BFH_SCALEFIT, name="Cancel")
        self.AddButton(ID_BTN_OK, c4d.BFH_SCALEFIT, name="OK")
        self.GroupEnd()
        return True

    def Command(self, id, msg):
        changed = False
        if id == ID_TABRADIO_X:
            self.x_mode = ("Off", "-X", "+X")[msg[c4d.BFM_ACTION_VALUE] - 1]
            changed = True
        elif id == ID_TABRADIO_Y:
            self.y_mode = ("Off", "-Y", "+Y")[msg[c4d.BFM_ACTION_VALUE] - 1]
            changed = True
        elif id == ID_TABRADIO_Z:
            self.z_mode = ("Off", "-Z", "+Z")[msg[c4d.BFM_ACTION_VALUE] - 1]
            changed = True
        elif id == 1001: # Axis Space
            self.axis_space = "World" if msg[c4d.BFM_ACTION_VALUE] == 1 else "Object"
            changed = True
        elif id == ID_BTN_OK:
            self._finalise()
            self.Close()
        elif id == ID_BTN_CANCEL:
            self._cancelled = True
            for obj in self.selected:
                _restore_object(obj, self.snapshots[obj])
            c4d.EventAdd()
            self.Close()
            
        if changed:
            self._apply_current()
        return True

    def _apply_current(self):
        """Live updates the viewport by restoring original snapshots and running transformations."""
        for obj in self.selected:
            # Revert to clean state so rotations do not compound on every click
            _restore_object(obj, self.snapshots[obj])
            
            # Apply active axes options sequentially
            for mode in (self.x_mode, self.y_mode, self.z_mode):
                axis, angle_deg = mode_to_axis_angle(mode)
                if axis is not None:
                    process_object(obj, axis=axis, angle_deg=angle_deg)
        c4d.EventAdd()

    def _finalise(self):
        """Wrap the current live state into a proper undo step."""
        for obj in self.selected:
            _restore_object(obj, self.snapshots[obj])
        operations = []
        for mode in (self.x_mode, self.y_mode, self.z_mode):
            axis, angle_deg = mode_to_axis_angle(mode)
            if axis is not None:
                operations.append((axis, angle_deg))
        if not operations:
            c4d.EventAdd()
            return
        self.doc.StartUndo()
        for obj in self.selected:
            self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            for axis, angle_deg in operations:
                process_object(obj, axis=axis, angle_deg=angle_deg)
        self.doc.EndUndo()
        c4d.EventAdd()
        axes_str = ", ".join(f"{a} {d:+.0f}°" for a, d in operations)
        print(f"Done: [{axes_str}] applied to {len(self.selected)} object(s).")

    def Message(self, msg, result):
        bc = c4d.BaseContainer()
        # Adjusted line breaks to ensure correct Python indentation/continuation syntax
        if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc) and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(ID_BTN_OK, {})
            return True
        if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc) and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(ID_BTN_CANCEL, {})
            return True
        return super().Message(msg, result)

# ─── ENTRY POINT ──────────────────────────────────────────────────────────────
_dlg = None
def main():
    global _dlg
    doc = c4d.documents.GetActiveDocument()
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not selected:
        c4d.gui.MessageDialog("Please select at least one object.")
        return
    snapshots = {obj: _snapshot_object(obj) for obj in selected}
    _dlg = AxisOrientationDialog(doc, selected, snapshots)
    _dlg.Open(c4d.DLG_TYPE_ASYNC, pluginid=ID_DLG_AXIS_FIX)

if __name__ == "__main__":
    main()