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
    if markers:
        if marker == markers[-1]:
            return bpy.context.scene.camera_sequencer.frame_end
        index_next = markers.index(marker) + 1
        return markers[index_next].frame - 1
    return None


def shot_duration(marker: bpy.types.TimelineMarker) -> int:
    frame_last = shot_frame_last(marker=marker)
    return frame_last + 1 - marker.frame


# Warning checks


def target_range_starts_with_first_shot() -> bool:
    '''Check whether the target range starts with the first shot marker'''
    markers = markers_chronological()
    return markers[0].frame == bpy.context.scene.camera_sequencer.frame_start


def render_range_matches_target_range() -> bool:
    '''Check whether the render range is identical to the target range'''
    scene = bpy.context.scene
    return (
        scene.frame_end == scene.camera_sequencer.frame_end and scene.frame_start == scene.camera_sequencer.frame_start
    )


def render_range_matches_marker_selection() -> bool:
    '''Check whether the render range encompasses the shot selection exactly'''
    markers = markers_chronological()
    first_shot = next(m for m in markers if m.select)
    *_, last_shot = (m for m in markers if m.select)
    scene = bpy.context.scene
    return scene.frame_start == first_shot.frame and scene.frame_end == shot_frame_last(marker=last_shot)
