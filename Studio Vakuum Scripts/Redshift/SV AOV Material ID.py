"""
SV AOV Material ID

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Assigns Material IDs to selected Redshift materials and automatically creates Puzzle Matte AOVs to output them.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d
import maxon
import redshift
from c4d import documents

# ====================== SETTINGS ======================
RS_NODESPACE = maxon.Id("com.redshift3d.redshift4c4d.class.nodespace")
MATERIAL_ID_PORT = "com.redshift3d.redshift4c4d.node.output.materialid"

# ====================== FUNCTIONS ======================
def get_selected_materials(doc):
    active = doc.GetActiveMaterial()
    if active:
        return [active]
    return [m for m in doc.GetMaterials() if m.GetBit(c4d.BIT_ACTIVE)]

def set_material_id(graph: maxon.NodesGraphModelRef, mat_id: int):
    if graph.IsNullValue():
        return False
    nodes = []
    graph.GetViewRoot().GetChildren(nodes, maxon.NODE_KIND.NODE)

    for node in nodes:
        asset_id = node.GetValue("net.maxon.node.attribute.assetid")
        if asset_id and "output" in str(asset_id[0]).lower():
            port = node.GetInputs().FindChild(MATERIAL_ID_PORT)
            if port:
                with graph.BeginTransaction() as t:
                    port.SetPortValue(int(mat_id))
                    t.Commit()
                return True
    return False

def create_puzzle_matte_aovs(vp_rs, num_materials: int):
    """Create enough Puzzle Matte AOVs for all materials (3 IDs per AOV)"""
    if num_materials < 1:
        return False

    aovs = redshift.RendererGetAOVs(vp_rs)

    aov_index = 1
    mat_id = 1

    while mat_id <= num_materials:
        aov = redshift.RSAOV()
        aov.SetParameter(c4d.REDSHIFT_AOV_TYPE, c4d.REDSHIFT_AOV_TYPE_PUZZLE_MATTE)
        aov.SetParameter(c4d.REDSHIFT_AOV_ENABLED, True)
        aov.SetParameter(c4d.REDSHIFT_AOV_NAME, f"PuzzleMatte_{aov_index:02d}")
        aov.SetParameter(c4d.REDSHIFT_AOV_MULTIPASS_ENABLED, True)

        # Use Material ID mode
        aov.SetParameter(c4d.REDSHIFT_AOV_PUZZLE_MATTE_MODE,
                        c4d.REDSHIFT_AOV_PUZZLE_MATTE_MODE_MATERIAL_ID)

        # Assign up to 3 Material IDs per AOV
        red_id   = mat_id
        green_id = mat_id + 1 if mat_id + 1 <= num_materials else 0
        blue_id  = mat_id + 2 if mat_id + 2 <= num_materials else 0

        aov.SetParameter(c4d.REDSHIFT_AOV_PUZZLE_MATTE_RED_ID, red_id)
        aov.SetParameter(c4d.REDSHIFT_AOV_PUZZLE_MATTE_GREEN_ID, green_id)
        aov.SetParameter(c4d.REDSHIFT_AOV_PUZZLE_MATTE_BLUE_ID, blue_id)

        aovs.append(aov)

        mat_id += 3
        aov_index += 1

    # Apply all AOVs
    return redshift.RendererSetAOVs(vp_rs, aovs)

# ====================== MAIN ======================
doc = documents.GetActiveDocument()
if not doc:
    # You can add a dialog here if you want feedback
    pass
else:
    # 1. Set Material IDs on selected materials
    materials = get_selected_materials(doc)
    for i, mat in enumerate(materials, start=1):
        if not mat:
            continue
        node_mat = mat.GetNodeMaterialReference()
        if not node_mat:
            continue
        graph = node_mat.GetGraph(RS_NODESPACE)
        if not graph.IsNullValue():
            set_material_id(graph, i)

    # 2. Create Puzzle Matte AOVs
    render_data = doc.GetActiveRenderData()
    vp_rs = redshift.FindAddVideoPost(render_data, redshift.VPrsrenderer)

    if vp_rs:
        render_data[c4d.RDATA_RENDERENGINE] = redshift.VPrsrenderer
        success = create_puzzle_matte_aovs(vp_rs, len(materials))

    c4d.EventAdd()