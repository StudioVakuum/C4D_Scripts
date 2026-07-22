"""
SV Quad Circle

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Creates a circular quad circle of selected points

Written for Maxon Cinema 4D 2026.3.1
Python version 3.11.4
"""

import c4d
from c4d import gui
import math
import sys

EDGE_FRACTION = 0.35
CURVATURE_STRENGTH = 1.0
CURVATURE_SLIDER_MAX = 1.0
REQUIRE_FOUR_QUADS = True

EPSILON = 0.000001
RELATIVE_SLIDER_MIN = 0.0
RELATIVE_SLIDER_MAX = 1.0

ID_EXACT_RADIUS = 1000
ID_VALUE = 1001
ID_CURVATURE = 1002
ID_CANCEL = 1003
ID_CREATE = 1004

ACTIVE_DIALOG = None


def poly_vertices(poly):
    if poly.c == poly.d:
        return [poly.a, poly.b, poly.c]
    return [poly.a, poly.b, poly.c, poly.d]


def make_tri(a, b, c):
    return c4d.CPolygon(a, b, c, c)


def make_quad(a, b, c, d):
    return c4d.CPolygon(a, b, c, d)


def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
    return c4d.Vector(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    )


def length(v):
    return math.sqrt(max(0.0, dot(v, v)))


def normalized(v):
    size = length(v)
    if size < EPSILON:
        return c4d.Vector(0.0, 0.0, 0.0)
    return v * (1.0 / size)


def project_to_plane(v, normal):
    return v - normal * dot(v, normal)


def face_normal(points, poly):
    verts = poly_vertices(poly)
    if len(verts) < 3:
        return c4d.Vector(0.0, 0.0, 0.0)

    p0 = points[verts[0]]
    p1 = points[verts[1]]
    p2 = points[verts[2]]
    return cross(p1 - p0, p2 - p0)


def average_normal(points, polys, face_indices):
    normal = c4d.Vector(0.0, 0.0, 0.0)

    for poly_index in face_indices:
        n = face_normal(points, polys[poly_index])
        if length(n) < EPSILON:
            continue

        if length(normal) > EPSILON and dot(normal, n) < 0.0:
            n = n * -1.0
        normal += n

    return normalized(normal)


def selected_point_ids(obj):
    sel = obj.GetPointS()
    return [i for i in range(obj.GetPointCount()) if sel.IsSelected(i)]


def message(text):
    gui.MessageDialog(text)
    return False


