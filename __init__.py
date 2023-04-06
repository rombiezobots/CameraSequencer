########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

    properties = importlib.reload(properties)
    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
else:
    import bpy
    from . import properties
    from . import operators
    from . import panels


########################################################################################################################
# Add-on information
########################################################################################################################


bl_info = {
    'author': 'Sam Van Hulle',
    'blender': (3, 5, 0),
    'category': 'Camera',
    'description': 'Shot-based user interface for cameras and timeline markers',
    'location': 'Properties > Scene',
    'name': 'Camera Sequencer',
    'wiki_url': 'https://rombiezobots.com',
}


########################################################################################################################
# Registration
########################################################################################################################


modules = [properties, operators, panels]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()


if __name__ == '__main__':
    register()
