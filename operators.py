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
# Operators
##############################################################################


class CAMERASEQUENCER_OT_import_milkshake_shots(bpy.types.Operator):
    """Import shots from Milkshake, and delete the old CollectionProperty"""

    bl_idname = 'camera_sequencer.import_milkshake_shots'
    bl_label = 'Import Milkshake Shots'
    bl_options = {'UNDO'}
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.import_milkshake_shots()
        functions.sync_timeline(self, context)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_clear_shots(bpy.types.Operator):
    """Clear the shot list."""

    bl_idname = 'camera_sequencer.clear_shots'
    bl_label = 'Clear'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clear_shots()
        functions.sync_timeline(self, context)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_delete_shot(bpy.types.Operator):
    """Delete the selected shot and the associated camera"""

    bl_idname = 'camera_sequencer.delete_shot'
    bl_label = 'Delete'
    bl_options = {'UNDO'}
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.delete_shot(index=self.index)
        functions.autorename_shots()
        functions.sync_timeline(self, context)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_isolate_shot(bpy.types.Operator):
    """Use this shot's frame range as the timeline's preview range"""

    bl_idname = 'camera_sequencer.isolate_shot'
    bl_label = 'Isolate shot'
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.isolate_shot(target_index=self.index)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_jump_shots(bpy.types.Operator):
    """Jump shots in the timeline"""

    bl_idname = 'camera_sequencer.jump_shots'
    bl_label = 'Jump Shots'
    previous: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        functions.jump_shots(previous=self.previous)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_jump_to_specific_shot(bpy.types.Operator):
    """Jump to this shot in the timeline"""

    bl_idname = 'camera_sequencer.jump_to_specific_shot'
    bl_label = 'Jump To Shot'
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.jump_to_specific_shot(index=self.index)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_move_shot_up(bpy.types.Operator):
    """Move the shot up the timeline"""

    bl_idname = 'camera_sequencer.move_shot_up'
    bl_label = 'Move Shot Up'
    bl_options = {'UNDO'}
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.move_shot_up(index=self.index)
        functions.autorename_shots()
        functions.sync_timeline(self, context)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_move_shot_down(bpy.types.Operator):
    """Move the shot down the timeline"""

    bl_idname = 'camera_sequencer.move_shot_down'
    bl_label = 'Move Shot Down'
    bl_options = {'UNDO'}
    index: bpy.props.IntProperty()

    def execute(self, context):
        functions.move_shot_down(index=self.index)
        functions.autorename_shots()
        functions.sync_timeline(self, context)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_new_shot(bpy.types.Operator):
    """Create a new shot and camera"""

    bl_idname = 'camera_sequencer.new_shot'
    bl_label = 'New Shot'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.new_shot()
        functions.autorename_shots()
        return {'FINISHED'}


class CAMERASEQUENCER_OT_setup_metadata_stamping(bpy.types.Operator):
    """Enable a handler that dynamically changes the Metadata Note with every shot's description.\nReleased on file close"""

    bl_idname = 'camera_sequencer.setup_metadata_stamping'
    bl_label = 'Enable Dynamic Note'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.setup_metadata_stamping()
        bpy.app.handlers.frame_change_pre.append(
            functions.enable_dynamic_metadata_note)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_clean_up_cameras(bpy.types.Operator):
    """Clean up unused cameras in the scene"""

    bl_idname = 'camera_sequencer.clean_up_cameras'
    bl_label = 'Clean Up Cameras'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clean_up_cameras()
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    CAMERASEQUENCER_OT_clean_up_cameras,
    CAMERASEQUENCER_OT_clear_shots,
    CAMERASEQUENCER_OT_delete_shot,
    CAMERASEQUENCER_OT_import_milkshake_shots,
    CAMERASEQUENCER_OT_isolate_shot,
    CAMERASEQUENCER_OT_jump_shots,
    CAMERASEQUENCER_OT_jump_to_specific_shot,
    CAMERASEQUENCER_OT_move_shot_down,
    CAMERASEQUENCER_OT_move_shot_up,
    CAMERASEQUENCER_OT_new_shot,
    CAMERASEQUENCER_OT_setup_metadata_stamping
])
