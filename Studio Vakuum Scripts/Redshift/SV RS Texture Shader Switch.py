"""
SV Texture Shader Switch

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Creates Texture Nodes from selected images and connects them to Shader Switch Node/s.

Written for Maxon Cinema 4D 2026.3.2 or later
Python version 3.11.4
"""

import os
import sys

import c4d
import maxon


RS_NODE_SPACE = maxon.Id("com.redshift3d.redshift4c4d.class.nodespace")
TEXTURE_SAMPLER_ASSET = "com.redshift3d.redshift4c4d.nodes.core.texturesampler"
INTEGER_USER_DATA_ASSET = "com.redshift3d.redshift4c4d.nodes.core.rsuserdatainteger"
SHADER_SWITCH_ASSET = "com.redshift3d.redshift4c4d.nodes.core.rsshaderswitch"
SWITCH_SLOT_COUNT = 10
ARRANGE_SELECTED_NODES_COMMAND = 465002311

IDC_ORDER_REVERSE = 2001
IDC_ORDER_CANCEL = 2002
IDC_ORDER_CREATE = 2003
IDC_ORDER_AREA = 2004
IDC_ORDER_SCROLL = 2005
ORDER_MAX_VISIBLE_ROWS = 12


def show_error(text):
    print(text)
    c4d.gui.MessageDialog(text)


def is_valid(value):
    try:
        return value is not None and not value.IsNullValue()
    except AttributeError:
        return value is not None


