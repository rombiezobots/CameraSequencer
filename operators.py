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


class CAMERASEQUENCER_OT_set_frame_range(bpy.types.Operator):
    '''Set frame ranges'''

    bl_idname = 'camera_sequencer.set_frame_range'
    bl_label = 'Set Frame Range'
    bl_options = {'UNDO'}

    method: bpy.props.EnumProperty(
        name='Method',
        items=[
            (
                'SELECTED_SHOTS',
                'Trim Render Range to Selected Shots',
                'Trim the scene\'s render range to encompass all selected shots',
            ),
            (
                'TARGET_RANGE',
                'Set Target Range to Render Range',
                'Set the target range to the scene\'s current render range',
            ),
            (
                'RENDER_RANGE',
                'Reset Render Range to Target Range',
                'Reset the scene\'s render range to the target range',
            ),
        ],
    )

    def execute(self, context):

        markers_chronological = common.markers_chronological()

        if markers_chronological:

            if self.method == 'SELECTED_SHOTS':
                first_shot = next(m for m in markers_chronological if m.select)
                *_, last_shot = (m for m in markers_chronological if m.select)
                last_frame = common.shot_frame_last(marker=last_shot)
                context.scene.frame_start = first_shot.frame
                context.scene.frame_end = last_frame

            elif self.method == 'TARGET_RANGE':
                context.scene.camera_sequencer.frame_start = context.scene.frame_start
                context.scene.camera_sequencer.frame_end = context.scene.frame_end

            elif self.method == 'RENDER_RANGE':  # Reset
                context.scene.frame_start = context.scene.camera_sequencer.frame_start
                context.scene.frame_end = context.scene.camera_sequencer.frame_end

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


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        CAMERASEQUENCER_OT_notes_to_marker_name,
        CAMERASEQUENCER_OT_set_frame_range,
        CAMERASEQUENCER_OT_clear_shots,
        CAMERASEQUENCER_OT_isolate_shot,
    ]
)
