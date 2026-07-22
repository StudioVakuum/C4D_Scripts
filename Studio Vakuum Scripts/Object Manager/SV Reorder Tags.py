"""
SV Reorder Tags

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Reorders tags on selected objects using the first selected object with tags as the template.

Named tags are matched by tag type and exact name. Unnamed tags are matched by
tag type. Tags which do not occur on the template remain at the end in their
original relative order. No tags are created, deleted, renamed, or copied.

Written for Maxon Cinema 4D 2026.3.0 or later
Python version 3.11.4
"""

import c4d


def get_tag_key(tag):
    """Returns the identity used to match a tag against the template."""
    name = tag.GetName()
    return tag.GetType(), name if name.strip() else None


def get_visible_tags(obj):
    """Returns only tags displayed in the Object Manager."""
    return [tag for tag in obj.GetTags()
            if tag.GetInfo() & c4d.TAG_VISIBLE]


def get_reordered_tags(template_keys, tags):
    """Returns tags ordered like the template, followed by unmatched tags."""
    remaining = list(tags)
    ordered = []

    for template_key in template_keys:
        for index, tag in enumerate(remaining):
            if get_tag_key(tag) == template_key:
                ordered.append(tag)
                remaining.pop(index)
                break

    ordered.extend(remaining)
    return ordered


def has_different_order(current_tags, reordered_tags):
    return any(current is not reordered
               for current, reordered in zip(current_tags, reordered_tags))


def apply_tag_order(obj, tags):
    """Moves existing tags into the supplied left-to-right order."""
    predecessor = None

    for tag in tags:
        obj.InsertTag(tag, predecessor)
        predecessor = tag


def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if len(objects) < 2:
        c4d.gui.MessageDialog("Please select at least two objects.")
        return

    template_index = next(
        (index for index, obj in enumerate(objects) if get_visible_tags(obj)),
        None
    )

    if template_index is None:
        c4d.gui.MessageDialog("None of the selected objects has tags.")
        return

    template = objects[template_index]
    template_keys = [get_tag_key(tag) for tag in get_visible_tags(template)]
    reorder_jobs = []

    for obj in objects[template_index + 1:]:
        current_tags = get_visible_tags(obj)
        if len(current_tags) < 2:
            continue

        reordered_tags = get_reordered_tags(template_keys, current_tags)
        if has_different_order(current_tags, reordered_tags):
            reorder_jobs.append((obj, reordered_tags))

    if not reorder_jobs:
        return

    doc.StartUndo()
    try:
        for obj, reordered_tags in reorder_jobs:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            apply_tag_order(obj, reordered_tags)
    finally:
        doc.EndUndo()

    c4d.EventAdd()


if __name__ == "__main__":
    main()