def selected_files():
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            class OPENFILENAMEW(ctypes.Structure):
                _fields_ = (
                    ("lStructSize", wintypes.DWORD),
                    ("hwndOwner", wintypes.HWND),
                    ("hInstance", wintypes.HINSTANCE),
                    ("lpstrFilter", wintypes.LPCWSTR),
                    ("lpstrCustomFilter", wintypes.LPWSTR),
                    ("nMaxCustFilter", wintypes.DWORD),
                    ("nFilterIndex", wintypes.DWORD),
                    ("lpstrFile", wintypes.LPWSTR),
                    ("nMaxFile", wintypes.DWORD),
                    ("lpstrFileTitle", wintypes.LPWSTR),
                    ("nMaxFileTitle", wintypes.DWORD),
                    ("lpstrInitialDir", wintypes.LPCWSTR),
                    ("lpstrTitle", wintypes.LPCWSTR),
                    ("Flags", wintypes.DWORD),
                    ("nFileOffset", wintypes.WORD),
                    ("nFileExtension", wintypes.WORD),
                    ("lpstrDefExt", wintypes.LPCWSTR),
                    ("lCustData", wintypes.LPARAM),
                    ("lpfnHook", wintypes.LPVOID),
                    ("lpTemplateName", wintypes.LPCWSTR),
                    ("pvReserved", wintypes.LPVOID),
                    ("dwReserved", wintypes.DWORD),
                    ("FlagsEx", wintypes.DWORD),
                )

            buffer_size = 65536
            path_buffer = ctypes.create_unicode_buffer(buffer_size)
            file_filter = "Image Files\0*.bmp;*.cin;*.dpx;*.exr;*.gif;*.hdr;*.jpeg;*.jpg;*.png;*.psd;*.tga;*.tif;*.tiff;*.tx;*.webp\0All Files\0*.*\0\0"

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            comdlg32 = ctypes.WinDLL("comdlg32", use_last_error=True)
            user32.GetForegroundWindow.argtypes = ()
            user32.GetForegroundWindow.restype = wintypes.HWND
            comdlg32.GetOpenFileNameW.argtypes = (ctypes.POINTER(OPENFILENAMEW),)
            comdlg32.GetOpenFileNameW.restype = wintypes.BOOL
            comdlg32.CommDlgExtendedError.argtypes = ()
            comdlg32.CommDlgExtendedError.restype = wintypes.DWORD

            file_dialog = OPENFILENAMEW()
            file_dialog.lStructSize = ctypes.sizeof(OPENFILENAMEW)
            file_dialog.hwndOwner = user32.GetForegroundWindow()
            file_dialog.lpstrFilter = file_filter
            file_dialog.nFilterIndex = 1
            file_dialog.lpstrFile = ctypes.cast(path_buffer, wintypes.LPWSTR)
            file_dialog.nMaxFile = buffer_size
            file_dialog.lpstrTitle = "Select textures for Redshift Shader Switch"
            file_dialog.Flags = (
                0x00080000
                | 0x00000200
                | 0x00001000
                | 0x00000800
                | 0x00000008
                | 0x00000004
            )

            if not comdlg32.GetOpenFileNameW(ctypes.byref(file_dialog)):
                error_code = comdlg32.CommDlgExtendedError()
                if error_code:
                    raise RuntimeError(
                        "Windows file dialog failed with error 0x%08X." % error_code
                    )
                return []

            parts = [value for value in path_buffer[:].split("\0") if value]
            if not parts:
                return []
            if len(parts) == 1:
                return [parts[0]]

            directory = parts[0]
            return [os.path.join(directory, filename) for filename in parts[1:]]
        except Exception as native_error:
            message = "Could not open the native Windows multi-file dialog:\n%s" % native_error
            print(message)
            c4d.gui.MessageDialog(message)
            return []

    if sys.platform != "darwin":
        c4d.gui.MessageDialog(
            "Texture Shader Switch file selection is supported on macOS and Windows."
        )
        return []

    try:
        import ctypes
        import ctypes.util

        appkit_path = ctypes.util.find_library("AppKit")
        objc_path = ctypes.util.find_library("objc")
        if not appkit_path or not objc_path:
            raise RuntimeError("The macOS AppKit frameworks could not be found.")

        appkit = ctypes.CDLL(appkit_path)
        objc = ctypes.CDLL(objc_path)
        objc.objc_getClass.argtypes = (ctypes.c_char_p,)
        objc.objc_getClass.restype = ctypes.c_void_p
        objc.sel_registerName.argtypes = (ctypes.c_char_p,)
        objc.sel_registerName.restype = ctypes.c_void_p

        msg_send_address = ctypes.cast(objc.objc_msgSend, ctypes.c_void_p).value

        def objc_class(name):
            value = objc.objc_getClass(name.encode("utf-8"))
            if not value:
                raise RuntimeError("Objective-C class '%s' is unavailable." % name)
            return value

        def objc_send(receiver, selector, restype=ctypes.c_void_p, argtypes=(), args=()):
            signature = ctypes.CFUNCTYPE(
                restype,
                ctypes.c_void_p,
                ctypes.c_void_p,
                *argtypes,
            )
            function = signature(msg_send_address)
            return function(
                receiver,
                objc.sel_registerName(selector.encode("utf-8")),
                *args,
            )

        application = objc_send(objc_class("NSApplication"), "sharedApplication")
        objc_send(
            application,
            "activateIgnoringOtherApps:",
            None,
            (ctypes.c_bool,),
            (True,),
        )

        panel = objc_send(objc_class("NSOpenPanel"), "openPanel")
        if not panel:
            raise RuntimeError("Could not create the macOS file panel.")

        for selector, enabled in (
            ("setCanChooseFiles:", True),
            ("setCanChooseDirectories:", False),
            ("setAllowsMultipleSelection:", True),
            ("setResolvesAliases:", True),
        ):
            objc_send(panel, selector, None, (ctypes.c_bool,), (enabled,))

        prompt = objc_send(
            objc_class("NSString"),
            "stringWithUTF8String:",
            ctypes.c_void_p,
            (ctypes.c_char_p,),
            (b"Select textures for Redshift Shader Switch",),
        )
        objc_send(panel, "setMessage:", None, (ctypes.c_void_p,), (prompt,))

        response = objc_send(panel, "runModal", ctypes.c_long)
        if response != 1:
            return []

        urls = objc_send(panel, "URLs")
        count = objc_send(urls, "count", ctypes.c_ulong)
        paths = []
        for index in range(count):
            url = objc_send(
                urls,
                "objectAtIndex:",
                ctypes.c_void_p,
                (ctypes.c_ulong,),
                (index,),
            )
            ns_path = objc_send(url, "path")
            utf8_path = objc_send(ns_path, "UTF8String", ctypes.c_char_p)
            if utf8_path:
                paths.append(utf8_path.decode("utf-8"))
        return paths
    except Exception as native_error:
        message = "Could not open the native macOS multi-file dialog:\n%s" % native_error
        print(message)
        c4d.gui.MessageDialog(message)
        return []


def texture_order_label(path):
    filename = os.path.basename(path)
    parent = os.path.basename(os.path.dirname(path))
    return "%s  —  %s" % (filename, parent) if parent else filename


