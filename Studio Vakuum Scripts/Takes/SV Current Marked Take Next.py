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

def find_last_checked_take_in_group(take):
    if not take:
        return None
        
    last_checked = None
    current = take
    
    while current.GetNext():
        current = current.GetNext()
    
    while current:
        if has_children(current):
            child_result = find_last_checked_take_in_group(current.GetDown())
            if child_result:
                return child_result
                
        if is_take_checked(current):
            return current
                
        current = current.GetPred()
    
    return None

def find_previous_checked_take(current_take):
    prev_sibling = current_take.GetPred()
    while prev_sibling:
        if has_children(prev_sibling):
            last_checked = find_last_checked_take_in_group(prev_sibling.GetDown())
            if last_checked:
                return last_checked
        
        if is_take_checked(prev_sibling):
            return prev_sibling
                
        prev_sibling = prev_sibling.GetPred()
    
    parent = current_take.GetUp()
    if parent:
        if is_take_checked(parent):
            return parent
        return find_previous_checked_take(parent)
    
    root = current_take
    while root.GetUp():
        root = root.GetUp()
        
    if has_children(root):
        last_in_children = find_last_checked_take_in_group(root.GetDown())
        if last_in_children:
            return last_in_children
            
    last_at_root = root
    while last_at_root.GetNext():
        last_at_root = last_at_root.GetNext()
        
    while last_at_root:
        if is_take_checked(last_at_root):
            return last_at_root
        last_at_root = last_at_root.GetPred()
    
    return None

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