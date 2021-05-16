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
    addon_updater_ops = importlib.reload(addon_updater_ops)
    properties = importlib.reload(properties)
    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
else:
    from . import addon_updater_ops, properties, operators, panels


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

    auto_check_update: bpy.props.BoolProperty(name='Auto-check for Update', description='If enabled, auto-check for updates using an interval', default=False)
    updater_intrval_months: bpy.props.IntProperty(name='Months', description='Number of months between checking for updates', default=0, min=0)
    updater_intrval_days: bpy.props.IntProperty(name='Days', description='Number of days between checking for updates', default=7, min=0, max=31)
    updater_intrval_hours: bpy.props.IntProperty(name='Hours', description='Number of hours between checking for updates', default=0, min=0, max=23)
    updater_intrval_minutes: bpy.props.IntProperty(name='Minutes', description='Number of minutes between checking for updates', default=0, min=0, max=59)

    def draw(self, context):
        addon_updater_ops.update_settings_ui(self,context)


###############################################################################
# Registration
###############################################################################


modules = [
    properties,
    operators,
    panels
]


def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(CameraSequencerAddonPreferences)
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()
    bpy.utils.unregister_class(CameraSequencerAddonPreferences)
    addon_updater_ops.unregister()


if __name__ == '__main__':
    register()