class TextureOrderArea(c4d.gui.GeUserArea):
    HEADER_HEIGHT = 30
    ROW_HEIGHT = 32
    ROW_GAP = 4
    PAD_X = 9
    HANDLE_WIDTH = 19
    SLOT_LABEL_WIDTH = 68

    def __init__(self, paths):
        super(TextureOrderArea, self).__init__()
        self.sources = list(paths)
        self.selected_index = 0 if self.sources else -1
        self.drop_index = -1

    def GetMinSize(self):
        height = self.HEADER_HEIGHT + max(3, len(self.sources)) * self.ROW_HEIGHT + 8
        return 460, height

    def current_paths(self):
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
        index = int(
            (y - self.HEADER_HEIGHT + self.ROW_HEIGHT / 2.0) // self.ROW_HEIGHT
        )
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

    def reverse_order(self):
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
        insert_index = max(0, min(insert_index, len(self.sources)))
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
            self.DrawText("%d texture(s)" % len(self.sources), width - 110, 8)
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
            self.DrawText(texture_order_label(source), label_x, top + 7)

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
        row_center_y = self.HEADER_HEIGHT + row * self.ROW_HEIGHT + self.ROW_HEIGHT / 2.0
        center_offset_y = row_center_y - local_y
        self.drop_index = self.insert_index_for_y(row_center_y)
        self.Redraw()

        state_to_local_y = None
        initial_state = c4d.BaseContainer()
        try:
            if c4d.gui.GetInputState(
                c4d.BFM_INPUT_MOUSE,
                c4d.BFM_INPUT_MOUSELEFT,
                initial_state,
            ):
                state_to_local_y = local_y - float(initial_state[c4d.BFM_INPUT_Y])
        except Exception:
            state_to_local_y = None

        self.MouseDragStart(
            c4d.KEY_MLEFT,
            raw_x,
            raw_y,
            c4d.MOUSEDRAGFLAGS_DONTHIDEMOUSE | c4d.MOUSEDRAGFLAGS_EVERYPACKET,
        )

        current_y = row_center_y
        while True:
            result, dx, dy, channels = self.MouseDrag()
            if result != c4d.MOUSEDRAGRESULT_CONTINUE:
                break

            state = c4d.BaseContainer()
            try:
                has_state = c4d.gui.GetInputState(
                    c4d.BFM_INPUT_MOUSE,
                    c4d.BFM_INPUT_MOUSELEFT,
                    state,
                )
            except Exception:
                has_state = False
            if has_state and state_to_local_y is not None:
                pointer_y = float(state[c4d.BFM_INPUT_Y]) + state_to_local_y
                current_y = pointer_y + center_offset_y
            else:
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


class TextureOrderDialog(c4d.gui.GeDialog):

    def __init__(self, paths):
        super(TextureOrderDialog, self).__init__()
        self.order_area = TextureOrderArea(paths)
        self.result = None
        self.cancelled = True

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

        if len(self.order_area.sources) > ORDER_MAX_VISIBLE_ROWS:
            visible_height = (
                self.order_area.HEADER_HEIGHT
                + ORDER_MAX_VISIBLE_ROWS * self.order_area.ROW_HEIGHT
                + 8
            )
            if self.ScrollGroupBegin(
                IDC_ORDER_SCROLL,
                c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                c4d.SCROLLGROUP_VERT,
                0,
                visible_height,
            ):
                self.AddUserArea(
                    IDC_ORDER_AREA,
                    c4d.BFH_SCALEFIT | c4d.BFV_TOP,
                    460,
                    self.order_area.GetMinSize()[1],
                )
                self.AttachUserArea(self.order_area, IDC_ORDER_AREA)
                self.GroupEnd()
        else:
            self.AddUserArea(
                IDC_ORDER_AREA,
                c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                460,
                180,
            )
            self.AttachUserArea(self.order_area, IDC_ORDER_AREA)

        self.GroupBegin(0, c4d.BFH_RIGHT, 3, 1)
        self.AddButton(IDC_ORDER_REVERSE, c4d.BFH_RIGHT, 80, 0, "Inverse")
        self.AddButton(IDC_ORDER_CANCEL, c4d.BFH_RIGHT, 75, 0, "Cancel")
        self.AddButton(IDC_ORDER_CREATE, c4d.BFH_RIGHT, 100, 0, "Create")
        self.GroupEnd()
        self.GroupEnd()
        return True

    def Command(self, control_id, msg):
        if control_id == IDC_ORDER_REVERSE:
            self.order_area.reverse_order()
            return True

        if control_id == IDC_ORDER_CANCEL:
            self.cancelled = True
            self.Close()
            return True

        if control_id == IDC_ORDER_CREATE:
            self.result = self.order_area.current_paths()
            self.cancelled = False
            self.Close()
            return True

        return True


