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

    def draw(self, context):
        scene = context.scene
        markers = common.markers_chronological()
        lay = self.layout

        # Scene-wide settings. These are native Blender properties of the current Scene, drawn here for convenience.
        box_settings = lay.box()
        box_settings.use_property_split = True
        box_settings.use_property_decorate = False
        col = box_settings.column(align=True)
        col.prop(scene, 'frame_start')
        col.prop(scene, 'frame_end')
        col = box_settings.column(align=True)
        col.prop(scene.render, 'use_stamp', text='Burn Metadata Into Image')
        col.prop(scene.render, 'use_stamp_marker', text='Include Marker Description')
        col.prop(scene.render, 'use_stamp_frame_range', text='Include Frame Range')
        col.prop(scene.render, 'use_stamp_camera', text='Include Camera Name')

        # Dynamic Note
        lay.operator('camera_sequencer.notes_to_marker_name', icon='FILE_TEXT')

        # Warning cases.
        if len(scene.timeline_markers) == 0:
            lay.label(text='The timeline has no markers yet.', icon='ERROR')
        elif markers[0].frame != context.scene.frame_start:
            lay.label(text='The first shot does not start on the timeline\'s first frame.', icon='ERROR')

        grid = lay.grid_flow(row_major=True, columns=6, even_columns=False, align=True)

        # Shot list.
        for marker in markers:

            end_frame = (
                next(m for m in markers if m.frame > marker.frame).frame - 1
                if marker != markers[-1]
                else context.scene.frame_end
            )
            dur = common.shot_duration(marker=marker)
            dur_secs = round(dur / scene.render.fps * scene.render.fps_base, 2)

            isolate_shot = grid.operator('camera_sequencer.isolate_shot', text='', icon='VIEWZOOM')
            isolate_shot.marker_frame = marker.frame
            grid.prop(marker, 'name', text='')
            grid.prop(marker, 'camera', text='', expand=True, icon='CAMERA_DATA')
            grid.label(text=f'{marker.frame} - {end_frame}')
            grid.label(text=f'{dur} f')
            grid.label(text=f'{dur_secs} s')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory([PROPERTIES_PT_camera_sequencer])
