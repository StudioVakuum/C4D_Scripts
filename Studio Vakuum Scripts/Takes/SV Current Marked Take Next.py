"""
SV Current Marked Take Next

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:Jumps down to the next marked take in the take system.

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def is_take_checked(take):
    return take.IsChecked()

def has_children(take):
    return take.GetDown() is not None

def has_checked_children(take):
    if not has_children(take):
        return False
    child = take.GetDown()
    while child:
        if is_take_checked(child) or has_checked_children(child):
            return True
        child = child.GetNext()
    return False

def find_next_checked_take(current_take):
    if has_children(current_take):
        child = current_take.GetDown()
        while child:
            if is_take_checked(child):
                return child
            if has_checked_children(child):
                return find_first_checked_take(child)
            child = child.GetNext()
    
    next_sibling = current_take.GetNext()
    while next_sibling:
        if is_take_checked(next_sibling):
            return next_sibling
        if has_checked_children(next_sibling):
            return find_first_checked_take(next_sibling)
        next_sibling = next_sibling.GetNext()
    
    parent = current_take.GetUp()
    while parent:
        next_parent = parent.GetNext()
        while next_parent:
            if is_take_checked(next_parent):
                return next_parent
            if has_checked_children(next_parent):
                return find_first_checked_take(next_parent)
            next_parent = next_parent.GetNext()
        parent = parent.GetUp()
    
    return None

def find_first_checked_take(take):
    if not take:
        return None
    
    if is_take_checked(take):
        return take
    
    child = take.GetDown()
    while child:
        if is_take_checked(child):
            return child
        result = find_first_checked_take(child)
        if result:
            return result
        child = child.GetNext()
    
    return None

def jump_to_next_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    next_take = find_next_checked_take(current_take)
    if not next_take:
        main_take = take_data.GetMainTake()
        if main_take:
            next_take = find_first_checked_take(main_take)
    
    if next_take:
        take_data.SetCurrentTake(next_take)
        c4d.EventAdd()

def main():
    doc = c4d.documents.GetActiveDocument()
    jump_to_next_take(doc)

if __name__ == "__main__":
    main()