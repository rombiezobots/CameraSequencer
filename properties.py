##############################################################################
# Imports
##############################################################################


if 'functions' in locals():
    import importlib
    functions = importlib.reload(functions)
else:
    from CameraSequencer import functions
    import bpy


##############################################################################
# Properties
##############################################################################


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


def register():
    bpy.utils.register_class(Shot)
    bpy.types.Scene.milkshake_shots = bpy.props.CollectionProperty(
        type=Shot)
    bpy.types.Scene.camera_sequencer_shots = bpy.props.CollectionProperty(
        type=Shot)


def unregister():
    bpy.utils.unregister_class(Shot)
    try:
        del bpy.types.Scene.milkshake_shots
        del bpy.types.Scene.camera_sequencer_shots
    except:
        pass
