"""
SV Unmark Takes

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:Unmarks all takes in the take system.

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def mark_last_level_takes(takeData):
    mainTake = takeData.GetMainTake()
    if not mainTake:
        return

    def mark_last_level_recursive(take):
        if not take.GetDown():
            take.SetChecked(True)
        else:
            child = take.GetDown()
            while child:
                mark_last_level_recursive(child)
                child = child.GetNext()

    mark_last_level_recursive(mainTake)

def main():
    doc = c4d.documents.GetActiveDocument()
    takeData = doc.GetTakeData()
    
    if not takeData:
        return
    
    mark_all_takes(takeData)

    c4d.EventAdd()

def mark_all_takes(takeData):
    mainTake = takeData.GetMainTake()
    if not mainTake:
        return

    def mark_takes_recursive(take):
        take.SetChecked(False)

        child = take.GetDown()
        while child:
            mark_takes_recursive(child)
            child = child.GetNext()

    mark_takes_recursive(mainTake)

if __name__ == '__main__':
    main()
