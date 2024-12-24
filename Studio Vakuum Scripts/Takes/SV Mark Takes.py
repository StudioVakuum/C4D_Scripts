"""
SV Mark Takes

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:DEFAULT: Marks all takes in the take system or only those selected and its children.<br>SHIFT: Marks all takes at the lowest hierarchy level.<br>CTRL: Marks takes at the next higher hierarchy level, maintaining previous marks.<br>ALT: Marks takes at the next higher hierarchy level, disregarding previous marks.

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

CUSTOM_ID_LEVEL = 1056789

def get_hierarchy_depth(take):
    depth = 0
    while take.GetUp():
        depth += 1
        take = take.GetUp()
    return depth

def get_max_depth(take):
    current_depth = get_hierarchy_depth(take)
    max_depth = current_depth

    child = take.GetDown()
    while child:
        child_depth = get_max_depth(child)
        max_depth = max(max_depth, child_depth)
        child = child.GetNext()

    return max_depth

def mark_takes_at_level(takeData, target_level, selected_takes=None):
    def mark_level_recursive(take):
        current_depth = get_hierarchy_depth(take)
        if selected_takes is None or take in selected_takes:
            take.SetChecked(current_depth == target_level)

        child = take.GetDown()
        while child:
            mark_level_recursive(child)
            child = child.GetNext()

    mainTake = takeData.GetMainTake()
    if mainTake:
        mark_level_recursive(mainTake)

def mark_takes_at_next_level(takeData, target_level, selected_takes=None):
    def mark_level_recursive(take):
        current_depth = get_hierarchy_depth(take)
        if selected_takes is None or take in selected_takes:
            if current_depth == target_level:
                take.SetChecked(True)

        child = take.GetDown()
        while child:
            mark_level_recursive(child)
            child = child.GetNext()

    mainTake = takeData.GetMainTake()
    if mainTake:
        mark_level_recursive(mainTake)

def get_stored_level(doc, max_level):
    bc = doc.GetDataInstance()
    return bc.GetInt32(CUSTOM_ID_LEVEL, max_level)

def store_level(doc, level):
    bc = doc.GetDataInstance()
    bc.SetInt32(CUSTOM_ID_LEVEL, level)

def mark_all_takes(takeData, selected_takes=None):
    def mark_takes_recursive(take):
        if selected_takes is None or take in selected_takes:
            take.SetChecked(True)
        child = take.GetDown()
        while child:
            mark_takes_recursive(child)
            child = child.GetNext()

    mainTake = takeData.GetMainTake()
    if mainTake:
        mark_takes_recursive(mainTake)

def main():
    doc = c4d.documents.GetActiveDocument()
    takeData = doc.GetTakeData()

    if not takeData:
        return

    selected_takes = takeData.GetTakeSelection(True)
    if not selected_takes:
        selected_takes = None

    bc = c4d.BaseContainer()
    shift_pressed = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_SHIFT, bc) and bc[c4d.BFM_INPUT_VALUE]
    ctrl_pressed = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_CONTROL, bc) and bc[c4d.BFM_INPUT_VALUE]
    alt_pressed = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ALT, bc) and bc[c4d.BFM_INPUT_VALUE]

    max_level = get_max_depth(takeData.GetMainTake())

    if shift_pressed:
        store_level(doc, max_level)
        mark_takes_at_level(takeData, max_level, selected_takes)
    elif ctrl_pressed:
        current_level = get_stored_level(doc, max_level)
        next_level = current_level - 1 if current_level > 0 else max_level
        store_level(doc, next_level)
        mark_takes_at_next_level(takeData, next_level, selected_takes)
    elif alt_pressed:
        current_level = get_stored_level(doc, max_level)
        next_level = current_level - 1 if current_level > 0 else max_level
        store_level(doc, next_level)
        mark_takes_at_level(takeData, next_level, selected_takes)
    else:
        mark_all_takes(takeData, selected_takes)
        store_level(doc, max_level)

    c4d.EventAdd()

if __name__ == '__main__':
    main()