class HoleSizeDialog(gui.GeDialog):
    def __init__(self, session):
        super(HoleSizeDialog, self).__init__()
        self.session = session
        self._exact_radius = False

    def SetRelativePercent(self, value):
        self.SetFloat(
            ID_VALUE,
            value * 0.01,
            RELATIVE_SLIDER_MIN,
            RELATIVE_SLIDER_MAX,
            0.01,
            c4d.FORMAT_PERCENT,
            EPSILON,
            sys.float_info.max,
        )

    def SetExactRadius(self, value):
        self.SetFloat(
            ID_VALUE,
            value,
            EPSILON,
            100.0,
            1.0,
            c4d.FORMAT_METER,
            EPSILON,
            sys.float_info.max,
        )

    def SetCurvatureStrength(self, value):
        self.SetFloat(
            ID_CURVATURE,
            value,
            0.0,
            CURVATURE_SLIDER_MAX,
            0.01,
            c4d.FORMAT_PERCENT,
            0.0,
            sys.float_info.max,
        )

    def CreateLayout(self):
        self.SetTitle("Circular Hole Topology")

        self.GroupBegin(0, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, 0)
        self.GroupBorderSpace(6, 6, 6, 6)


        self.AddCheckbox(
            ID_EXACT_RADIUS,
            c4d.BFH_SCALEFIT,
            0,
            0,
            "Exact Radius",
        )

        self.GroupBegin(0, c4d.BFH_SCALEFIT, 2, 0)
        self.AddStaticText(0, c4d.BFH_LEFT | c4d.BFV_CENTER, 90, 0, "Radius")
        self.AddEditSlider(ID_VALUE, c4d.BFH_SCALEFIT | c4d.BFV_CENTER, 60, 0)
        self.GroupEnd()

        self.GroupBegin(0, c4d.BFH_SCALEFIT, 2, 0)
        self.AddStaticText(0, c4d.BFH_LEFT | c4d.BFV_CENTER, 90, 0, "Curvature")
        self.AddEditSlider(ID_CURVATURE, c4d.BFH_SCALEFIT | c4d.BFV_CENTER, 60, 0)
        self.GroupEnd()

        self.AddStaticText(0, c4d.BFH_SCALEFIT, 0, 8, "")
        self.GroupBegin(0, c4d.BFH_LEFT, 2, 1)
        self.AddButton(ID_CANCEL, c4d.BFH_LEFT, 90, 0, "Cancel")
        self.AddButton(
            ID_CREATE,
            c4d.BFH_LEFT,
            90,
            0,
            "Apply",
        )
        self.GroupEnd()

        self.GroupEnd()
        return True

    def InitValues(self):
        self.SetBool(ID_EXACT_RADIUS, False)
        self.SetRelativePercent(EDGE_FRACTION * 100.0)
        self.SetCurvatureStrength(CURVATURE_STRENGTH)
        self.UpdateControls()
        self.Preview()
        return True

    def UpdateControls(self):
        exact_radius = bool(self.GetBool(ID_EXACT_RADIUS))

        if exact_radius != self._exact_radius:
            if exact_radius:
                self.SetExactRadius(1.0)
            else:
                self.SetRelativePercent(EDGE_FRACTION * 100.0)

        self._exact_radius = exact_radius

    def BuildResult(self):
        exact_radius = bool(self.GetBool(ID_EXACT_RADIUS))
        value = self.GetFloat(ID_VALUE)
        curvature_strength = self.GetFloat(ID_CURVATURE)

        if value is None:
            return None, "Enter a radius value."
        if curvature_strength is None:
            return None, "Enter a curvature value."
        if curvature_strength < 0.0:
            return None, "Use a curvature value of 0% or greater."

        if exact_radius:
            if value <= EPSILON:
                return None, "Use an exact radius greater than 0."
            return {
                "mode": "absolute",
                "radius": value,
                "curvature_strength": curvature_strength,
            }, None

        if value <= 0.0:
            return None, "Use a relative value greater than 0%."

        return {
            "mode": "relative",
            "fraction": value,
            "curvature_strength": curvature_strength,
        }, None

    def Command(self, control_id, msg):
        global ACTIVE_DIALOG
        if control_id == ID_EXACT_RADIUS:
            self.UpdateControls()
            self.Preview()
            return True

        if control_id == ID_VALUE or control_id == ID_CURVATURE:
            self.Preview()
            return True

        if control_id == ID_CANCEL:
            self.session.Cancel()
            if ACTIVE_DIALOG is self:
                ACTIVE_DIALOG = None
            self.Close()
            return True

        if control_id == ID_CREATE:
            result, error = self.BuildResult()
            if error:
                gui.MessageDialog(error)
                return True

            if self.session.Commit(result):
                if ACTIVE_DIALOG is self:
                    ACTIVE_DIALOG = None
                self.Close()
            return True

        return True

    def Preview(self):
        result, error = self.BuildResult()
        if error is None:
            self.session.Preview(result)

    def AskClose(self):
        global ACTIVE_DIALOG
        self.session.Cancel()
        if ACTIVE_DIALOG is self:
            ACTIVE_DIALOG = None
        return False


def selected_ids(selection, count):
    return [i for i in range(count) if selection.IsSelected(i)]


def collect_patch(points, polys, center_id, hole_size):
    face_data = {}
    neighbor_ids = set()

    for poly_index, poly in enumerate(polys):
        verts = poly_vertices(poly)
        if center_id not in verts:
            continue

        if len(verts) != 4:
            return None, "must be surrounded only by quads."

        k = verts.index(center_id)
        next_id = verts[(k + 1) % 4]
        opposite_id = verts[(k + 2) % 4]
        prev_id = verts[(k - 1) % 4]

        if len(set([center_id, next_id, opposite_id, prev_id])) != 4:
            return None, "touches a degenerate polygon."

        face_data[poly_index] = {
            "next": next_id,
            "opposite": opposite_id,
            "prev": prev_id,
        }
        neighbor_ids.add(next_id)
        neighbor_ids.add(prev_id)

    if not face_data:
        return None, "is not used by any polygon."

    if REQUIRE_FOUR_QUADS and (len(face_data) != 4 or len(neighbor_ids) != 4):
        return None, (
            "must be one interior quad-grid point with exactly four "
            "surrounding quads."
        )

    opposite_neighbor = {}
    if len(neighbor_ids) == 4:
        neighbor_adjacency = {point_id: set() for point_id in neighbor_ids}
        for data in face_data.values():
            neighbor_adjacency[data["next"]].add(data["prev"])
            neighbor_adjacency[data["prev"]].add(data["next"])

        for point_id in neighbor_ids:
            across = neighbor_ids - set([point_id]) - neighbor_adjacency[point_id]
            if len(across) != 1:
                return None, "does not have a usable four-direction quad grid."
            opposite_neighbor[point_id] = across.pop()

    center_pos = points[center_id]
    normal = average_normal(points, polys, face_data.keys())
    if length(normal) < EPSILON:
        return None, "does not have a stable local surface normal."

    neighbor_lengths = {}

    for point_id in sorted(neighbor_ids):
        projected = project_to_plane(points[point_id] - center_pos, normal)
        projected_length = length(projected)
        if projected_length < EPSILON:
            return None, "has an invalid local edge direction."
        neighbor_lengths[point_id] = projected_length

    min_neighbor_length = min(neighbor_lengths.values())
    if hole_size["mode"] == "absolute":
        ring_radius = hole_size["radius"]
    else:
        ring_radius = min_neighbor_length * hole_size["fraction"]

    if ring_radius < EPSILON:
        return None, "does not have a usable circle radius."

    return {
        "center": center_id,
        "center_pos": center_pos,
        "face_data": face_data,
        "neighbor_ids": neighbor_ids,
        "opposite_neighbor": opposite_neighbor,
        "curvature_strength": hole_size["curvature_strength"],
        "edge_fraction": {
            point_id: ring_radius / neighbor_lengths[point_id]
            for point_id in neighbor_ids
        },
        "edge_point": {},
        "corner_point": {},
    }, None


