###############################################################################
#                               CAMERA SEQUENCER                              #
#         Shot-based user interface for cameras and timeline markers          #
###############################################################################


###############################################################################
# Imports
###############################################################################


import bpy
if 'properties' in locals():
    import importlib
    properties = importlib.reload(properties)
    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
else:
    from . import properties, operators, panels


###############################################################################
# Add-on information
###############################################################################


bl_info = {
    'name': 'Camera Sequencer',
    'description': 'Shot-based user interface for cameras and timeline markers',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 1),
    'blender': (2, 92, 0),
    'location': 'Properties > Scene',
    'category': 'Camera'
}


###############################################################################
# Add-on preferences
###############################################################################


class CameraSequencerAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__


###############################################################################
# Registration
###############################################################################


modules = [
    properties,
    operators,
    panels
]


def register():
    bpy.utils.register_class(CameraSequencerAddonPreferences)
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()
    bpy.utils.unregister_class(CameraSequencerAddonPreferences)


if __name__ == '__main__':
    register()
