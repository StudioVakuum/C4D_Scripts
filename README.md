# C4D_Scripts

Collection of Cinema 4D Python scripts by Studio Vakuum.

<details>
<summary><h3>Modeling</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Axis%20Orientation.png" alt="SV Axis Orientation" width="96">
    </td>
    <td>
      <h3>SV Axis Orientation</h3>
      Rotates the selected object axis orientation without changing the visible object position, mesh shape, or child transforms.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Center%20to%20Global%20Zero.png" alt="SV Center to Global Zero" width="96">
    </td>
    <td>
      <h3>SV Center to Global Zero</h3>
      Sets the selected object's axis to global zero while preserving the global position and axis of its children.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Centered%20Spline.png" alt="SV Create Centered Spline" width="96">
    </td>
    <td>
      <h3>SV Create Centered Spline</h3>
      Creates a linear spline through the center points of selected edge loops on a polygon object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Quad%20Circle.png" alt="SV Quad Circle" width="96">
    </td>
    <td>
      <h3>SV Quad Circle</h3>
      Creates a circular quad layout from selected points, with controls for radius accuracy and curvature.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Snap%20Points%20to%20Spline.png" alt="SV Snap Points to Spline" width="96">
    </td>
    <td>
      <h3>SV Snap Points to Spline</h3>
      Snaps selected polygon points or selected edge endpoints to the closest position on one or more selected splines.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Symmetry%20Delete.png" alt="SV Symmetry Delete" width="96">
    </td>
    <td>
      <h3>SV Symmetry Delete</h3>
      Deletes points symmetrically based on the chosen axis, side, tolerance, and world or object space.<br><br>
    </td>
  </tr>
</table>

</details>

<details>
<summary><h3>Object Manager</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Block%20HDR%20Light%20Studio%20Visibility.png" alt="SV Block HDR Light Studio Visibility" width="96">
    </td>
    <td>
      <h3>SV Block HDR Light Studio Visibility</h3>
      Adds a visibility-lock Python tag to selected objects with a Default, On, or Off mode for editor and render visibility.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Children%20Name%20to%20Parent.png" alt="SV Children Name to Parent" width="96">
    </td>
    <td>
      <h3>SV Children Name to Parent</h3>
      Renames parent objects from the selected child object names, with support for specific hierarchy levels and optional suffixes.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Instance%20Delete%20Unselected.png" alt="SV Instance Delete Unselected" width="96">
    </td>
    <td>
      <h3>SV Instance Delete Unselected</h3>
      Deletes unselected objects while preserving the selected objects, their hierarchies, and linked instance references.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Instance%20Inherit%20Name.png" alt="SV Instance Inherit Name" width="96">
    </td>
    <td>
      <h3>SV Instance Inherit Name</h3>
      Renames selected Instance objects to match the names of their linked reference objects.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Instance.png" alt="SV Instances" width="96">
    </td>
    <td>
      <h3>SV Instances</h3>
      <strong>Default:</strong> Creates an instance object for each selected item.<br>
      <strong>Shift:</strong> Creates a clean duplicate hierarchy of structural Nulls.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Parent%20Name%20to%20Children.png" alt="SV Parent Name to Children" width="96">
    </td>
    <td>
      <h3>SV Parent Name to Children</h3>
      Renames children based on the parent object name. Supports specific hierarchy levels and optional numeric suffixes.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Paste%20Objects%20as%20Children.png" alt="SV Paste Objects as Children" width="96">
    </td>
    <td>
      <h3>SV Paste Objects as Children</h3>
      Pastes clipboard objects as children under each selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Paste%20Objects%20as%20Parent.png" alt="SV Paste Objects as Parent" width="96">
    </td>
    <td>
      <h3>SV Paste Objects as Parent</h3>
      Pastes clipboard objects above the selected objects and inserts the selected objects under the deepest pasted child.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Trim%20Name.png" alt="SV Trim Object Names" width="96">
    </td>
    <td>
      <h3>SV Trim Object Names</h3>
      Removes a chosen number of characters from the start or end of selected object names.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Reorder%20Tags.png" alt="SV Reorder Tags" width="96">
    </td>
    <td>
      <h3>SV Reorder Tags</h3>
      Reorders visible tags on selected objects to match the first selected object with tags, without creating, deleting, renaming, or copying tags.<br><br>
    </td>
  </tr>