def add_patch_points(points, patch, new_points):
    center_pos = patch["center_pos"]

    for point_id in sorted(patch["neighbor_ids"]):
        patch["edge_point"][point_id] = len(new_points)
        fraction = patch["edge_fraction"][point_id]
        new_points.append(
            center_pos
            + (points[point_id] - center_pos) * fraction
            + arc_correction(points, patch, point_id, fraction)
        )

    for poly_index, data in sorted(patch["face_data"].items()):
        patch["corner_point"][poly_index] = len(new_points)
        next_fraction = patch["edge_fraction"][data["next"]] / math.sqrt(2.0)
        prev_fraction = patch["edge_fraction"][data["prev"]] / math.sqrt(2.0)
        next_pos = points[data["next"]]
        opposite_pos = points[data["opposite"]]
        prev_pos = points[data["prev"]]
        new_points.append(
            center_pos * ((1.0 - next_fraction) * (1.0 - prev_fraction))
            + next_pos * (next_fraction * (1.0 - prev_fraction))
            + opposite_pos * (next_fraction * prev_fraction)
            + prev_pos * ((1.0 - next_fraction) * prev_fraction)
            + arc_correction(points, patch, data["next"], next_fraction)
            + arc_correction(points, patch, data["prev"], prev_fraction)
        )


def arc_correction(points, patch, point_id, fraction):
    opposite_id = patch["opposite_neighbor"].get(point_id)
    if opposite_id is None:
        return c4d.Vector(0.0, 0.0, 0.0)

    center_pos = patch["center_pos"]
    second_derivative = points[point_id] - center_pos * 2.0 + points[opposite_id]
    strength = patch["curvature_strength"]
    return second_derivative * (
        strength * 0.5 * fraction * fraction * (fraction - 1.0)
    )


def build_mesh(old_points, old_polys, picked, hole_size):
    patches = []
    polygon_owner = {}

    for center_id in picked:
        patch, error = collect_patch(old_points, old_polys, center_id, hole_size)
        if error:
            return None, "Selected point %d %s" % (center_id, error)

        for poly_index in patch["face_data"].keys():
            owner = polygon_owner.get(poly_index)
            if owner is not None:
                return None, (
                    "Selected point rings overlap: points %d and %d share a "
                    "polygon. Select points farther apart." % (owner, center_id)
                )
            polygon_owner[poly_index] = center_id

        patches.append(patch)

    new_points = list(old_points)
    patch_by_polygon = {}

    for patch in patches:
        add_patch_points(old_points, patch, new_points)
        for poly_index in patch["face_data"].keys():
            patch_by_polygon[poly_index] = patch

    new_polys = []
    ring_edge_refs = []
    inner_polygon_refs = []

    for poly_index, poly in enumerate(old_polys):
        patch = patch_by_polygon.get(poly_index)
        if patch is None:
            new_polys.append(poly)
            continue

        data = patch["face_data"][poly_index]
        center_id = patch["center"]
        next_id = data["next"]
        opposite_id = data["opposite"]
        prev_id = data["prev"]

        edge_next = patch["edge_point"][next_id]
        edge_prev = patch["edge_point"][prev_id]
        corner = patch["corner_point"][poly_index]

        inner_index = len(new_polys)
        new_polys.append(make_quad(center_id, edge_next, corner, edge_prev))
        inner_polygon_refs.append(inner_index)
        ring_edge_refs.append((inner_index, 1))
        ring_edge_refs.append((inner_index, 2))

        new_polys.append(make_quad(edge_next, next_id, opposite_id, corner))
        new_polys.append(make_quad(corner, opposite_id, prev_id, edge_prev))

    return (new_points, new_polys, ring_edge_refs, inner_polygon_refs), None


