########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Properties
########################################################################################################################


class TimelineMarkerProperties(bpy.types.PropertyGroup):
    notes: bpy.props.StringProperty(name='Notes', default='This shot has no description yet.')
    is_collapsed: bpy.props.BoolProperty(default=False)


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    TimelineMarkerProperties,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TimelineMarker.camera_sequencer = bpy.props.PointerProperty(type=TimelineMarkerProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.TimelineMarker.camera_sequencer
