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
        col = box_settings.column(align=True)
        col.prop(scene, 'frame_start')
        col.prop(scene, 'frame_end')

        # Dynamic Note
        lay.operator('camera_sequencer.setup_metadata_stamping', icon='FILE_TEXT')

        # Shot list frame.
        box_shotlist = lay.box()

        # Warning cases.
        if len(scene.timeline_markers) == 0:
            box_shotlist.label(text='The timeline has no markers yet.', icon='ERROR')
        elif markers[0].frame != context.scene.frame_start:
            box_shotlist.label(text='The first shot does not start on the timeline\'s first frame.', icon='ERROR')

        # Shot list.
        for marker in markers:
            # Frame and main column.
            box_shot = box_shotlist.box()
            col_main = box_shot.column(align=True)

            # Top row. Toggle collapse, isolate shot, shot name, and the assigned camera.
            row_top = col_main.row(align=True)
            triangle = 'TRIA_RIGHT' if marker.camera_sequencer.is_collapsed else 'TRIA_DOWN'
            row_top.prop(marker.camera_sequencer, 'is_collapsed', icon=triangle, text='', invert_checkbox=True)
            row_top.operator('camera_sequencer.isolate_shot', text='', icon='VIEWZOOM').marker_frame = marker.frame
            row_top.prop(marker, 'name', text='')
            row_top.prop(marker, 'camera', text='', icon='CAMERA_DATA')

            if not marker.camera_sequencer.is_collapsed:
                # Shot notes / description.
                col_main.prop(data=marker.camera_sequencer, property='notes', text='')

                # Bottom row. Shot duration.
                len_frames = common.shot_duration(marker=marker)
                len_secs = len_frames / scene.render.fps * scene.render.fps_base
                box_bottom = col_main.box()
                box_bottom.label(text=f'{len_frames} frames = {round(len_secs, 2)} seconds', icon='TIME')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory([PROPERTIES_PT_camera_sequencer])