def get_ordered_texture_paths(paths):
    if len(paths) <= 1:
        return list(paths)
    dialog = TextureOrderDialog(paths)
    visible_rows = min(len(paths), ORDER_MAX_VISIBLE_ROWS)
    default_height = min(620, 100 + 30 + visible_rows * 32)
    dialog.Open(
        c4d.DLG_TYPE_MODAL_RESIZEABLE,
        defaultw=500,
        defaulth=default_height,
    )
    return None if dialog.cancelled else dialog.result


def active_graph(doc):
    material = doc.GetActiveMaterial()
    if material is None:
        raise RuntimeError("Please make the target Redshift material active first.")
    node_material = material.GetNodeMaterialReference()
    if node_material is None:
        raise RuntimeError("The active material is not a node material.")
    graph = node_material.GetGraph(RS_NODE_SPACE)
    if not is_valid(graph):
        raise RuntimeError("The active material has no Redshift node graph.")
    return graph


def port_name(port):
    for key in (maxon.NODE.BASE.NAME,):
        try:
            value = port.GetValue(key)
            if value:
                return str(value)
        except Exception:
            pass
    try:
        return str(port.GetId())
    except Exception:
        return ""


def direct_ports(port_group, kind):
    try:
        return list(port_group.GetChildren(mask=kind))
    except Exception:
        return []


def shader_input_ports(switch):
    direct_ids = [
        "com.redshift3d.redshift4c4d.nodes.core.rsshaderswitch.shader%d" % index
        for index in range(SWITCH_SLOT_COUNT)
    ]
    direct = []
    for port_id in direct_ids:
        try:
            port = switch.GetInputs().FindChild(port_id)
            if is_valid(port):
                direct.append(port)
        except Exception:
            pass
    if direct:
        return direct

    numbered = []
    for index, port in enumerate(direct_ports(switch.GetInputs(), maxon.NODE_KIND.INPORT)):
        label = port_name(port).lower().replace(" ", "")
        number = None
        for prefix in ("shader",):
            if label.startswith(prefix) and label[len(prefix):].isdigit():
                number = int(label[len(prefix):])
                break
        if number is not None:
            numbered.append((number, port))
    if numbered:
        return [port for _, port in sorted(numbered)]

    return direct_ports(switch.GetInputs(), maxon.NODE_KIND.INPORT)[1:]


def output_port(node):
    ports = direct_ports(node.GetOutputs(), maxon.NODE_KIND.OUTPORT)
    if not ports:
        return None
    preferred = ("outcolor", "color", "out", "shader")
    return sorted(
        ports,
        key=lambda port: next((i for i, name in enumerate(preferred) if name in port_name(port).lower().replace(" ", "")), len(preferred)),
    )[0]


def recursive_ports(port):
    for child in port.GetChildren():
        yield child
        yield from recursive_ports(child)


def set_texture_path(texture, path):
    file_url = maxon.Url("file://" + path)
    try:
        texture_port = texture.GetInputs().FindChild(
            "com.redshift3d.redshift4c4d.nodes.core.texturesampler.tex0"
        )
        path_port = texture_port.FindChild("path") if is_valid(texture_port) else None
        if is_valid(path_port):
            path_port.SetPortValue(file_url)
            return True
    except Exception:
        pass

    values = (file_url, maxon.Url(path), maxon.String(path), path)
    candidates = list(recursive_ports(texture.GetInputs()))
    candidates += direct_ports(texture.GetInputs(), maxon.NODE_KIND.INPORT)
    for port in candidates:
        port_id = str(port.GetId()).lower()
        if not any(key in port_id for key in ("path", "file", "tex0")):
            continue
        for value in values:
            try:
                port.SetPortValue(value)
                return True
            except Exception:
                pass
    return False


def set_switch_offset(switch, offset):
    try:
        port = switch.GetInputs().FindChild(
            "com.redshift3d.redshift4c4d.nodes.core.rsshaderswitch.offset"
        )
        if is_valid(port):
            port.SetPortValue(maxon.Int(offset))
            return True
    except Exception:
        pass

    for port in recursive_ports(switch.GetInputs()):
        label = (port_name(port) + str(port.GetId())).lower().replace(" ", "")
        if "offset" not in label:
            continue
        for value in (maxon.Int(offset), int(offset)):
            try:
                port.SetPortValue(value)
                return True
            except Exception:
                pass
    return False


def hide_node_preview(node):
    preview_values = (
        ("DISPLAYPREVIEW", False),
        ("HIDEPREVIEW", True),
        ("SHOWPREVIEW", False),
    )
    for attribute_name, value in preview_values:
        try:
            node.SetValue(getattr(maxon.NODE.BASE, attribute_name), value)
        except Exception:
            pass