class OctagonPreviewSession(object):
    def __init__(self, document, obj, picked):
        self.doc = document
        self.obj = obj
        self.picked = picked
        self.old_points = list(obj.GetAllPoints())
        self.old_polys = list(obj.GetAllPolygons())
        self.old_point_selection = selected_ids(obj.GetPointS(), obj.GetPointCount())
        self.old_polygon_selection = selected_ids(obj.GetPolygonS(), obj.GetPolygonCount())
        self.old_edge_selection = selected_ids(
            obj.GetEdgeS(), obj.GetPolygonCount() * 4
        )
        try:
            self.old_mode = document.GetMode()
        except Exception:
            self.old_mode = None
        self.closed = False
        self.committed = False

    def RestoreOriginal(self):
        self.obj.ResizeObject(len(self.old_points), len(self.old_polys))
        self.obj.SetAllPoints(self.old_points)
        for index, poly in enumerate(self.old_polys):
            self.obj.SetPolygon(index, poly)

        self.obj.GetPointS().DeselectAll()
        self.obj.GetPolygonS().DeselectAll()
        self.obj.GetEdgeS().DeselectAll()
        for index in self.old_point_selection:
            self.obj.GetPointS().Select(index)
        for index in self.old_polygon_selection:
            self.obj.GetPolygonS().Select(index)
        for edge in self.old_edge_selection:
            self.obj.GetEdgeS().Select(edge)
        if self.old_mode is not None:
            try:
                self.doc.SetMode(self.old_mode)
            except Exception:
                pass
        self.obj.Message(c4d.MSG_UPDATE)

    def ApplyMesh(self, mesh):
        new_points, new_polys, ring_edge_refs, inner_polygon_refs = mesh
        self.obj.ResizeObject(len(new_points), len(new_polys))
        self.obj.SetAllPoints(new_points)
        for index, poly in enumerate(new_polys):
            self.obj.SetPolygon(index, poly)

        self.obj.GetPointS().DeselectAll()
        self.obj.GetPolygonS().DeselectAll()
        self.obj.GetEdgeS().DeselectAll()
        for poly_index, local_edge in ring_edge_refs:
            self.obj.GetEdgeS().Select(poly_index * 4 + local_edge)
        for poly_index in inner_polygon_refs:
            self.obj.GetPolygonS().Select(poly_index)
        try:
            self.doc.SetMode(c4d.Mpolygons)
        except Exception:
            pass
        self.obj.Message(c4d.MSG_UPDATE)

    def Preview(self, hole_size):
        if self.closed:
            return
        mesh, error = build_mesh(self.old_points, self.old_polys, self.picked, hole_size)
        if error is None:
            c4d.StopAllThreads()
            self.ApplyMesh(mesh)
            c4d.EventAdd()

    def Cancel(self):
        if self.closed:
            return
        self.RestoreOriginal()
        self.closed = True
        c4d.EventAdd()

    def Commit(self, hole_size):
        if self.closed:
            return False
        mesh, error = build_mesh(self.old_points, self.old_polys, self.picked, hole_size)
        if error:
            gui.MessageDialog(error)
            return False

        self.RestoreOriginal()
        c4d.StopAllThreads()
        self.doc.StartUndo()
        try:
            self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, self.obj)
            self.ApplyMesh(mesh)
        finally:
            self.doc.EndUndo()
        self.committed = True
        self.closed = True
        c4d.EventAdd()
        return True


def main():
    global ACTIVE_DIALOG
    obj = op

    if obj is None or not obj.CheckType(c4d.Opolygon):
        return message("Select one editable Polygon Object.")

    picked = selected_point_ids(obj)
    if not picked:
        return message("Select one or more points, then run the script.")

    if EDGE_FRACTION <= 0.0:
        return message("EDGE_FRACTION must be greater than 0.")

    if ACTIVE_DIALOG is not None:
        ACTIVE_DIALOG.Close()

    session = OctagonPreviewSession(doc, obj, picked)
    ACTIVE_DIALOG = HoleSizeDialog(session)
    if not ACTIVE_DIALOG.Open(c4d.DLG_TYPE_ASYNC, defaultw=360, defaulth=0):
        ACTIVE_DIALOG = None
        return False

    return True


if __name__ == "__main__":
    main()