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
# Panels
########################################################################################################################


class PROPERTIES_PT_camera_sequencer(bpy.types.Panel):
    bl_context = 'scene'
    bl_idname = 'PROPERTIES_PT_camera_sequencer'
    bl_label = 'Camera Sequencer'
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def _get_warnings(self, scene):
        warnings = []
        if len(scene.timeline_markers) == 0:
            warnings.append('The timeline has no markers yet.')
        elif common.markers_chronological()[0].frame != scene.frame_start:
            warnings.append('The scene\'s render range does not start with the first shot.')
            return warnings

    def draw(self, context):
        scene = context.scene
        markers = common.markers_chronological()
        lay = self.layout

        # Scene-wide settings.
        box_settings = lay.box()
        box_settings.use_property_split = True
        box_settings.use_property_decorate = False
        target_frame_range = box_settings.column(align=True)
        target_frame_range.prop(scene.camera_sequencer, 'frame_start')
        target_frame_range.prop(scene.camera_sequencer, 'frame_end')
        render_frame_range = box_settings.column(align=True)
        render_frame_range.prop(scene, 'frame_start', text='Render Start Frame')
        render_frame_range.prop(scene, 'frame_end', text='Render End Frame')
        metadata = box_settings.column(align=True)
        metadata.prop(scene.render, 'use_stamp', text='Burn Metadata Into Image')
        metadata.prop(scene.render, 'use_stamp_marker', text='Include Marker Description')
        metadata.prop(scene.render, 'use_stamp_frame_range', text='Include Frame Range')
        metadata.prop(scene.render, 'use_stamp_camera', text='Include Camera Name')

        # Utilities.
        box_utils = lay.box()
        grid_utils = box_utils.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
        grid_utils.operator('camera_sequencer.set_render_range')
        grid_utils.operator('camera_sequencer.reset_render_range')
        select_all = grid_utils.operator('camera_sequencer.toggle_select_all')
        select_all.deselect = False
        select_none = grid_utils.operator('camera_sequencer.toggle_select_all', text='Select None')
        select_none.deselect = True
        grid_utils.operator('camera_sequencer.notes_to_marker_name', icon='FILE_TEXT')

        # Warnings.
        warnings = self._get_warnings(scene=scene)
        if warnings:
            box_warnings = lay.box()
            for warning in warnings:
                box_warnings.label(text=warning, icon='ERROR')

        # Shot list.
        box_markers = lay.box()
        grid_markers = box_markers.grid_flow(row_major=True, columns=7, even_columns=False)

        for marker in markers:

            end_frame = (
                next(m for m in markers if m.frame > marker.frame).frame - 1
                if marker != markers[-1]
                else context.scene.camera_sequencer.frame_end
            )
            dur = common.shot_duration(marker=marker)
            dur_secs = round(dur / scene.render.fps * scene.render.fps_base, 2)

            grid_markers.prop(marker, 'select', text='')
            isolate_shot = grid_markers.operator('camera_sequencer.isolate_shot', text='', icon='VIEWZOOM')
            isolate_shot.marker_frame = marker.frame
            grid_markers.prop(marker, 'name', text='')
            grid_markers.prop(marker, 'camera', text='', expand=True, icon='CAMERA_DATA')
            grid_markers.label(text=f'{marker.frame} - {end_frame}')
            grid_markers.label(text=f'{dur} f')
            grid_markers.label(text=f'{dur_secs} s')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory([PROPERTIES_PT_camera_sequencer])
