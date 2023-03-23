##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_camera_sequencer(bpy.types.Panel):

    bl_context = 'scene'
    bl_idname = 'PROPERTIES_PT_camera_sequencer'
    bl_label = 'Camera Sequencer'
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        scene = context.scene
        lay = self.layout

        box_settings = lay.box()
        box_settings.use_property_split = True
        box_settings.prop(scene, 'frame_start')

        lay.separator()

        col = lay.column(align=True)
        sub = col.row(align=True)
        sub.operator('camera_sequencer.new_shot',
                     icon='ADD',
                     text='')
        sub.operator('camera_sequencer.jump_shots',
                     icon='TRIA_LEFT',
                     text='').previous = True
        sub.operator('camera_sequencer.jump_shots',
                     icon='TRIA_RIGHT',
                     text='').previous = False
        sub.operator('camera_sequencer.clear_shots',
                     icon='X',
                     text='')
        sub.separator()
        sub.operator('camera_sequencer.setup_metadata_stamping',
                     icon='FILE_TEXT',
                     text='')
        box_shots = col.box()

        if len(scene.timeline_markers) == 0:
            box_shots.label(text='The timeline has no markers yet.',
                            icon='ERROR')

        for index, marker in enumerate(scene.timeline_markers):
            cs = marker.camera_sequencer
            triangle = 'TRIA_RIGHT' if cs.is_collapsed else 'TRIA_DOWN'
            shot_box = box_shots.box()
            col = shot_box.column(align=True)
            # top = col.split(factor=0.5, align=True)
            top = col.row(align=True)
            top.scale_y = 1 + int(not cs.is_collapsed) * 0.5
            # top_left = top.row(align=True)
            top.prop(cs,
                     'is_collapsed',
                     icon=triangle,
                     text='',
                     invert_checkbox=True)
            top.operator('camera_sequencer.isolate_shot',
                         text='',
                         icon='VIEWZOOM').index = index
            # top_right = top.row(align=True)
            top.prop(cs, 'name', text='')
            top.prop(data=marker,
                     property='camera',
                     text='',
                     icon='CAMERA_DATA')

            # Shot duration. NEEDS WORK

            if index == len(scene.timeline_markers) - 1:
                len_frames = scene.frame_end + 1 - marker.frame
            else:
                len_frames = scene.timeline_markers[index +
                                                    1].frame - marker.frame
            len_secs = len_frames / scene.render.fps * scene.render.fps_base
            top.label(text=f'{round(len_secs, 2)}s',
                      icon='TIME')

            if not cs.is_collapsed:
                block_bottom = col.row(align=True)
                block_bottom.prop(data=cs,
                                  property='notes',
                                  text='')
                block_bottom.operator('camera_sequencer.delete_shot',
                                      icon='TRASH',
                                      text='').index = index


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    PROPERTIES_PT_camera_sequencer
])
