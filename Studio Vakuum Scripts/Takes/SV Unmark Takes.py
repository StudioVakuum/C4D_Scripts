"""
SV Unmark Takes
Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US:Unmarks all takes in the take system or only the selected ones (and their children).
Written for Maxon Cinema 4D 2026.1.4
Python version 3.11.4
"""
import c4d

def unmark_takes(takeData, selected_takes=None):
    mainTake = takeData.GetMainTake()
    if not mainTake:
        return
    
    def unmark_recursive(take):
        if selected_takes is None or take in selected_takes:
            take.SetChecked(False)
        
        child = take.GetDown()
        while child:
            unmark_recursive(child)
            child = child.GetNext()
    
    unmark_recursive(mainTake)

def main():
    doc = c4d.documents.GetActiveDocument()
    takeData = doc.GetTakeData()
    if not takeData:
        return

    selected_takes = takeData.GetTakeSelection(True)
    if not selected_takes:
        selected_takes = None

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, takeData.GetMainTake())
    
    unmark_takes(takeData, selected_takes)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()