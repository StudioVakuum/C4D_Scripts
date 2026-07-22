"""
SV Node MultiConnect

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Connects selected Redshift nodes to a selected target node with manual source ordering.

Written for Maxon Cinema 4D 2026.3.2 or later
Python version 3.11.4
"""

import c4d
import maxon
import re


RS_NODE_SPACE = maxon.Id("com.redshift3d.redshift4c4d.class.nodespace")
SCRIPT_CONTEXT = {
    "node_material": None,
    "space_id": None,
}

IDC_ORDER_AREA = 1000
IDC_CONNECT = 1001
IDC_CANCEL = 1002
IDC_INVERSE = 1003

USE_NATIVE_INEXCLUDE_REORDER = False

POSITION_ATTRIBUTE_IDS = (
    maxon.Id("net.maxon.node.attribute.position"),
    maxon.Id("net.maxon.node.base.position"),
    maxon.Id("net.maxon.nodes.ui.position"),
    maxon.Id("net.maxon.ui.node.position"),
    maxon.Id("net.maxon.nodegraph.node.position"),
    maxon.Id("net.maxon.nimbus.node.position"),
)

POSITION_ATTRIBUTE_KEYWORDS = (
    "position",
    "pos",
    "location",
    "view",
    "ui",
    "editor",
    "graph",
    "nimbus",
)

GRAPH_VALUE_MASKS = (
    maxon.GraphAttributeInterface.FLAGS.DIRECT
    | maxon.GraphAttributeInterface.FLAGS.META,
    maxon.GraphAttributeInterface.FLAGS.USER_STATE,
    maxon.GraphAttributeInterface.FLAGS.DIRECT,
    maxon.GraphAttributeInterface.FLAGS.META,
    maxon.GraphAttributeInterface.FLAGS.DIRECT
    | maxon.GraphAttributeInterface.FLAGS.META
    | maxon.GraphAttributeInterface.FLAGS.USER_STATE,
)

OUTPUT_NAME_PRIORITY = (
    "outcolor",
    "out_color",
    "color",
    "out",
    "shader",
    "closure",
    "result",
)


def natural_key(text):
    chunks = re.split(r"(\d+(?:[.-]\d+)*)", text.lower())
    key = []

    for chunk in chunks:
        normalized = chunk.replace("-", ".")
        try:
            key.append((0, float(normalized)))
        except ValueError:
            key.append((1, chunk))

    return key


def message(text):
    print(text)
    try:
        c4d.gui.MessageDialog(text)
    except Exception:
        pass


def as_text(value):
    if value is None:
        return ""

    try:
        text = str(value)
    except Exception:
        return ""

    if text in ("None", "<Null>", "Null"):
        return ""
    return text


def is_generated_node_name(name):
    return bool(re.match(r"^[^@\s]+@[^\s]+$", name or ""))


def texture_filename_label(node):
    try:
        filename_port = node.GetInputs().FindChild(
            "com.redshift3d.redshift4c4d.nodes.core.texturesampler.tex0"
        )
        path_port = filename_port.FindChild("path")
    except Exception:
        return ""

    try:
        if path_port is None or path_port.IsNullValue():
            return ""
    except Exception:
        pass

    for getter in (
        lambda: path_port.GetValue("effectivevalue"),
        lambda: path_port.GetPortValue(),
        lambda: path_port.GetDefaultValue(),
    ):
        try:
            value = getter()
        except Exception:
            continue

        if isinstance(value, (tuple, list)) and value:
            value = value[0]
        if value is None:
            continue

        try:
            if value.IsEmpty():
                continue
        except Exception:
            pass

        try:
            filename = as_text(value.GetName())
            if filename:
                return filename
        except Exception:
            pass

        text = as_text(value).split("?", 1)[0].rstrip("/\\")
        if text and not text.startswith("<"):
            filename = re.split(r"[/\\]", text)[-1]
            if filename:
                return filename

    return ""


def graph_is_usable(graph):
    if graph is None:
        return False

    try:
        return not graph.IsNullValue()
    except Exception:
        pass

    try:
        root = graph.GetViewRoot()
        return root is not None and root.IsValid()
    except Exception:
        return True


