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
        if not common.markers_chronological():
            warnings.append('The timeline has no markers yet.')
        else:
            if not common.target_range_starts_with_first_shot():
                warnings.append('Target range doesn\'t start with the first shot.')
            if not common.render_range_matches_marker_selection():
                warnings.append('Render range doesn\'t match the shot selection.')
        if not common.render_range_matches_target_range():
            warnings.append('Render range doesn\'t match target range.')
        return warnings

    def draw(self, context):
        scene = context.scene
        markers = common.markers_chronological()
        lay = self.layout
        lay.use_property_decorate = False

        # Scene-wide settings.
        box_settings = lay.box()
        box_settings.use_property_split = True
        render_range = box_settings.row(align=True)
        render_range.prop(scene.camera_sequencer, 'frame_start', text='Target Frame Range')
        render_range.prop(scene.camera_sequencer, 'frame_end', text='')
        target_range = box_settings.row(align=True)
        target_range.prop(scene, 'frame_start', text='Render Frame Range')
        target_range.prop(scene, 'frame_end', text='')
        metadata = box_settings.column(align=True)
        metadata.prop(scene.render, 'use_stamp', text='Burn Metadata Into Image')
        metadata.prop(scene.render, 'use_stamp_marker', text='Include Marker Description')
        metadata.prop(scene.render, 'use_stamp_frame_range', text='Include Frame Range')
        metadata.prop(scene.render, 'use_stamp_camera', text='Include Camera Name')

        col_shotlist = lay.column(align=True)

        # Utilities.
        row_utils = col_shotlist.row(align=True)
        row_utils.operator_menu_enum('camera_sequencer.set_frame_range', 'method')
        row_utils.operator('camera_sequencer.notes_to_marker_name', icon='FILE_TEXT')

        # Warnings.
        warnings = self._get_warnings(scene=scene)
        if warnings:
            box_warnings = lay.box()
            for warning in warnings:
                box_warnings.label(text=warning, icon='ERROR')

        # Shot list.
        box_shot_list = col_shotlist.box()
        panels = {}  # Keep a reference to all shot panels
        for marker in markers:

            end_frame = (
                next(m for m in markers if m.frame > marker.frame).frame - 1
                if marker != markers[-1]
                else context.scene.camera_sequencer.frame_end
            )
            dur = common.shot_duration(marker=marker) if marker.frame <= scene.camera_sequencer.frame_end else 0
            dur_secs = round(dur / scene.render.fps * scene.render.fps_base, 2)

            panels[marker.name] = box_shot_list.panel_prop(marker.camera_sequencer, 'is_panel_open')

            row_header = panels[marker.name][0].row()

            split_header = row_header.split(factor=0.55)

            row_name_select = split_header.row(align=True)
            row_name_select.prop(marker, 'select', text='')
            row_name_select.prop(marker, 'name', text='')

            split_time = split_header.split(factor=0.45)

            split_time.label(text=f'{marker.frame}-{end_frame}')

            row_durations = split_time.split(factor=0.45)
            row_durations.label(text=f'{dur} f')
            row_durations.label(text=f'{dur_secs} s')

            isolate_shot = row_header.operator('camera_sequencer.isolate_shot', text='', icon='VIEWZOOM')
            isolate_shot.marker_frame = marker.frame

            if panels[marker.name][1]:
                row = panels[marker.name][1].row(align=True)
                row.use_property_split = True
                row.prop(marker, 'camera', icon='CAMERA_DATA')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory([PROPERTIES_PT_camera_sequencer])
