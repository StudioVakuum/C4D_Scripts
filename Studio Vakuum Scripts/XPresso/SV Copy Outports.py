import c4d
import json
from c4d.modules import graphview

def GetSelectedXPressoNode():
    gv_master = graphview.GetMaster(0)
    if gv_master is None:
        return None

    for node in gv_master.GetRoot().GetChildren():
        if node.GetBit(c4d.BIT_ACTIVE):
            return node
    return None

def CopyOutputPortsToClipboard(node):
    if node is None:
        print("Kein Node ausgewählt.")
        return

    num_ports = node.GetOutPortCount()
    if num_ports == 0:
        print("Keine Output-Ports vorhanden.")
        return

    ports_data = [port.GetName(node) for i in range(num_ports) if (port := node.GetOutPort(i))]

    clipboard_data = json.dumps(ports_data, indent=4)
    print(clipboard_data)
    c4d.CopyStringToClipboard(clipboard_data)
    print(f"{len(ports_data)} Output-Port-Namen wurden ins Clipboard kopiert.")

def main():
    selected_node = GetSelectedXPressoNode()
    if selected_node:
        CopyOutputPortsToClipboard(selected_node)
    else:
        print("Kein Xpresso-Node ausgewählt.")

if __name__ == "__main__":
    main()