def get_active_redshift_graph(doc):
    mat = doc.GetActiveMaterial()
    if mat is None:
        raise RuntimeError("Please select the Redshift material that owns the selected nodes.")

    node_material = mat.GetNodeMaterialReference()
    if node_material is None:
        raise RuntimeError("The active material has no node material reference.")

    node_spaces = []

    try:
        active_space = c4d.GetActiveNodeSpaceId()
        if active_space:
            node_spaces.append(active_space)
    except Exception:
        pass

    node_spaces.append(RS_NODE_SPACE)

    seen = set()
    for space_id in node_spaces:
        key = as_text(space_id)
        if key in seen:
            continue
        seen.add(key)

        try:
            if hasattr(node_material, "HasSpace") and not node_material.HasSpace(space_id):
                continue
        except Exception:
            pass

        try:
            graph = node_material.GetGraph(space_id)
        except Exception:
            continue

        if graph_is_usable(graph):
            SCRIPT_CONTEXT["node_material"] = node_material
            SCRIPT_CONTEXT["space_id"] = space_id
            return graph

    raise RuntimeError("Could not find a Redshift node graph on the active material.")


def get_selected_true_nodes(graph):
    selected = []

    try:
        selected = maxon.GraphModelHelper.GetSelectedNodes(graph, maxon.NODE_KIND.NODE)
    except Exception:
        selected = []

    nodes = []
    for node in selected:
        try:
            if node.IsValid() and node.GetKind() == maxon.NODE_KIND.NODE:
                nodes.append(node)
        except Exception:
            pass

    return nodes


def node_label(node):
    graph_name = ""
    try:
        graph_name = as_text(node.GetValue(maxon.NODE.BASE.NAME))
        if graph_name and not is_generated_node_name(graph_name):
            return graph_name
    except Exception:
        pass

    filename = texture_filename_label(node)
    if filename:
        return filename

    try:
        base_list = get_base_list_for_node(node)
        base_list_name = as_text(base_list.GetName()) if base_list is not None else ""
        if base_list_name and not is_generated_node_name(base_list_name):
            return base_list_name
    except Exception:
        pass

    if graph_name:
        return graph_name

    try:
        return as_text(node.GetId())
    except Exception:
        return "<node>"


def port_label(port):
    try:
        name = as_text(port.GetValue(maxon.NODE.BASE.NAME))
        if name:
            return name
    except Exception:
        pass

    try:
        return as_text(port.GetId())
    except Exception:
        return "<port>"


def compact_label(label):
    return re.sub(r"[^a-z0-9]+", "", label.lower())


def value_to_xy(value, allow_text=True):
    if value is None:
        return None

    for x_name, y_name in (("x", "y"), ("X", "Y")):
        if hasattr(value, x_name) and hasattr(value, y_name):
            try:
                return float(getattr(value, x_name)), float(getattr(value, y_name))
            except Exception:
                pass

    try:
        return float(value[0]), float(value[1])
    except Exception:
        pass

    if allow_text:
        try:
            numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", str(value))
            if len(numbers) >= 2:
                return float(numbers[0]), float(numbers[1])
        except Exception:
            pass

    return None


def iter_node_values(node):
    seen = set()

    for mask in GRAPH_VALUE_MASKS:
        try:
            values = node.GetValues(mask)
        except Exception:
            continue

        for item in values:
            try:
                attr_id, value = item[0], item[1]
            except Exception:
                continue

            key = (as_text(attr_id), as_text(value))
            if key in seen:
                continue
            seen.add(key)

            yield attr_id, value


def node_position_from_values(node):
    best = None
    best_score = -1

    for attr_id, value in iter_node_values(node):
        attr_text = as_text(attr_id).lower()
        if not any(keyword in attr_text for keyword in POSITION_ATTRIBUTE_KEYWORDS):
            continue

        xy = value_to_xy(value)
        if xy is None:
            continue

        score = 0
        if "position" in attr_text:
            score += 20
        if "pos" in attr_text:
            score += 10
        if "node" in attr_text:
            score += 5
        if "ui" in attr_text or "editor" in attr_text or "view" in attr_text:
            score += 5
        if "nimbus" in attr_text:
            score += 5

        if score > best_score:
            best = xy
            best_score = score

    return best


def node_position(node):
    for attr_id in POSITION_ATTRIBUTE_IDS:
        try:
            xy = value_to_xy(node.GetValue(attr_id))
            if xy is not None:
                return xy
        except Exception:
            pass

    return node_position_from_values(node)


def get_base_list_for_node(node):
    node_material = SCRIPT_CONTEXT.get("node_material")
    space_id = SCRIPT_CONTEXT.get("space_id")

    if node_material is None or space_id is None:
        return None

    try:
        return node_material.GetBaseListForNode(space_id, node.GetPath())
    except Exception:
        return None


def looks_like_editor_xy(xy):
    if xy is None:
        return False

    x, y = xy
    if abs(x) <= 2.0 and abs(y) <= 2.0:
        return False

    return True


