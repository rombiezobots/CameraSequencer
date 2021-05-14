###############################################################################
#                               CAMERA SEQUENCER                              #
#         Shot-based user interface for cameras and timeline markers          #
###############################################################################


###############################################################################
# Imports
###############################################################################


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
    'version': (1, 0, 0),
    'blender': (2, 83, 0),
    'location': 'Properties > Scene',
    'category': 'Camera'
}


###############################################################################
# Registration
###############################################################################


modules = [
    properties,
    operators,
    panels
]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()


if __name__ == '__main__':
    register()
