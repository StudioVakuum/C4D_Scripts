# C4D_Scripts

Collection of Cinema 4D Python scripts by Studio Vakuum.

## Studio Vakuum Scripts

### Modeling

- `SV Center to Global Zero`
  Sets the selected object's axis to global zero while preserving the global position and axis of its children.

### Object Manager

- `SV Parent Name to Children`
  Renames children based on the parent object name. Supports specific hierarchy levels and optional numeric suffixes.

- `SV Paste Objects as Children`
  Pastes clipboard objects as children under each selected object.

- `SV Paste Objects as Parent`
  Pastes clipboard objects above the selected objects and inserts the selected objects under the deepest pasted child.

### Takes

- `SV Current Take Next`
  Switches to the next take in the Take Manager. With `Shift`, it navigates through leaf takes without stopping on parent takes.

- `SV Current Take Previous`
  Switches to the previous take in the Take Manager. With `Shift`, it navigates through leaf takes only.

- `SV Current Marked Take Next`
  Switches to the next checked or marked take in the Take Manager.

- `SV Current Marked Take Previous`
  Switches to the previous checked or marked take in the Take Manager.

- `SV Mark Takes`
  Marks takes in different ways depending on modifier keys: all takes, selected takes, deepest level, higher levels, or leaf-only takes.

- `SV Unmark Takes`
  Clears take marks for all takes or only the currently selected take branches.

### User Data

- `SV Copy for Cycle`
  Copies selected object or material names to the clipboard in a format that can be reused for cycle user data entries.

- `SV Create Bool`
  Adds a boolean user data field to the selected object.

- `SV Create Color`
  Adds a color user data field to the selected object.

- `SV Create Cycle`
  Adds an empty cycle user data field to the selected object.

- `SV Create Cycle from Clipboard`
  Creates a cycle user data field from clipboard data prepared with `SV Copy for Cycle`.

- `SV Create Float`
  Adds a float user data field to the selected object, with optional unit selection such as length, percent, or degree.

- `SV Create Folder Path`
  Opens a folder picker and stores the chosen folder path as a string user data field on the selected object.

- `SV Create Folder Tex Path`
  Adds the current project `tex` folder path as a string user data field on the selected object.

- `SV Create Integer`
  Adds an integer user data field to the selected object.

- `SV Create String`
  Adds a string user data field to the selected object.

- `SV Create Vector`
  Adds a vector user data field to the selected object, with optional unit selection.
