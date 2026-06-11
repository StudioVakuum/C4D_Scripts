"""
SV Create Centered Spline

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Creates a spline through the center points of selected edge loops.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d
from collections import defaultdict


SPLINE_TYPE = c4d.SPLINETYPE_LINEAR   # LINEAR / BEZIER / BSPLINE


def get_edge_point_pairs(obj):
    all_polys = obj.GetAllPolygons()
    result = {}
    for poly_idx, poly in enumerate(all_polys):
        is_tri = (poly.c == poly.d)
        if is_tri:
            edges = [(poly.a, poly.b), (poly.b, poly.c), (poly.c, poly.a), None]
        else:
            edges = [
                (poly.a, poly.b),
                (poly.b, poly.c),
                (poly.c, poly.d),
                (poly.d, poly.a),
            ]
        for local_idx, pair in enumerate(edges):
            if pair is not None:
                result[poly_idx * 4 + local_idx] = pair
    return result


def group_into_loops(selected_edge_pairs):
    adj = defaultdict(set)
    for a, b in selected_edge_pairs.values():
        adj[a].add(b)
        adj[b].add(a)

    visited = set()
    loops = []

    for start in adj.keys():
        if start in visited:
            continue
        loop_pts = set()
        stack = [start]
        while stack:
            pt = stack.pop()
            if pt in visited:
                continue
            visited.add(pt)
            loop_pts.add(pt)
            for nb in adj[pt]:
                if nb not in visited:
                    stack.append(nb)
        if loop_pts:
            loops.append(loop_pts)

    return loops


def nearest_neighbour_sort(centers):
    """
    Sort centers by nearest-neighbour chaining.
    Picks the endpoint that gives the longest straight start as the origin,
    then always walks to the closest unvisited center.
    Works correctly on U-turns, S-curves, helixes, etc.
    """
    if len(centers) < 2:
        return centers

    remaining = list(centers)

    # Try every point as a starting candidate, pick the one whose
    # first step is longest (i.e. an end cap, not a middle point)
    def chain_from(start_idx):
        pts = list(remaining)
        chain = [pts.pop(start_idx)]
        while pts:
            last = chain[-1]
            closest_idx = min(range(len(pts)), key=lambda i: (pts[i] - last).GetLength())
            chain.append(pts.pop(closest_idx))
        return chain

    # Use the point that is farthest from the overall centroid as start
    centroid = sum(centers, c4d.Vector(0, 0, 0)) / len(centers)
    start_idx = max(range(len(remaining)), key=lambda i: (remaining[i] - centroid).GetLength())

    return chain_from(start_idx)


def main():
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetActiveObject()

    if obj is None or obj.GetType() != c4d.Opolygon:
        c4d.gui.MessageDialog("Select a polygon object in Edge mode with loops selected.")
        return

    all_points = obj.GetAllPoints()
    edge_sel   = obj.GetEdgeS()
    mg         = obj.GetMg()

    edge_pairs = get_edge_point_pairs(obj)
    selected   = {ei: pair for ei, pair in edge_pairs.items() if edge_sel.IsSelected(ei)}

    if not selected:
        c4d.gui.MessageDialog("No edges selected.")
        return

    loops   = group_into_loops(selected)
    centers = []

    for loop_pts in loops:
        total = c4d.Vector(0, 0, 0)
        for pi in loop_pts:
            total += all_points[pi]
        centers.append(mg * (total / len(loop_pts)))

    centers = nearest_neighbour_sort(centers)

    spline = c4d.SplineObject(len(centers), SPLINE_TYPE)
    spline.SetName("{} – Center Spline".format(obj.GetName()))
    for i, pt in enumerate(centers):
        spline.SetPoint(i, pt)
    spline.Message(c4d.MSG_UPDATE)

    doc.StartUndo()
    doc.InsertObject(spline)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, spline)
    doc.EndUndo()
    c4d.EventAdd()

    print("[Center Spline] {} points from {} loops.".format(len(centers), len(loops)))


if __name__ == "__main__":
    main()