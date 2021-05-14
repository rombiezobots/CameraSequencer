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

    start_frame: bpy.props.IntProperty(name='Start Frame', default=1,
                                       update=functions.sync_timeline,
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
                                    update=functions.sync_timeline,
                                    subtype='TIME',
                                    description='Duration in frames')
    camera_object: bpy.props.PointerProperty(name='Camera',
                                             type=bpy.types.Object,
                                             update=functions.sync_timeline,
                                             poll=functions.object_must_be_camera)
    notes: bpy.props.StringProperty(name='Notes',
                                    default='')


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
