"""
SV Current Take Next

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:Jumps down to the next take in the take system.<br>SHIFT: Doesn't skip parent takes with children.

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def has_children(take):
    return take.GetDown() is not None

def find_next_take(current_take):
    child_take = current_take.GetDown()
    if child_take:
        return child_take
    
    next_sibling = current_take.GetNext()
    if next_sibling:
        return next_sibling
    
    parent = current_take.GetUp()
    while parent:
        next_sibling = parent.GetNext()
        if next_sibling:
            return next_sibling
        parent = parent.GetUp()
    
    return None

def find_next_leaf_take(current_take):
    next_sibling = current_take.GetNext()
    
    if next_sibling:
        if not has_children(next_sibling):
            return next_sibling
        child = next_sibling.GetDown()
        while child:
            if not has_children(child):
                return child
            child = child.GetDown()
        return find_next_leaf_take(next_sibling)
    
    parent = current_take.GetUp()
    while parent:
        next_parent_sibling = parent.GetNext()
        if next_parent_sibling:
            if not has_children(next_parent_sibling):
                return next_parent_sibling
            child = next_parent_sibling.GetDown()
            while child:
                if not has_children(child):
                    return child
                child = child.GetDown()
            return find_next_leaf_take(next_parent_sibling)
        parent = parent.GetUp()
    
    return None

def jump_to_next_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    next_take = find_next_take(current_take)
    
    if not next_take:
        main_take = take_data.GetMainTake()
        if main_take:
            next_take = main_take.GetDown()
    
    if next_take:
        take_data.SetCurrentTake(next_take)
        c4d.EventAdd()

def find_first_leaf_take(take):
    if not has_children(take):
        return take
    
    child = take.GetDown()
    while child:
        if not has_children(child):
            return child
        child = child.GetDown()
    return None

def jump_to_next_leaf_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    if has_children(current_take):
        next_take = find_first_leaf_take(current_take)
    else:
        next_take = find_next_leaf_take(current_take)
    
    if not next_take:
        main_take = take_data.GetMainTake()
        if main_take:
            next_take = find_first_leaf_take(main_take)
    
    if next_take:
        take_data.SetCurrentTake(next_take)
        c4d.EventAdd()

def main():
    doc = c4d.documents.GetActiveDocument()
    bc = c4d.BaseContainer()
    shift_pressed = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_SHIFT, bc) and bc[c4d.BFM_INPUT_VALUE]
    
    if shift_pressed:
        jump_to_next_take(doc)
    else:
        jump_to_next_leaf_take(doc)

if __name__ == "__main__":
    main()
