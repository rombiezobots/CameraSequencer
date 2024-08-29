########################################################################################################################
# Imports
########################################################################################################################


import bpy
from operator import attrgetter


########################################################################################################################
# Functions
########################################################################################################################


def marker_at_frame(frame: int, exact: bool = False) -> bpy.types.TimelineMarker:
    markers = markers_chronological()

    if exact:
        # Return the marker placed exactly on the given frame.
        return next((x for x in markers if x.frame == frame), None)

    # Return the marker that's active on the given frame.
    return next((m for m in markers if m.frame <= frame and frame <= m.frame + shot_duration(m) - 1), None)


def markers_chronological():
    return sorted(bpy.context.scene.timeline_markers, key=attrgetter('frame'))


def shot_frame_last(marker: bpy.types.TimelineMarker) -> int:
    markers = markers_chronological()
    if marker == markers[-1]:
        return bpy.context.scene.camera_sequencer.frame_end
    index_next = markers.index(marker) + 1
    return markers[index_next].frame - 1


def shot_duration(marker: bpy.types.TimelineMarker) -> int:
    frame_last = shot_frame_last(marker=marker)
    return frame_last + 1 - marker.frame
