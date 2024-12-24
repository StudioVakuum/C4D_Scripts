"""
SV Current Marked Take Previous

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:Jumps up to the previous marked take in the take system.

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

def find_last_checked_take_in_group(take):
    if not take:
        return None
        
    last_checked = None
    current = take
    
    while current.GetNext():
        current = current.GetNext()
    
    while current:
        if is_take_checked(current) and not has_checked_children(current):
            return current
            
        if has_checked_children(current):
            child_result = find_last_checked_take_in_group(current.GetDown())
            if child_result:
                return child_result
                
        current = current.GetPred()
    
    return None

def find_previous_checked_take(current_take):
    prev_sibling = current_take.GetPred()
    while prev_sibling:
        if is_take_checked(prev_sibling) and not has_checked_children(prev_sibling):
            return prev_sibling
            
        if has_checked_children(prev_sibling):
            last_checked = find_last_checked_take_in_group(prev_sibling.GetDown())
            if last_checked:
                return last_checked
                
        prev_sibling = prev_sibling.GetPred()
    
    parent = current_take.GetUp()
    if parent:
        if is_take_checked(parent) and not has_other_checked_children(parent, current_take):
            return parent
        return find_previous_checked_take(parent)
    
    root = current_take
    while root.GetUp():
        root = root.GetUp()
    
    return find_last_checked_take_in_group(root)

def has_other_checked_children(parent, exclude_take):
    if not has_children(parent):
        return False
        
    child = parent.GetDown()
    while child:
        if child != exclude_take:
            if is_take_checked(child) or has_checked_children(child):
                return True
        child = child.GetNext()
    return False

def jump_to_previous_take(doc):
    take_data = doc.GetTakeData()
    if not take_data:
        return
    
    current_take = take_data.GetCurrentTake()
    if not current_take:
        return
    
    prev_take = find_previous_checked_take(current_take)
    if prev_take:
        take_data.SetCurrentTake(prev_take)
        c4d.EventAdd()

def main():
    doc = c4d.documents.GetActiveDocument()
    jump_to_previous_take(doc)

if __name__ == "__main__":
    main()