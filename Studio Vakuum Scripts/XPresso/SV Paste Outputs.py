import c4d
from c4d.modules import graphview
"""only works for Englisch!!!"""

parameter_map = {
    "Position": c4d.ID_BASEOBJECT_REL_POSITION,
    "Position . X": (c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_X),
    "Position . Y": (c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_Y),
    "Position . Z": (c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_Z),

    "Rotation": c4d.ID_BASEOBJECT_REL_ROTATION,
    "Rotation . H": (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X),
    "Rotation . P": (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y),
    "Rotation . B": (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z),

    "Scale": c4d.ID_BASEOBJECT_REL_SCALE,
    "Scale . X": (c4d.ID_BASEOBJECT_REL_SCALE, c4d.VECTOR_X),
    "Scale . Y": (c4d.ID_BASEOBJECT_REL_SCALE, c4d.VECTOR_Y),
    "Scale . Z": (c4d.ID_BASEOBJECT_REL_SCALE, c4d.VECTOR_Z),

    "Global Position": c4d.ID_BASEOBJECT_GLOBAL_POSITION,
    "Global Position . X": (c4d.ID_BASEOBJECT_GLOBAL_POSITION, c4d.VECTOR_X),
    "Global Position . Y": (c4d.ID_BASEOBJECT_GLOBAL_POSITION, c4d.VECTOR_Y),
    "Global Position . Z": (c4d.ID_BASEOBJECT_GLOBAL_POSITION, c4d.VECTOR_Z),

    "Global Rotation": c4d.ID_BASEOBJECT_GLOBAL_ROTATION,
    "Global Rotation . H": (c4d.ID_BASEOBJECT_GLOBAL_ROTATION, c4d.VECTOR_X),
    "Global Rotation . P": (c4d.ID_BASEOBJECT_GLOBAL_ROTATION, c4d.VECTOR_Y),
    "Global Rotation . B": (c4d.ID_BASEOBJECT_GLOBAL_ROTATION, c4d.VECTOR_Z),

    "Frozen Position": c4d.ID_BASEOBJECT_FROZEN_POSITION,
    "Frozen Position . X": (c4d.ID_BASEOBJECT_FROZEN_POSITION, c4d.VECTOR_X),
    "Frozen Position . Y": (c4d.ID_BASEOBJECT_FROZEN_POSITION, c4d.VECTOR_Y),
    "Frozen Position . Z": (c4d.ID_BASEOBJECT_FROZEN_POSITION, c4d.VECTOR_Z),

    "Frozen Rotation": c4d.ID_BASEOBJECT_FROZEN_ROTATION,
    "Frozen Rotation . H": (c4d.ID_BASEOBJECT_FROZEN_ROTATION, c4d.VECTOR_X),
    "Frozen Rotation . P": (c4d.ID_BASEOBJECT_FROZEN_ROTATION, c4d.VECTOR_Y),
    "Frozen Rotation . B": (c4d.ID_BASEOBJECT_FROZEN_ROTATION, c4d.VECTOR_Z),

    "Frozen Scale": c4d.ID_BASEOBJECT_FROZEN_SCALE,
    "Frozen Scale . X": (c4d.ID_BASEOBJECT_FROZEN_SCALE, c4d.VECTOR_X),
    "Frozen Scale . Y": (c4d.ID_BASEOBJECT_FROZEN_SCALE, c4d.VECTOR_Y),
    "Frozen Scale . Z": (c4d.ID_BASEOBJECT_FROZEN_SCALE, c4d.VECTOR_Z),

    "Color": c4d.ID_BASEOBJECT_COLOR,
    "Color . R": (c4d.ID_BASEOBJECT_COLOR, c4d.VECTOR_X),
    "Color . G": (c4d.ID_BASEOBJECT_COLOR, c4d.VECTOR_Y),
    "Color . B": (c4d.ID_BASEOBJECT_COLOR, c4d.VECTOR_Z),

    "Renderer Visibility": c4d.ID_BASEOBJECT_VISIBILITY_RENDER,
    "Viewport Visibility": c4d.ID_BASEOBJECT_VISIBILITY_EDITOR,
    "Enabled": c4d.ID_BASEOBJECT_GENERATOR_FLAG,
    "Display Color": c4d.ID_BASEOBJECT_USECOLOR,
    "Name": c4d.ID_BASELIST_NAME,
    "X-Ray": c4d.ID_BASEOBJECT_XRAY,

    "Layer": c4d.ID_LAYER_LINK,

    "Global Matrix": c4d.GV_OBJECT_OPERATOR_GLOBAL_OUT,
    "Local Matrix": c4d.GV_OBJECT_OPERATOR_LOCAL_OUT,

    "Object": c4d.GV_OBJECT_OPERATOR_OBJECT_OUT,
    "Reference Mode": c4d.GV_OBJECT_PATH_TYPE,
    "Instance Mode": c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE,
    "Reference Object": c4d.INSTANCEOBJECT_LINK,

    "Path": c4d.GV_OBJECT_PATH_ID,
    "Start Position": c4d.GV_OBJECT_START_TYPE_ID,
    "Start Distance": c4d.GV_OBJECT_DISTANCE_ID,
    "History Depth": c4d.GV_OBJECT_HISTORY_DEPTH_ID,
    "History level": c4d.GV_OBJECT_OPERATOR_HISTORY_IN,
    "On": c4d.GV_OBJECT_OPERATOR_ON,

    "Previous position": c4d.GV_OBJECT_OPERATOR_OLD_POS_OUT,
    "Previous rotation": c4d.GV_OBJECT_OPERATOR_OLD_ROT_OUT,
    "Previous scale": c4d.GV_OBJECT_OPERATOR_OLD_SIZE_OUT,
    "Previous global matrix": c4d.GV_OBJECT_OPERATOR_OLD_GLOBAL_OUT,
    "Previous local matrix": c4d.GV_OBJECT_OPERATOR_OLD_LOCAL_OUT,

    "Position velocity": c4d.GV_OBJECT_OPERATOR_VELOCITY_POS_OUT,
    "Rotation velocity": c4d.GV_OBJECT_OPERATOR_VELOCITY_ROT_OUT,
    "Scale velocity": c4d.GV_OBJECT_OPERATOR_VELOCITY_SIZE_OUT,

    "Quaternion Rotation": c4d.ID_BASEOBJECT_QUATERNION_ROTATION_INTERPOLATION,
    "Rotation Order": c4d.ID_BASEOBJECT_ROTATION_ORDER,

    "Clones": c4d.MGCLONER_MODE,
    "Mode": c4d.ID_MG_MOTIONGENERATOR_MODE,
    "Reset Coordinates": c4d.MGCLONER_FIX_CLONES,
    "Fix Texture": c4d.MGCLONER_FIX_TEXTURE,
    "Instance Mode": c4d.MGCLONER_VOLUMEINSTANCES_MODE,
    "Count": c4d.MG_GRID_RESOLUTION,
    "Size": c4d.MG_GRID_SIZE,
    "Form": c4d.MG_GRID_TYPE,
    "Fill": c4d.MG_GRID_INSIDE,
    "Viewport Mode": c4d.MGCLONER_MULTIINSTANCE_DRAW_MODE,
    "Count . X": (c4d.MG_GRID_RESOLUTION, c4d.VECTOR_X),
    "Count . Y": (c4d.MG_GRID_RESOLUTION, c4d.VECTOR_Y),
    "Count . Z": (c4d.MG_GRID_RESOLUTION, c4d.VECTOR_Z),
    "Size . X": (c4d.MG_GRID_SIZE, c4d.VECTOR_X),
    "Size . Y": (c4d.MG_GRID_SIZE, c4d.VECTOR_Y),
    "Size . Z": (c4d.MG_GRID_SIZE, c4d.VECTOR_Z),
    "Effectors": c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST,
    "Display": c4d.ID_MG_TRANSFORM_DISPLAYMODE,
    "P": c4d.ID_BASEOBJECT_REL_POSITION,
    "R": c4d.ID_BASEOBJECT_REL_ROTATION,
    "S": c4d.ID_BASEOBJECT_REL_SCALE,
    "Weight": c4d.ID_MG_TRANSFORM_WEIGHT,
    "Time": c4d.ID_MG_TRANSFORM_TIME,
    "Animation Mode": c4d.MGCLONER_ANIMATIONMODE,
    "W(UV)-Orientation": c4d.MG_GRID_UVAXIS,
    "P . X": (c4d.ID_MG_TRANSFORM_POSITION, c4d.VECTOR_X),
    "P . Y": (c4d.ID_MG_TRANSFORM_POSITION, c4d.VECTOR_Y),
    "P . Z": (c4d.ID_MG_TRANSFORM_POSITION, c4d.VECTOR_Z),
    "R . H": (c4d.ID_MG_TRANSFORM_ROTATE, c4d.VECTOR_X),
    "R . P": (c4d.ID_MG_TRANSFORM_ROTATE, c4d.VECTOR_Y),
    "R . B": (c4d.ID_MG_TRANSFORM_ROTATE, c4d.VECTOR_Z),
    "S . X": (c4d.ID_MG_TRANSFORM_SCALE, c4d.VECTOR_X),
    "S . Y": (c4d.ID_MG_TRANSFORM_SCALE, c4d.VECTOR_Y),
    "S . Z": (c4d.ID_MG_TRANSFORM_SCALE, c4d.VECTOR_Z)
    
    # to be continued
}