</table>

</details>

<details>
<summary><h3>Redshift</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20RS%20MultiConnect%20Nodes.png" alt="SV RS MultiConnect Nodes" width="96">
    </td>
    <td>
      <h3>SV RS MultiConnect Nodes</h3>
      Connects selected Redshift nodes to a selected target node using manually defined source ordering.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20RS%20Texture%20Shader%20Switch.png" alt="SV RS Texture Shader Switch" width="96">
    </td>
    <td>
      <h3>SV RS Texture Shader Switch</h3>
      Creates texture sampler nodes from selected image files and connects them to Redshift Shader Switch nodes.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20AOV%20Material%20ID.png" alt="SV AOV Material ID" width="96">
    </td>
    <td>
      <h3>SV AOV Material ID</h3>
      Assigns Material IDs to selected Redshift materials and creates Puzzle Matte AOVs to output those IDs.<br><br>
    </td>
  </tr>
</table>

</details>

<details>
<summary><h3>Takes</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Take%20Next.png" alt="SV Current Take Next" width="96">
    </td>
    <td>
      <h3>SV Current Take Next</h3>
      <strong>Default:</strong> Switches to the next leaf take in the Take Manager, skipping parent takes with children.<br>
      <strong>Shift:</strong> Switches to the next take without skipping parent takes with children.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Take%20Previous.png" alt="SV Current Take Previous" width="96">
    </td>
    <td>
      <h3>SV Current Take Previous</h3>
      <strong>Default:</strong> Switches to the previous leaf take in the Take Manager, skipping parent takes with children.<br>
      <strong>Shift:</strong> Switches to the previous take without skipping parent takes with children.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Marked%20Take%20Next.png" alt="SV Current Marked Take Next" width="96">
    </td>
    <td>
      <h3>SV Current Marked Take Next</h3>
      Switches to the next checked or marked take in the Take Manager.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Marked%20Take%20Previous.png" alt="SV Current Marked Take Previous" width="96">
    </td>
    <td>
      <h3>SV Current Marked Take Previous</h3>
      Switches to the previous checked or marked take in the Take Manager.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Mark%20Takes.png" alt="SV Mark Takes" width="96">
    </td>
    <td>
      <h3>SV Mark Takes</h3>
      <strong>Default:</strong> Marks all takes in the Take Manager, or the selected takes and their children when takes are selected.<br>
      <strong>Shift:</strong> Marks all takes at the lowest hierarchy level.<br>
      <strong>Ctrl:</strong> Marks takes at the next higher hierarchy level while keeping previous marks.<br>
      <strong>Alt:</strong> Marks takes at the next higher hierarchy level and clears previous marks.<br>
      <strong>Shift + Ctrl:</strong> Marks takes that have no children.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Unmark%20Takes.png" alt="SV Unmark Takes" width="96">
    </td>
    <td>
      <h3>SV Unmark Takes</h3>
      Clears take marks for all takes or only the currently selected take branches.<br><br>
    </td>
  </tr>
</table>

</details>

