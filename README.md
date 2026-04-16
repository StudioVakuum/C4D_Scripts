# C4D_Scripts

Collection of Cinema 4D Python scripts by Studio Vakuum.

## Studio Vakuum Scripts

### Modeling

![SV Center to Global Zero](Icons/SV%20Center%20to%20Global%20Zero.png)
- `SV Center to Global Zero`
  Sets the selected object's axis to global zero while preserving the global position and axis of its children.

### Object Manager

![SV Parent Name to Children](Icons/SV%20Parent%20Name%20to%20Children.png)
- `SV Parent Name to Children`
  Renames children based on the parent object name. Supports specific hierarchy levels and optional numeric suffixes.

![SV Paste Objects as Children](Icons/SV%20Paste%20Objects%20as%20Children.png)
- `SV Paste Objects as Children`
  Pastes clipboard objects as children under each selected object.

![SV Paste Objects as Parent](Icons/SV%20Paste%20Objects%20as%20Parent.png)
- `SV Paste Objects as Parent`
  Pastes clipboard objects above the selected objects and inserts the selected objects under the deepest pasted child.

### Takes

![SV Current Take Next](Icons/SV%20Current%20Take%20Next.png)
- `SV Current Take Next`
  Switches to the next take in the Take Manager. With `Shift`, it navigates through leaf takes without stopping on parent takes.

![SV Current Take Previous](Icons/SV%20Current%20Take%20Previous.png)
- `SV Current Take Previous`
  Switches to the previous take in the Take Manager. With `Shift`, it navigates through leaf takes only.

![SV Current Marked Take Next](Icons/SV%20Current%20Marked%20Take%20Next.png)
- `SV Current Marked Take Next`
  Switches to the next checked or marked take in the Take Manager.

![SV Current Marked Take Previous](Icons/SV%20Current%20Marked%20Take%20Previous.png)
- `SV Current Marked Take Previous`
  Switches to the previous checked or marked take in the Take Manager.

![SV Mark Takes](Icons/SV%20Mark%20Takes.png)
- `SV Mark Takes`
  Marks takes in different ways depending on modifier keys: all takes, selected takes, deepest level, higher levels, or leaf-only takes.

![SV Unmark Takes](Icons/SV%20Unmark%20Takes.png)
- `SV Unmark Takes`
  Clears take marks for all takes or only the currently selected take branches.

### User Data

![SV Copy for Cycle](Icons/SV%20Copy%20for%20Cycle.png)
- `SV Copy for Cycle`
  Copies selected object or material names to the clipboard in a format that can be reused for cycle user data entries.

![SV Create Bool](Icons/SV%20Create%20Bool.png)
- `SV Create Bool`
  Adds a boolean user data field to the selected object.

![SV Create Color](Icons/SV%20Create%20Color.png)
- `SV Create Color`
  Adds a color user data field to the selected object.

![SV Create Cycle](Icons/SV%20Create%20Cycle.png)
- `SV Create Cycle`
  Adds an empty cycle user data field to the selected object.

![SV Create Cycle from Clipboard](Icons/SV%20Create%20Cycle%20from%20Clipboard.png)
- `SV Create Cycle from Clipboard`
  Creates a cycle user data field from clipboard data prepared with `SV Copy for Cycle`.

![SV Create Float](Icons/SV%20Create%20Float.png)
- `SV Create Float`
  Adds a float user data field to the selected object, with optional unit selection such as length, percent, or degree.

![SV Create Folder Path](Icons/SV%20Create%20Folder%20Path.png)
- `SV Create Folder Path`
  Opens a folder picker and stores the chosen folder path as a string user data field on the selected object.

![SV Create Folder Tex Path](Icons/SV%20Create%20Folder%20Tex%20Path.png)
- `SV Create Folder Tex Path`
  Adds the current project `tex` folder path as a string user data field on the selected object.

![SV Create Integer](Icons/SV%20Create%20Integer.png)
- `SV Create Integer`
  Adds an integer user data field to the selected object.

![SV Create String](Icons/SV%20Create%20String.png)
- `SV Create String`
  Adds a string user data field to the selected object.

![SV Create Vector](Icons/SV%20Create%20Vector.png)
- `SV Create Vector`
  Adds a vector user data field to the selected object, with optional unit selection.
