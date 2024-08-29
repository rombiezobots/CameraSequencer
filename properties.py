########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Properties
########################################################################################################################


class SceneProperties(bpy.types.PropertyGroup):
    frame_start: bpy.props.IntProperty(name='Target Start Frame', default=1001)
    frame_end: bpy.props.IntProperty(name='Target End Frame', default=1250)


class TimelineMarkerProperties(bpy.types.PropertyGroup):
    notes: bpy.props.StringProperty(name='Notes', default='This shot has no description yet.')


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    TimelineMarkerProperties,
    SceneProperties,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.camera_sequencer = bpy.props.PointerProperty(type=SceneProperties)
    bpy.types.TimelineMarker.camera_sequencer = bpy.props.PointerProperty(type=TimelineMarkerProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.camera_sequencer
    del bpy.types.TimelineMarker.camera_sequencer
