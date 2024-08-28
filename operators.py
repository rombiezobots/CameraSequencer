########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

    common = importlib.reload(common)
else:
    import bpy
    from . import common


########################################################################################################################
# Operators
########################################################################################################################


class CAMERASEQUENCER_OT_notes_to_marker_name(bpy.types.Operator):
    '''(temporary) Copy old Notes property value to the native marker name'''

    bl_idname = 'camera_sequencer.notes_to_marker_name'
    bl_label = 'Notes to Marker Name'
    bl_options = {'UNDO'}

    def execute(self, context):
        for m in context.scene.timeline_markers:
            m.name = m.camera_sequencer.notes
        return {'FINISHED'}


class CAMERASEQUENCER_OT_clear_shots(bpy.types.Operator):
    '''Delete all markers from the timeline'''

    bl_idname = 'camera_sequencer.clear_shots'
    bl_label = 'Clear'
    bl_options = {'UNDO'}

    def execute(self, context):
        for m in context.scene.timeline_markers:
            context.scene.timeline_markers.remove(m)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_isolate_shot(bpy.types.Operator):
    '''Isolate this shot as a preview'''

    bl_idname = 'camera_sequencer.isolate_shot'
    bl_label = 'Isolate shot'
    marker_frame: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        marker = common.marker_at_frame(frame=self.marker_frame, exact=True)
        length = common.shot_duration(marker=marker)
        # Disable the preview range if it's currently set to the same shot.
        if (
            scene.use_preview_range
            and scene.frame_preview_start == marker.frame
            and scene.frame_preview_end == marker.frame + length - 1
        ):
            scene.use_preview_range = False
        # Set the preview range to the specified shot.
        else:
            scene.use_preview_range = True
            # If the target preview range comes after the current one, set the end frame first (inherent issue caused by Blender clamping)
            if marker.frame >= scene.frame_preview_start:
                scene.frame_preview_end = marker.frame + length - 1
                scene.frame_preview_start = marker.frame
            # If not, reverse.
            else:
                scene.frame_preview_start = marker.frame
                scene.frame_preview_end = marker.frame + length - 1
            # Set current frame to the shot's marker.
            scene.frame_set(marker.frame)
        return {'FINISHED'}


class CAMERASEQUENCER_OT_setup_metadata_stamping(bpy.types.Operator):
    '''Enable a handler that dynamically changes the Metadata Note with every shot's description.\nReleased on file close'''

    bl_idname = 'camera_sequencer.setup_metadata_stamping'
    bl_label = 'Enable Dynamic Note'
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.app.handlers.frame_change_pre.append(functions.enable_dynamic_metadata_note)
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        CAMERASEQUENCER_OT_notes_to_marker_name,
        CAMERASEQUENCER_OT_clear_shots,
        CAMERASEQUENCER_OT_isolate_shot,
        CAMERASEQUENCER_OT_setup_metadata_stamping,
    ]
)
