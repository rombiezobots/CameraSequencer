##############################################################################
# Imports
##############################################################################


if 'functions' in locals():
    import importlib
    functions = importlib.reload(functions)
else:
    from . import functions
    import bpy


##############################################################################
# Properties
##############################################################################


class CameraSequencerSettings(bpy.types.PropertyGroup):

    start_frame: bpy.props.IntProperty(name='Start Frame', default=1001,
                                       update=functions.change_start_frame,
                                       min=0,
                                       description='Shots should start at this frame',
                                       options=set())


class Shot(bpy.types.PropertyGroup):

    code: bpy.props.StringProperty(name='Shot Code',
                                   default='Shot',
                                   update=functions.sync_timeline)
    duration: bpy.props.IntProperty(name='Frames',
                                    default=24,
                                    min=1,
                                    update=functions.change_shot_duration,
                                    subtype='TIME',
                                    description='Duration in frames')

    # This is to circumvent the fact that Blender doesn't automatically
    # provide update functions with what has changed since last calling
    # it. When changing a shot's duration, we compare it to
    # previous_duration's value to determine for how many frames any
    # camera animation should be moved.
    previous_duration: bpy.props.IntProperty(default=24)

    camera_object: bpy.props.PointerProperty(name='Camera',
                                             type=bpy.types.Object,
                                             update=functions.on_camera_update,
                                             poll=functions.object_must_be_camera)
    notes: bpy.props.StringProperty(name='Notes',
                                    default='')
    is_collapsed: bpy.props.BoolProperty(default=False)


##############################################################################
# Registration
##############################################################################


classes = [
    Shot,
    CameraSequencerSettings
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.camera_sequencer_shots = bpy.props.CollectionProperty(type=Shot)
    bpy.types.Scene.camera_sequencer_settings = bpy.props.PointerProperty(type=CameraSequencerSettings)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    try:
        del bpy.types.Scene.camera_sequencer_shots
        del bpy.types.Scene.camera_sequencer_settings
    except:
        pass