<details>
<summary><h3>XPresso</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Condition%20Create%20Materials.png" alt="SV Create Material Op + Condition" width="96">
    </td>
    <td>
      <h3>SV Create Material Op + Condition</h3>
      Creates Material Operator nodes from selected materials and connects them to a Condition node.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Manage%20Condition%20Inputs.png" alt="SV Manage Inputs" width="96">
    </td>
    <td>
      <h3>SV Manage Inputs</h3>
      Adds or removes input ports on selected XPresso nodes such as Condition or Math nodes and adjusts their size.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20MultiConnect%20Nodes.png" alt="SV MultiConnect Nodes" width="96">
    </td>
    <td>
      <h3>SV MultiConnect Nodes</h3>
      Automatically connects multiple selected source nodes to the free input ports of a target node.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Copy%20Outports.png" alt="SV Copy Outports" width="96">
    </td>
    <td>
      <h3>SV Copy Outports</h3>
      Copies the output port names of the selected XPresso node to the clipboard for reuse in other nodes.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Paste%20Outports.png" alt="SV Paste Outports" width="96">
    </td>
    <td>
      <h3>SV Paste Outports</h3>
      Adds output ports to the selected XPresso nodes from parameter names stored in the clipboard.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Material%20Op.png" alt="SV Create Material Op" width="96">
    </td>
    <td>
      <h3>SV Create Material Op</h3>
      Creates Material Operator nodes in the selected XPresso tag from the currently selected materials.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Condition%20Create%20Objects.png" alt="SV Create Objects Op + Condition" width="96">
    </td>
    <td>
      <h3>SV Create Objects Op + Condition</h3>
      Creates Object Operator nodes from selected objects and connects them to a Condition node.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Objects%20Op.png" alt="SV Create Objects Op" width="96">
    </td>
    <td>
      <h3>SV Create Objects Op</h3>
      Creates Object Operator nodes in the selected XPresso tag from the currently selected objects.<br><br>
    </td>
  </tr>  
</table>

</details>

<details>
<summary><h3>User Data</h3></summary>

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Copy%20for%20Cycle.png" alt="SV Copy for Cycle" width="96">
    </td>
    <td>
      <h3>SV Copy for Cycle</h3>
      Copies selected object or material names to the clipboard in a format that can be reused for cycle user data entries.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Bool.png" alt="SV Create Bool" width="96">
    </td>
    <td>
      <h3>SV Create Bool</h3>
      Adds a boolean user data field to the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Color.png" alt="SV Create Color" width="96">
    </td>
    <td>
      <h3>SV Create Color</h3>
      Adds a color user data field to the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Cycle.png" alt="SV Create Cycle" width="96">
    </td>
    <td>
      <h3>SV Create Cycle</h3>
      Adds an empty cycle user data field to the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Cycle%20from%20Clipboard.png" alt="SV Create Cycle from Clipboard" width="96">
    </td>
    <td>
      <h3>SV Create Cycle from Clipboard</h3>
      Creates a cycle user data field from clipboard data prepared with <code>SV Copy for Cycle</code>.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="./Icons/SV Create Float.png" alt="SV Create Float" width="96">
    </td>
    <td>
      <h3>SV Create Float</h3>
      Adds a float user data field to the selected object, with optional unit selection such as length, percent, or degree.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Folder%20Path.png" alt="SV Create Folder Path" width="96">
    </td>
    <td>
      <h3>SV Create Folder Path</h3>
      Opens a folder picker and stores the chosen folder path as a string user data field on the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Folder%20Tex%20Path.png" alt="SV Create Folder Tex Path" width="96">
    </td>
    <td>
      <h3>SV Create Folder Tex Path</h3>
      Adds the current project <code>tex</code> folder path as a string user data field on the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Integer.png" alt="SV Create Integer" width="96">
    </td>
    <td>
      <h3>SV Create Integer</h3>
      Adds an integer user data field to the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20String.png" alt="SV Create String" width="96">
    </td>
    <td>
      <h3>SV Create String</h3>
      Adds a string user data field to the selected object.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Create%20Vector.png" alt="SV Create Vector" width="96">
    </td>
    <td>
      <h3>SV Create Vector</h3>
      Adds a vector user data field to the selected object, with optional unit selection.<br><br>
    </td>
  </tr>
</table>

</details>
