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

        # Warning cases.
        if len(scene.timeline_markers) == 0:
            lay.label(text='The timeline has no markers yet.', icon='ERROR')
        elif markers[0].frame != context.scene.frame_start:
            lay.label(text='The first shot does not start on the timeline\'s first frame.', icon='ERROR')

        # Shot list.
        # First create a dict to not lose the panel references.
        panels = {}
        for marker in markers:
            panels[marker.name] = lay.panel_prop(marker.camera_sequencer, 'is_collapsed')

            # Top row. Toggle collapse, isolate shot, shot name, and the assigned camera.
            row_header = panels[marker.name][0].row(align=True)
            isolate_shot = row_header.operator('camera_sequencer.isolate_shot', text='', icon='VIEWZOOM')
            isolate_shot.marker_frame = marker.frame
            row_header.prop(marker, 'name', text='')
            row_header.prop(marker, 'camera', text='', icon='CAMERA_DATA')

            # Shot notes / description.
            if panels[marker.name][1]:
                col_body = panels[marker.name][1].column(align=True)
                col_body.prop(data=marker.camera_sequencer, property='notes', text='')
                len_frames = common.shot_duration(marker=marker)
                len_secs = len_frames / scene.render.fps * scene.render.fps_base
                box = col_body.box()
                row_time = box.row()
                row_time.label(text=f'{len_frames} frames', icon='PREVIEW_RANGE')
                row_time.label(text=f'{round(len_secs, 2)} seconds')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory([PROPERTIES_PT_camera_sequencer])