def GetStringFromClipboard():
    clipboard_text = c4d.GetStringFromClipboard()
    if clipboard_text:
        clipboard_text = clipboard_text.strip().strip('[]').strip('"')
        clipboard_parameters = [param.strip().strip('"') for param in clipboard_text.split(',')]
        return clipboard_parameters
    return []

def GetSelectedXPressoNodes():
    gv_master = graphview.GetMaster(0)
    if gv_master is None:
        return []

    selected_nodes = []
    for node in gv_master.GetRoot().GetChildren():
        if node.GetBit(c4d.BIT_ACTIVE):
            selected_nodes.append(node)
    return selected_nodes

def AddPortsFromClipboard():
    clipboard_parameters = GetStringFromClipboard()
    if not clipboard_parameters:
        print("Das Clipboard ist leer oder enthält ungültige Daten.")
        return

    print("Gefundene Parameter im Clipboard:", clipboard_parameters)

    selected_nodes = GetSelectedXPressoNodes()
    if not selected_nodes:
        print("Keine Nodes ausgewählt.")
        return

    for node in selected_nodes:
        for param_name in clipboard_parameters:
            if param_name in parameter_map:
                param_id = parameter_map[param_name]
                port = node.AddPort(c4d.GV_PORT_OUTPUT, param_id)
                if port:
                    port.SetName(param_name)
                    print(f"Port '{param_name}' hinzugefügt mit ID {param_id}.")

    c4d.EventAdd()

def main():
    AddPortsFromClipboard()

if __name__ == "__main__":
    main()