def iter_container_xy_candidates(container, path=(), depth=0):
    if container is None or depth > 4:
        return

    try:
        iterator = iter(container)
    except Exception:
        return

    for data_id, value in iterator:
        item_path = path + (data_id,)

        if isinstance(value, c4d.BaseContainer):
            for result in iter_container_xy_candidates(value, item_path, depth + 1):
                yield result
            continue

        xy = value_to_xy(value, allow_text=False)
        if looks_like_editor_xy(xy):
            yield item_path, xy


def base_list_position_candidates(node):
    base_list = get_base_list_for_node(node)
    if base_list is None:
        return {}

    try:
        container = base_list.GetDataInstance()
    except Exception:
        container = None

    if container is None:
        try:
            container = base_list.GetData()
        except Exception:
            container = None

    return dict(iter_container_xy_candidates(container))


def choose_shared_position_key(nodes):
    per_node = {node: base_list_position_candidates(node) for node in nodes}
    keys = set()

    for candidates in per_node.values():
        keys.update(candidates.keys())

    best = None
    best_score = None

    for key in keys:
        values = [
            candidates[key]
            for candidates in per_node.values()
            if key in candidates
        ]
        if len(values) < max(2, len(nodes) // 2):
            continue

        xs = [xy[0] for xy in values]
        ys = [xy[1] for xy in values]
        y_range = max(ys) - min(ys)
        x_range = max(xs) - min(xs)

        if y_range <= 2.0:
            continue

        score = (len(values), y_range - (x_range * 0.05))
        if best_score is None or score > best_score:
            best = key
            best_score = score

    if best is None:
        return {}

    return {
        node: candidates[best]
        for node, candidates in per_node.items()
        if best in candidates
    }


def visual_position_map(nodes):
    direct_positions = {
        node: position
        for node in nodes
        for position in [node_position(node)]
        if position is not None
    }

    if len(direct_positions) >= 2:
        ys = [position[1] for position in direct_positions.values()]
        if max(ys) - min(ys) > 2.0:
            return direct_positions

    return choose_shared_position_key(nodes)


def direct_ports(port_list, kind):
    try:
        if port_list is None or not port_list.IsValid():
            return []
    except Exception:
        return []

    try:
        return [port for port in port_list.GetChildren(mask=kind) if port.IsValid()]
    except Exception:
        return []


def input_ports(node):
    try:
        return direct_ports(node.GetInputs(), maxon.NODE_KIND.INPORT)
    except Exception:
        return []


def output_ports(node):
    try:
        return direct_ports(node.GetOutputs(), maxon.NODE_KIND.OUTPORT)
    except Exception:
        return []


def has_incoming_connection(port):
    try:
        return bool(port.GetConnections(maxon.PORT_DIR.INPUT))
    except Exception:
        pass

    try:
        return bool(maxon.GraphModelHelper.GetDirectPredecessors(port, maxon.NODE_KIND.OUTPORT))
    except Exception:
        return False


def free_input_ports(node):
    return [port for port in input_ports(node) if not has_incoming_connection(port)]


def shader_switch_input_rank(port):
    label = port_label(port)
    compact = compact_label(label)

    if compact in ("shaderselector", "selector"):
        return 0

    match = re.search(r"shader\D*(\d+)$", label.lower())
    if match:
        return int(match.group(1)) + 1

    return None


def ranked_shader_switch_input_ports(node, only_free=True):
    all_ports = input_ports(node)
    free_ports = set(free_input_ports(node)) if only_free else set(all_ports)

    ranked = []
    used_ports = set()

    for port in all_ports:
        if port not in free_ports:
            continue

        rank = shader_switch_input_rank(port)
        if rank is None:
            continue

        ranked.append((rank, port))
        used_ports.add(port)

    if not ranked:
        label = compact_label(node_label(node))
        if "shaderswitch" in label or ("shader" in label and "switch" in label):
            return [
                (index, port)
                for index, port in enumerate(all_ports)
                if port in free_ports
            ]

    if ranked:
        used_ranks = {rank for rank, _ in ranked}
        if 0 not in used_ranks and all_ports:
            first_port = all_ports[0]
            if first_port in free_ports and first_port not in used_ports:
                ranked.append((0, first_port))
                used_ports.add(first_port)

        shader_rank = 1
        for port in all_ports[1:]:
            if port not in free_ports or port in used_ports:
                continue
            while shader_rank in used_ranks:
                shader_rank += 1
            ranked.append((shader_rank, port))
            used_ranks.add(shader_rank)
            used_ports.add(port)
            shader_rank += 1

    return sorted(ranked, key=lambda item: item[0])


def shader_switch_input_ports(node, only_free=True):
    return [port for _, port in ranked_shader_switch_input_ports(node, only_free=only_free)]


def unique_ports(ports):
    result = []
    seen = set()

    for port in ports:
        if port in seen:
            continue
        result.append(port)
        seen.add(port)

    return result


def input_port_indices(node):
    return {port: index for index, port in enumerate(input_ports(node))}


def shader_slot_candidate_ports(target, available_inputs):
    ranked = []
    indices = input_port_indices(target)

    for port in available_inputs:
        rank = shader_switch_input_rank(port)
        if rank is not None and rank > 0:
            ranked.append((rank, indices.get(port, 9999), port))

    if ranked:
        return [port for _, _, port in sorted(ranked)]

    label = compact_label(node_label(target))
    if "shaderswitch" in label or ("shader" in label and "switch" in label):
        return sorted(available_inputs, key=lambda port: indices.get(port, 9999))[1:]

    return []


def selector_candidate_ports(target, available_inputs):
    all_ports = input_ports(target)
    indices = input_port_indices(target)
    shader_ports = shader_slot_candidate_ports(target, available_inputs)
    shader_indices = [indices[port] for port in shader_ports if port in indices]
    first_shader_index = min(shader_indices) if shader_indices else None

    named_selector = []
    before_shader = []
    non_shader = []

    for port in available_inputs:
        rank = shader_switch_input_rank(port)
        index = indices.get(port, 9999)

        if rank == 0:
            named_selector.append(port)
        elif first_shader_index is not None and index < first_shader_index:
            before_shader.append(port)
        elif port not in shader_ports:
            non_shader.append(port)

    return unique_ports(
        sorted(named_selector, key=lambda port: indices.get(port, 9999))
        + sorted(before_shader, key=lambda port: indices.get(port, 9999))
        + sorted(non_shader, key=lambda port: indices.get(port, 9999))
        + sorted(available_inputs, key=lambda port: indices.get(port, 9999))
    )


def shader_switch_score(node):
    label = compact_label(node_label(node))
    ports = shader_switch_input_ports(node, only_free=False)
    ranks = {shader_switch_input_rank(port) for port in ports}

    score = 0
    if "shaderswitch" in label or ("shader" in label and "switch" in label):
        score += 1000
    if 0 in ranks:
        score += 100
    score += 10 * len([rank for rank in ranks if rank and rank > 0])

    return score


def output_score(port):
    label = port_label(port).replace(" ", "").lower()

    for index, token in enumerate(OUTPUT_NAME_PRIORITY):
        if token in label:
            return index

    return len(OUTPUT_NAME_PRIORITY)


def first_output_port(node):
    ports = output_ports(node)
    if not ports:
        return None

    return sorted(ports, key=lambda port: (output_score(port), port_label(port).lower()))[0]


def source_output_candidates(node):
    ports = output_ports(node)
    if not ports:
        return []

    first = first_output_port(node)
    return unique_ports([first] + sorted(ports, key=lambda port: (output_score(port), port_label(port).lower())))


def is_selector_source(node, source_output=None):
    label = compact_label(node_label(node))
    output = source_output if source_output is not None else first_output_port(node)
    output_label = compact_label(port_label(output)) if output is not None else ""

    return (
        "integer" in label
        or "userdata" in label
        or output_label in ("out", "outvalue", "value", "index", "selector")
    )


def is_shader_source(source_output):
    label = compact_label(port_label(source_output))
    return any(token in label for token in ("outcolor", "color", "outclosure", "closure", "shader"))


def choose_target_node(nodes):
    shader_switch_candidates = [(shader_switch_score(node), node) for node in nodes]
    best_score, best_node = max(shader_switch_candidates, key=lambda item: item[0])
    if best_score >= 120:
        return best_node

    positioned = [(node, node_position(node)) for node in nodes]
    if any(pos is not None for _, pos in positioned):
        return max(
            positioned,
            key=lambda item: (
                item[1][0] if item[1] is not None else float("-inf"),
                len(free_input_ports(item[0])),
            ),
        )[0]

    return max(nodes, key=lambda node: (len(free_input_ports(node)), len(input_ports(node))))


def source_fallback_key(node):
    label = node_label(node)
    output = first_output_port(node)

    return (0 if is_selector_source(node, output) else 1, natural_key(label))


def sort_sources(nodes):
    positions = visual_position_map(nodes)
    if positions:
        return [
            node
            for node in sorted(
                nodes,
                key=lambda item: (
                    positions[item][1] if item in positions else float("inf"),
                    positions[item][0] if item in positions else float("inf"),
                    node_label(item).lower(),
                ),
            )
        ]

    return sorted(nodes, key=source_fallback_key)


def has_visual_source_positions(nodes):
    return bool(visual_position_map(nodes))


def source_order_label(index, node):
    return "Shader %d | %s" % (index, node_label(node))


def split_source_types(sources):
    selector_sources = []
    shader_sources = []
    other_sources = []

    for source in sources:
        output = first_output_port(source)
        if output is None:
            other_sources.append(source)
        elif is_selector_source(source, output) and not is_shader_source(output):
            selector_sources.append(source)
        elif is_shader_source(output):
            shader_sources.append(source)
        else:
            other_sources.append(source)

    return selector_sources, shader_sources, other_sources


class ShaderSourceOrderArea(c4d.gui.GeUserArea):
    HEADER_HEIGHT = 30
    ROW_HEIGHT = 32
    ROW_GAP = 4
    PAD_X = 9
    HANDLE_WIDTH = 19
    SLOT_LABEL_WIDTH = 68

    def __init__(self, shader_sources):
        super(ShaderSourceOrderArea, self).__init__()
        self.sources = list(shader_sources)
        self.selected_index = 0 if self.sources else -1
        self.drop_index = -1

    def GetMinSize(self):
        height = self.HEADER_HEIGHT + max(3, len(self.sources)) * self.ROW_HEIGHT + 8
        return 460, height

    def current_nodes(self):
        return list(self.sources)

    def clamp_index(self, index, include_end=False):
        upper = len(self.sources) if include_end else len(self.sources) - 1
        if upper < 0:
            return -1
        return max(0, min(index, upper))

    def row_at_y(self, y):
        if y < self.HEADER_HEIGHT:
            return -1
        index = int((y - self.HEADER_HEIGHT) // self.ROW_HEIGHT)
        if 0 <= index < len(self.sources):
            return index
        return -1

    def insert_index_for_y(self, y):
        index = int((y - self.HEADER_HEIGHT + (self.ROW_HEIGHT / 2.0)) // self.ROW_HEIGHT)
        return self.clamp_index(index, include_end=True)

    def row_card_left(self):
        return 8 + self.SLOT_LABEL_WIDTH

    def event_point(self, msg):
        x = float(msg[c4d.BFM_INPUT_X])
        y = float(msg[c4d.BFM_INPUT_Y])

        try:
            offset = self.Global2Local()
            if offset is not None:
                return x + float(offset["x"]), y + float(offset["y"])
        except Exception:
            pass

        return x, y

    def move_selected(self, delta):
        if self.selected_index < 0:
            return

        insert_index = self.selected_index + delta
        if delta > 0:
            insert_index += 1
        self.move_row(self.selected_index, insert_index)

    def move_selected_to_top(self):
        if self.selected_index >= 0:
            self.move_row(self.selected_index, 0)

    def move_selected_to_bottom(self):
        if self.selected_index >= 0:
            self.move_row(self.selected_index, len(self.sources))

    def inverse_order(self):
        self.sources.reverse()
        if self.selected_index >= 0:
            self.selected_index = len(self.sources) - 1 - self.selected_index
        self.Redraw()

    def move_row(self, old_index, insert_index):
        if old_index < 0 or old_index >= len(self.sources):
            return

        insert_index = self.clamp_index(insert_index, include_end=True)
        if insert_index > old_index:
            insert_index -= 1
        if insert_index == old_index:
            self.selected_index = old_index
            self.Redraw()
            return

        source = self.sources.pop(old_index)
        insert_index = self.clamp_index(insert_index, include_end=True)
        self.sources.insert(insert_index, source)
        self.selected_index = insert_index
        self.Redraw()

    def color(self, color_id, fallback):
        try:
            rgb = self.GetColorRGB(color_id)
            return c4d.Vector(
                rgb.get("r", 0) / 255.0,
                rgb.get("g", 0) / 255.0,
                rgb.get("b", 0) / 255.0,
            )
        except Exception:
            return fallback

    def mix(self, a, b, amount):
        return c4d.Vector(
            a.x + (b.x - a.x) * amount,
            a.y + (b.y - a.y) * amount,
            a.z + (b.z - a.z) * amount,
        )

    def draw_box(self, x1, y1, x2, y2, color, radius=0):
        self.DrawSetPen(color)
        if radius:
            try:
                self.DrawRoundedRectangle(x1, y1, x2, y2, radius, radius)
                return
            except Exception:
                pass
        self.DrawRectangle(x1, y1, x2, y2)

    def draw_frame(self, x1, y1, x2, y2, color, radius=0):
        self.DrawSetPen(color)
        if radius:
            try:
                self.DrawRoundedFrame(x1, y1, x2, y2, radius, radius)
                return
            except Exception:
                pass
        self.DrawFrame(x1, y1, x2, y2)

    def DrawMsg(self, x1, y1, x2, y2, msg):
        width = max(1, self.GetWidth())
        height = max(1, self.GetHeight())

        bg = self.color(c4d.COLOR_BG, c4d.Vector(0.17, 0.17, 0.17))
        panel = self.mix(bg, c4d.Vector(0.04, 0.04, 0.04), 0.28)
        row_bg = self.mix(bg, c4d.Vector(0.26, 0.26, 0.26), 0.45)
        row_alt = self.mix(bg, c4d.Vector(0.22, 0.22, 0.22), 0.35)
        selected_bg = self.mix(bg, c4d.Vector(0.73, 0.54, 0.12), 0.55)
        text = self.color(c4d.COLOR_TEXT, c4d.Vector(0.9, 0.9, 0.9))
        dim_text = self.mix(text, bg, 0.36)
        selected_text = c4d.Vector(1.0, 0.96, 0.80)
        line = self.mix(bg, c4d.Vector(0.0, 0.0, 0.0), 0.42)
        drop = c4d.Vector(1.0, 0.78, 0.08)

        try:
            self.OffScreenOn()
        except Exception:
            pass

        self.draw_box(0, 0, width, height, bg)
        self.draw_box(4, 4, width - 5, height - 5, panel, 7)

        self.DrawSetFont(c4d.FONT_BOLD)
        self.DrawSetTextCol(text, panel)
        self.DrawText("Shader slot order", self.PAD_X + 1, 7)
        self.DrawSetFont(c4d.FONT_DEFAULT)
        if width > 320:
            self.DrawSetTextCol(dim_text, panel)
            self.DrawText("%d texture node(s)" % len(self.sources), width - 120, 8)
        self.DrawSetPen(self.mix(line, bg, 0.25))
        self.DrawLine(8, self.HEADER_HEIGHT - 2, width - 9, self.HEADER_HEIGHT - 2)

        self.DrawSetFont(c4d.FONT_DEFAULT)
        for index, source in enumerate(self.sources):
            top = self.HEADER_HEIGHT + index * self.ROW_HEIGHT + (self.ROW_GAP // 2)
            bottom = top + self.ROW_HEIGHT - self.ROW_GAP
            slot_left = 12
            left = self.row_card_left()
            right = width - 9
            selected = index == self.selected_index
            row_color = selected_bg if selected else (row_alt if index % 2 else row_bg)

            self.DrawSetTextCol(selected_text if selected else dim_text, panel)
            self.DrawText("Shader %d" % index, slot_left, top + 7)

            self.draw_box(left, top, right, bottom, row_color, 5)
            self.draw_frame(left, top, right, bottom, drop if selected else line, 5)

            handle_x = left + self.PAD_X
            self.DrawSetTextCol(dim_text if not selected else selected_text, row_color)
            self.DrawText("|||", handle_x, top + 7)

            label_x = left + self.PAD_X + self.HANDLE_WIDTH
            self.DrawSetTextCol(selected_text if selected else text, row_color)
            self.DrawText(node_label(source), label_x, top + 7)

        if self.drop_index >= 0:
            y = self.HEADER_HEIGHT + self.drop_index * self.ROW_HEIGHT
            self.draw_box(self.row_card_left(), y - 2, width - 13, y + 2, drop, 2)

        self.draw_frame(4, 4, width - 5, height - 5, line, 7)

    def InputEvent(self, msg):
        if msg[c4d.BFM_INPUT_DEVICE] != c4d.BFM_INPUT_MOUSE:
            return False
        if msg[c4d.BFM_INPUT_CHANNEL] != c4d.BFM_INPUT_MOUSELEFT:
            return False

        raw_x = float(msg[c4d.BFM_INPUT_X])
        raw_y = float(msg[c4d.BFM_INPUT_Y])
        local_x, local_y = self.event_point(msg)
        row = self.row_at_y(local_y)
        if row < 0:
            return False
        if local_x < self.row_card_left():
            return False

        self.selected_index = row
        self.drop_index = row
        self.Redraw()

        self.MouseDragStart(
            c4d.KEY_MLEFT,
            raw_x,
            raw_y,
            c4d.MOUSEDRAGFLAGS_DONTHIDEMOUSE | c4d.MOUSEDRAGFLAGS_EVERYPACKET,
        )

        current_y = local_y
        while True:
            result, dx, dy, channels = self.MouseDrag()
            if result != c4d.MOUSEDRAGRESULT_CONTINUE:
                break

            current_y -= dy
            new_drop_index = self.insert_index_for_y(current_y)
            if new_drop_index != self.drop_index:
                self.drop_index = new_drop_index
                self.Redraw()

        final_drop_index = self.drop_index
        self.drop_index = -1
        if self.MouseDragEnd() != c4d.MOUSEDRAGRESULT_ESCAPE:
            self.move_row(row, final_drop_index)
        else:
            self.Redraw()

        return True


class ReorderSourcesDialog(c4d.gui.GeDialog):
    def __init__(self, shader_sources, document):
        super(ReorderSourcesDialog, self).__init__()
        self.shader_sources = list(shader_sources)
        self.document = document
        self.order_area = ShaderSourceOrderArea(self.shader_sources)
        self.native_gui = None
        self.native_data = None
        self.temp_parent = None
        self.temp_objects = []
        self.node_by_temp_guid = {}
        self.node_by_temp_name = {}
        self.result = None
        self.cancelled = True

    def hide_temp_object(self, obj):
        try:
            obj.SetEditorMode(c4d.MODE_OFF)
            obj.SetRenderMode(c4d.MODE_OFF)
        except Exception:
            pass

        for bit in (c4d.NBIT_OHIDE, c4d.NBIT_EHIDE):
            try:
                obj.ChangeNBit(bit, c4d.NBITCONTROL_SET)
            except Exception:
                pass

    def create_native_data(self):
        data = c4d.InExcludeData()

        parent = c4d.BaseObject(c4d.Onull)
        parent.SetName("__Shader Slot Order Temp__")
        self.hide_temp_object(parent)
        self.document.InsertObject(parent)
        self.temp_parent = parent

        for index, source in enumerate(self.shader_sources):
            obj = c4d.BaseObject(c4d.Onull)
            temp_name = source_order_label(index, source)
            obj.SetName(temp_name)
            self.hide_temp_object(obj)
            self.document.InsertObject(obj, parent)
            self.temp_objects.append(obj)
            self.node_by_temp_name[temp_name] = source

            try:
                self.node_by_temp_guid[obj.GetGUID()] = source
            except Exception:
                self.node_by_temp_guid[id(obj)] = source

            data.InsertObject(obj, 1)

        try:
            c4d.EventAdd()
        except Exception:
            pass

        self.native_data = data
        return data

    def cleanup_temp_objects(self):
        try:
            if self.temp_parent is not None:
                self.temp_parent.Remove()
            else:
                for obj in self.temp_objects:
                    try:
                        obj.Remove()
                    except Exception:
                        pass
        except Exception:
            pass

        self.temp_parent = None
        self.temp_objects = []
        try:
            c4d.EventAdd()
        except Exception:
            pass

    def native_ordered_sources(self):
        data = None
        if self.native_gui is not None:
            try:
                data = self.native_gui.GetData()
            except Exception:
                data = None
        if data is None:
            data = self.native_data
        if data is None:
            return []

        ordered = []
        count = data.GetObjectCount()
        for index in range(count):
            obj = data.ObjectFromIndex(self.document, index)
            if obj is None:
                continue

            source = None
            try:
                source = self.node_by_temp_guid.get(obj.GetGUID())
            except Exception:
                source = None
            if source is None:
                source = self.node_by_temp_guid.get(id(obj))
            if source is None:
                try:
                    source = self.node_by_temp_name.get(obj.GetName())
                except Exception:
                    source = None
            if source is not None:
                ordered.append(source)

        return ordered

    def CreateLayout(self):
        self.SetTitle("Shader Slot Order")
        self.GroupBegin(0, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, 0)
        self.AddStaticText(
            0,
            c4d.BFH_SCALEFIT,
            0,
            0,
            "Drag to set shader slots.",
        )

        if USE_NATIVE_INEXCLUDE_REORDER:
            settings = c4d.BaseContainer()
            settings.SetBool(c4d.DESCRIPTION_OBJECTSNOTINDOC, True)
            settings.SetBool(c4d.IN_EXCLUDE_FLAG_SEND_SELCHANGE_MSG, True)
            settings.SetBool(c4d.IN_EXCLUDE_FLAG_DISABLE_CONTEXTMENU, True)
            settings.SetInt32(c4d.IN_EXCLUDE_FLAG_NUM_FLAGS, 0)
            settings.SetInt32(c4d.IN_EXCLUDE_FLAG_SMALL_MODE_SIZE, 180)
            settings.SetInt32(c4d.IN_EXCLUDE_FLAG_BIG_MODE_SIZE, 180)

            try:
                self.native_gui = self.AddCustomGui(
                    IDC_ORDER_AREA,
                    c4d.CUSTOMGUI_INEXCLUDE_LIST,
                    "",
                    c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                    460,
                    180,
                    settings,
                )
                if self.native_gui is not None:
                    self.native_gui.SetData(self.create_native_data())
            except Exception:
                self.native_gui = None

        if self.native_gui is None:
            self.AddUserArea(IDC_ORDER_AREA, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 460, 180)
            self.AttachUserArea(self.order_area, IDC_ORDER_AREA)

        self.GroupBegin(0, c4d.BFH_RIGHT, 3, 1)
        self.AddButton(IDC_INVERSE, c4d.BFH_RIGHT, 80, 0, "Inverse")
        self.AddButton(IDC_CANCEL, c4d.BFH_RIGHT, 75, 0, "Cancel")
        self.AddButton(IDC_CONNECT, c4d.BFH_RIGHT, 90, 0, "Connect")
        self.GroupEnd()
        self.GroupEnd()
        return True

    def InitValues(self):
        return True

    def Command(self, control_id, msg):
        if control_id == IDC_CANCEL:
            self.cancelled = True
            self.Close()
            return True

        if control_id == IDC_INVERSE:
            if self.native_gui is None:
                self.order_area.inverse_order()
            return True

        if control_id == IDC_CONNECT:
            if self.native_gui is not None:
                self.result = self.native_ordered_sources()
            else:
                self.result = self.order_area.current_nodes()
            self.cancelled = False
            self.Close()
            return True

        return True


def get_user_ordered_shader_sources(shader_sources, document):
    if len(shader_sources) <= 1:
        return shader_sources

    dialog = ReorderSourcesDialog(shader_sources, document)
    try:
        dialog.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, defaultw=500, defaulth=260)

        if dialog.cancelled:
            return None

        if dialog.result:
            return dialog.result

        return shader_sources
    finally:
        dialog.cleanup_temp_objects()


def try_connect(source_port, target_port):
    try:
        result = source_port.Connect(target_port, maxon.WIRE_MODE.NORMAL)
    except Exception:
        return False

    if result is False:
        return False
    if result is True:
        return True

    try:
        return bool(maxon.GraphModelHelper.IsConnected(source_port, target_port))
    except Exception:
        return True


def candidate_target_ports(source, source_output, target, available_inputs, shader_switch_mode):
    if not shader_switch_mode:
        return available_inputs

    selector = is_selector_source(source, source_output)
    shader = is_shader_source(source_output)

    if selector:
        return selector_candidate_ports(target, available_inputs)

    if shader:
        return shader_slot_candidate_ports(target, available_inputs)

    return available_inputs


def clear_target_inputs(target):
    for port in input_ports(target):
        try:
            port.RemoveConnections(maxon.PORT_DIR.INPUT, maxon.Wires.All())
        except Exception:
            pass


def connect_sources_to_target(graph, sources, target, replace_existing=True):
    shader_switch_mode = shader_switch_score(target) >= 120
    connected = []
    skipped = []

    with graph.BeginTransaction() as transaction:
        if replace_existing:
            clear_target_inputs(target)

        available_inputs = list(free_input_ports(target))

        for source in sources:
            source_outputs = source_output_candidates(source)
            if not source_outputs:
                skipped.append("%s: no output port" % node_label(source))
                continue

            did_connect = False

            for source_output in source_outputs:
                for target_input in candidate_target_ports(
                    source, source_output, target, available_inputs, shader_switch_mode
                ):
                    if try_connect(source_output, target_input):
                        connected.append(
                            "%s.%s -> %s.%s"
                            % (
                                node_label(source),
                                port_label(source_output),
                                node_label(target),
                                port_label(target_input),
                            )
                        )
                        available_inputs.remove(target_input)
                        did_connect = True
                        break

                if did_connect:
                    break

            if not did_connect:
                skipped.append("%s: no compatible free input found" % node_label(source))

        transaction.Commit()

    return connected, skipped


def main():
    try:
        graph = get_active_redshift_graph(doc)
        selected_nodes = get_selected_true_nodes(graph)

        if len(selected_nodes) < 2:
            raise RuntimeError("Select at least two nodes: one or more source nodes and one target node.")

        target = choose_target_node(selected_nodes)
        sources = sort_sources([node for node in selected_nodes if node != target])

        if not sources:
            raise RuntimeError("No source nodes found in the selection.")

        if not input_ports(target):
            raise RuntimeError("The target node '%s' has no input ports." % node_label(target))

        selector_sources, shader_sources, other_sources = split_source_types(sources)
        ordered_shader_sources = get_user_ordered_shader_sources(shader_sources, doc)
        if ordered_shader_sources is None:
            return

        ordered_sources = selector_sources + ordered_shader_sources + other_sources
        connected, skipped = connect_sources_to_target(
            graph, ordered_sources, target, replace_existing=True
        )
        c4d.EventAdd()

        summary = "Connected %d node(s) into '%s'." % (len(connected), node_label(target))
        if skipped:
            summary += "\n\nSkipped:\n- " + "\n- ".join(skipped)
        summary += "\n\nShader slots used the order from the dialog."

        print(summary)

    except Exception as error:
        message("Redshift node auto-connect failed:\n%s" % error)


if __name__ == "__main__":
    main()
