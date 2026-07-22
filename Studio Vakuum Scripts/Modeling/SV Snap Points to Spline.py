"""
SV Snap Points to Spline

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US: Snaps selected polygon points, or the endpoints of selected
polygon edges, to the closest position on one or more selected splines.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d


# The curve is sampled first and the best intervals are then refined on the
# actual spline. Raising these values improves precision on unusually complex
# splines at the cost of execution time.
MIN_SAMPLES_PER_SEGMENT = 32
MAX_SAMPLES_PER_SEGMENT = 512
SAMPLES_PER_LINE_VERTEX = 4
REFINE_CANDIDATE_COUNT = 6
REFINE_ITERATIONS = 20


def distance_squared(a, b):
    """Returns the squared distance between two vectors."""
    return (a - b).GetSquaredLength()


def distance_to_line_segment_squared(point, a, b):
    """Returns the squared distance from point to the finite line a-b."""
    ab = b - a
    length_squared = ab.GetSquaredLength()
    if length_squared <= 1e-20:
        return distance_squared(point, a)

    offset = max(0.0, min(1.0, (point - a).Dot(ab) / length_squared))
    return distance_squared(point, a + ab * offset)


class SplineSampler:
    """Samples and queries one spline in global coordinates."""

    def __init__(self, spline):
        self.spline = spline
        self.helper = c4d.utils.SplineHelp()
        self.segments = []

        flags = (
            c4d.SPLINEHELPFLAGS_GLOBALSPACE
            | c4d.SPLINEHELPFLAGS_CONTINUECURVE
            | c4d.SPLINEHELPFLAGS_USERDEFORMERS
        )
        if not self.helper.InitSplineWith(spline, flags):
            raise RuntimeError(
                'Could not initialize spline "{}".'.format(spline.GetName())
            )

        for segment_index in range(self.helper.GetSegmentCount()):
            try:
                vertex_count = self.helper.GetVertexCount(segment_index)
            except (IndexError, RuntimeError):
                vertex_count = MIN_SAMPLES_PER_SEGMENT

            sample_count = max(
                MIN_SAMPLES_PER_SEGMENT,
                min(
                    MAX_SAMPLES_PER_SEGMENT,
                    max(1, vertex_count) * SAMPLES_PER_LINE_VERTEX,
                ),
            )
            offsets = [i / sample_count for i in range(sample_count + 1)]
            positions = [
                self.evaluate(segment_index, offset) for offset in offsets
            ]
            self.segments.append((segment_index, offsets, positions))

        if not self.segments:
            raise RuntimeError(
                'Spline "{}" contains no usable segments.'.format(
                    spline.GetName()
                )
            )

    def evaluate(self, segment_index, offset):
        """Evaluates the spline in global space using uniform length offsets."""
        return self.helper.GetPosition(
            offset, segment_index, smooth=True, realoffset=True
        )

    def refine_interval(self, target, segment_index, lower, upper):
        """Finds a local distance minimum inside one sampled interval."""
        ratio = 0.6180339887498949
        x1 = upper - (upper - lower) * ratio
        x2 = lower + (upper - lower) * ratio
        p1 = self.evaluate(segment_index, x1)
        p2 = self.evaluate(segment_index, x2)
        d1 = distance_squared(target, p1)
        d2 = distance_squared(target, p2)

        for _ in range(REFINE_ITERATIONS):
            if d1 <= d2:
                upper = x2
                x2, p2, d2 = x1, p1, d1
                x1 = upper - (upper - lower) * ratio
                p1 = self.evaluate(segment_index, x1)
                d1 = distance_squared(target, p1)
            else:
                lower = x1
                x1, p1, d1 = x2, p2, d2
                x2 = lower + (upper - lower) * ratio
                p2 = self.evaluate(segment_index, x2)
                d2 = distance_squared(target, p2)

        if d1 <= d2:
            return p1, d1
        return p2, d2

    def closest_point(self, target):
        """Returns the closest global spline position to target."""
        best_position = None
        best_distance = float("inf")

        for segment_index, offsets, positions in self.segments:
            interval_candidates = []

            for index in range(len(positions) - 1):
                chord_distance = distance_to_line_segment_squared(
                    target, positions[index], positions[index + 1]
                )
                interval_candidates.append((chord_distance, index))

            interval_candidates.sort(key=lambda item: item[0])
            for _, index in interval_candidates[:REFINE_CANDIDATE_COUNT]:
                position, dist = self.refine_interval(
                    target,
                    segment_index,
                    offsets[index],
                    offsets[index + 1],
                )
                if dist < best_distance:
                    best_position = position
                    best_distance = dist

            # Explicit endpoint checks protect open splines whose closest
            # position is exactly at the beginning or end.
            for position in (positions[0], positions[-1]):
                dist = distance_squared(target, position)
                if dist < best_distance:
                    best_position = position
                    best_distance = dist

        return best_position, best_distance


def is_spline_object(obj):
    """Returns True for editable and parametric spline objects."""
    return bool(obj.GetInfo() & c4d.OBJECT_ISSPLINE)


def get_input_objects(doc):
    """Returns one selected polygon object and all selected spline objects."""
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    polygon_objects = [obj for obj in selection if obj.CheckType(c4d.Opolygon)]
    spline_objects = [obj for obj in selection if is_spline_object(obj)]

    if len(polygon_objects) != 1:
        raise ValueError(
            "Select exactly one polygon object and at least one spline."
        )
    if not spline_objects:
        raise ValueError(
            "Select exactly one polygon object and at least one spline."
        )

    return polygon_objects[0], spline_objects


def get_edge_point_indices(polygon_object):
    """Returns the unique point indices used by all selected polygon edges."""
    edge_selection = polygon_object.GetEdgeS()
    result = set()

    for polygon_index, polygon in enumerate(polygon_object.GetAllPolygons()):
        if polygon.IsTriangle():
            edges = (
                (polygon.a, polygon.b),
                (polygon.b, polygon.c),
                (polygon.c, polygon.a),
            )
        else:
            edges = (
                (polygon.a, polygon.b),
                (polygon.b, polygon.c),
                (polygon.c, polygon.d),
                (polygon.d, polygon.a),
            )

        for local_edge_index, point_pair in enumerate(edges):
            edge_index = polygon_index * 4 + local_edge_index
            if edge_selection.IsSelected(edge_index):
                result.update(point_pair)

    return result


def get_selected_point_indices(doc, polygon_object):
    """Resolves the active point or edge component selection to point IDs."""
    point_selection = polygon_object.GetPointS()
    point_indices = {
        index
        for index in range(polygon_object.GetPointCount())
        if point_selection.IsSelected(index)
    }
    edge_point_indices = get_edge_point_indices(polygon_object)

    # Point and edge selections are stored independently by Cinema 4D. Honor
    # the current modeling mode so a stale selection from another mode does
    # not unexpectedly move additional points.
    mode = doc.GetMode()
    if mode == c4d.Medges:
        return sorted(edge_point_indices), "edge"
    if mode == c4d.Mpoints:
        return sorted(point_indices), "point"

    # Outside a component mode, accept whichever stored selection is present.
    # When both are present, using their union is the least surprising result.
    combined_indices = point_indices | edge_point_indices
    if point_indices and edge_point_indices:
        source = "point and edge"
    elif edge_point_indices:
        source = "edge"
    else:
        source = "point"
    return sorted(combined_indices), source


def main():
    doc = c4d.documents.GetActiveDocument()

    try:
        polygon_object, spline_objects = get_input_objects(doc)
    except ValueError as error:
        c4d.gui.MessageDialog(str(error))
        return

    selected_indices, selection_source = get_selected_point_indices(
        doc, polygon_object
    )
    if not selected_indices:
        c4d.gui.MessageDialog(
            "The polygon object has no selected points or edges in the "
            "active component mode. Select points or edges and run the "
            "script again."
        )
        return

    samplers = []
    errors = []
    for spline in spline_objects:
        try:
            samplers.append(SplineSampler(spline))
        except RuntimeError as error:
            errors.append(str(error))

    if not samplers:
        c4d.gui.MessageDialog(
            "None of the selected splines could be evaluated.\n\n"
            + "\n".join(errors)
        )
        return

    points = polygon_object.GetAllPoints()
    object_matrix = polygon_object.GetMg()
    inverse_object_matrix = ~object_matrix

    doc.StartUndo()
    try:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, polygon_object)

        for point_index in selected_indices:
            global_point = object_matrix * points[point_index]
            closest_position = None
            closest_distance = float("inf")

            for sampler in samplers:
                position, dist = sampler.closest_point(global_point)
                if position is not None and dist < closest_distance:
                    closest_position = position
                    closest_distance = dist

            if closest_position is not None:
                points[point_index] = inverse_object_matrix * closest_position

        polygon_object.SetAllPoints(points)
        polygon_object.Message(c4d.MSG_UPDATE)
    finally:
        doc.EndUndo()

    c4d.EventAdd()

    print(
        "[Snap Points to Spline] Snapped {} point{} from the {} selection "
        "on '{}' to {} spline{}."
        .format(
            len(selected_indices),
            "" if len(selected_indices) == 1 else "s",
            selection_source,
            polygon_object.GetName(),
            len(samplers),
            "" if len(samplers) == 1 else "s",
        )
    )

    if errors:
        c4d.gui.MessageDialog(
            "The points were snapped, but some splines were skipped:\n\n"
            + "\n".join(errors)
        )


if __name__ == "__main__":
    main()
