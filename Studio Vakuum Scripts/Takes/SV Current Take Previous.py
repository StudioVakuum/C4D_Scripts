"""
SV Current Take Previous

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:Jumps up to the previous take in the take system.<br>SHIFT: Doesn't skip parent takes with children.

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def has_children(take):
    return take.GetDown() is not None

def find_previous_take(current_take):
    prev_sibling = current_take.GetPred()
    if prev_sibling:
        while has_children(prev_sibling):
            prev_sibling = prev_sibling.GetDown()
            while prev_sibling.GetNext():
                prev_sibling = prev_sibling.GetNext()
        return prev_sibling
    
    parent = current_take.GetUp()
    if parent:
        return parent
    
    root = current_take
    while root.GetUp():
        root = root.GetUp()
    
    last_take = root
    while last_take.GetNext() or last_take.GetDown():
        if last_take.GetNext():
            last_take = last_take.GetNext()
        elif last_take.GetDown():
            last_take = last_take.GetDown()
    
    return last_take

def find_previous_leaf_take(current_take):
    prev_sibling = current_take.GetPred()
    
    if prev_sibling:
        if has_children(prev_sibling):
            last_child = prev_sibling
            while has_children(last_child):
                last_child = last_child.GetDown()
                while last_child.GetNext():
                    last_child = last_child.GetNext()
            return last_child
        return prev_sibling
    
    parent = current_take.GetUp()
    while parent:
        prev_parent_sibling = parent.GetPred()
        if prev_parent_sibling:
            if not has_children(prev_parent_sibling):
                return prev_parent_sibling
            last_child = prev_parent_sibling
            while has_children(last_child):
                last_child = last_child.GetDown()
                while last_child.GetNext():
                    last_child = last_child.GetNext()
            return last_child
        parent = parent.GetUp()
    
    root = current_take
    while root.GetUp():
        root = root.GetUp()
    
    last_take = root
    while last_take.GetNext() or last_take.GetDown():
        if last_take.GetNext():
            last_take = last_take.GetNext()
        elif last_take.GetDown():
            last_take = last_take.GetDown()
    
    return last_take if not has_children(last_take) else find_previous_leaf_take(last_take)

def find_last_leaf_take(take):
    if not has_children(take):
        return take
    
    last_child = take.GetDown()
    while last_child.GetNext():
        last_child = last_child.GetNext()
    
    return find_last_leaf_take(last_child)

def jump_to_previous_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    prev_take = find_previous_take(current_take)
    
    if prev_take:
        take_data.SetCurrentTake(prev_take)
        c4d.EventAdd()

def jump_to_previous_leaf_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    prev_take = find_previous_leaf_take(current_take)
    
    if prev_take:
        take_data.SetCurrentTake(prev_take)
        c4d.EventAdd()

def main():
    doc = c4d.documents.GetActiveDocument()
    bc = c4d.BaseContainer()
    shift_pressed = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_SHIFT, bc) and bc[c4d.BFM_INPUT_VALUE]
    
    if shift_pressed:
        jump_to_previous_take(doc)
    else:
        jump_to_previous_leaf_take(doc)

if __name__ == "__main__":
    main()