def make_node(graph, asset_id, name):
    node = graph.AddChild(maxon.Id(), maxon.Id(asset_id), maxon.DataDictionary())
    if not is_valid(node):
        raise RuntimeError("Could not create Redshift node: %s" % asset_id)
    try:
        node.SetValue(maxon.NODE.BASE.NAME, name)
    except Exception:
        pass
    hide_node_preview(node)
    return node


def connect(source_node, target_port):
    source_port = output_port(source_node)
    if source_port is None:
        raise RuntimeError("Could not find an output on '%s'." % port_name(source_node))
    source_port.Connect(target_port, maxon.WIRE_MODE.NORMAL)


def find_port(port_group, port_id):
    try:
        port = port_group.FindChild(port_id)
        return port if is_valid(port) else None
    except Exception:
        return None


def connect_integer_user_data(selector, switch):
    output = find_port(
        selector.GetOutputs(),
        "com.redshift3d.redshift4c4d.nodes.core.rsuserdatainteger.out",
    ) or output_port(selector)
    selector_input = find_port(
        switch.GetInputs(),
        "com.redshift3d.redshift4c4d.nodes.core.rsshaderswitch.selector",
    )
    if output is None or selector_input is None:
        raise RuntimeError("Could not find the Integer User Data or Shader Selector port.")
    output.Connect(selector_input, maxon.WIRE_MODE.NORMAL)


def build_switch_chain(graph, textures):
    first_switch = make_node(graph, SHADER_SWITCH_ASSET, "Shader Switch")
    switches = [first_switch]
    current = first_switch
    slots = shader_input_ports(current)
    if len(slots) < 2:
        raise RuntimeError("The Redshift Shader Switch does not expose its shader input ports.")

    texture_index = 0
    while texture_index < len(textures):
        available_slots = slots if current is first_switch else slots[1:]
        for slot in available_slots:
            if texture_index >= len(textures):
                break
            connect(textures[texture_index], slot)
            texture_index += 1

        if texture_index >= len(textures):
            break

        next_switch = make_node(
            graph, SHADER_SWITCH_ASSET, "Shader Switch %d" % (len(switches) + 1)
        )
        set_switch_offset(next_switch, len(switches) * SWITCH_SLOT_COUNT)
        next_slots = shader_input_ports(next_switch)
        if not next_slots:
            raise RuntimeError("Could not find shader inputs on the added Shader Switch.")
        connect(current, next_slots[0])
        switches.append(next_switch)
        current = next_switch
        slots = next_slots

    return switches


def arrange_selected_nodes(graph, nodes):
    try:
        select_nodes(graph, nodes)
        c4d.GeSyncMessage(c4d.EVMSG_CHANGE)
        return c4d.CallCommand(ARRANGE_SELECTED_NODES_COMMAND)
    except Exception as error:
        print("Could not arrange the newly created nodes: %s" % error)
        return False


def select_nodes(graph, nodes):
    with graph.BeginTransaction() as transaction:
        maxon.GraphModelHelper.DeselectAll(graph, maxon.NODE_KIND.ALL_MASK)
        for node in nodes:
            maxon.GraphModelHelper.SelectNode(node)
        transaction.Commit()


def main():
    paths = selected_files()
    if not paths:
        return
    paths = get_ordered_texture_paths(paths)
    if not paths:
        return
    try:
        graph = active_graph(doc)
        with graph.BeginTransaction() as transaction:
            textures = []
            for path in paths:
                texture = make_node(
                    graph,
                    TEXTURE_SAMPLER_ASSET,
                    os.path.splitext(os.path.basename(path))[0],
                )
                if not set_texture_path(texture, path):
                    raise RuntimeError("Could not set the texture path for '%s'." % path)
                textures.append(texture)
            switches = build_switch_chain(graph, textures)
            selector = make_node(
                graph,
                INTEGER_USER_DATA_ASSET,
                "Shader Selector (Integer User Data)",
            )
            for switch in switches:
                connect_integer_user_data(selector, switch)
            transaction.Commit()
        new_nodes = textures + switches + [selector]
        arrange_selected_nodes(graph, new_nodes)
        select_nodes(graph, new_nodes)
        c4d.EventAdd()
        print("Created %d Texture Sampler(s) and %d Shader Switch node(s)." % (len(textures), len(switches)))
    except Exception as error:
        show_error(str(error))


if __name__ == "__main__":
    main()