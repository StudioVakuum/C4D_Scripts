# C4D_Scripts

Collection of Cinema 4D Python scripts by Studio Vakuum.

### Modeling

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Center%20to%20Global%20Zero.png" alt="SV Center to Global Zero" width="96">
    </td>
    <td>
      <h3>SV Center to Global Zero</h3>
      Sets the selected object's axis to global zero while preserving the global position and axis of its children.<br><br>
    </td>
  </tr>
</table>

### Object Manager

<table>
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
</table>

### Takes

<table>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Take%20Next.png" alt="SV Current Take Next" width="96">
    </td>
    <td>
      <h3>SV Current Take Next</h3>
      Switches to the next take in the Take Manager. With <code>Shift</code>, it navigates through leaf takes without stopping on parent takes.<br><br>
    </td>
  </tr>
  <tr>
    <td width="96">
      <img src="Icons/SV%20Current%20Take%20Previous.png" alt="SV Current Take Previous" width="96">
    </td>
    <td>
      <h3>SV Current Take Previous</h3>
      Switches to the previous take in the Take Manager. With <code>Shift</code>, it navigates through leaf takes only.<br><br>
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
      Marks takes in different ways depending on modifier keys: all takes, selected takes, deepest level, higher levels, or leaf-only takes.<br><br>
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

### User Data

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
