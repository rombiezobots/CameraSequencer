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
        box_settings.prop(scene.camera_sequencer_settings, 'start_frame')
        lay.separator()
        col = lay.column(align=True)
        sub = col.row(align=True)
        sub.operator('camera_sequencer.new_shot',
                     icon='ADD', text='')
        sub.operator('camera_sequencer.jump_shots',
                     icon='TRIA_LEFT', text='').previous = True
        sub.operator('camera_sequencer.jump_shots',
                     icon='TRIA_RIGHT', text='').previous = False
        sub.operator('camera_sequencer.clear_shots',
                     icon='X', text='')
        sub.separator()
        sub.operator('camera_sequencer.clean_up_cameras',
                     icon='BRUSH_DATA', text='')
        sub.separator()
        sub.operator('camera_sequencer.setup_metadata_stamping',
                     icon='FILE_TEXT', text='')
        box_shots = col.box()
        if len(scene.camera_sequencer_shots) == 0:
            box_shots.label(text='No shots yet.')
        for index, shot in enumerate(scene.camera_sequencer_shots):
            triangle = 'TRIA_RIGHT' if shot.is_collapsed else 'TRIA_DOWN'
            shot_box = box_shots.box()
            col = shot_box.column(align=True)
            top = col.split(factor=0.3, align=True)
            top.scale_y = 1 + int(not shot.is_collapsed) * 0.5
            top_left = top.row(align=True)
            top_left.prop(shot, 'is_collapsed', icon=triangle, text='',
                invert_checkbox=True)
            split = top_left.split(factor=0.5, align=True)
            split.operator('camera_sequencer.isolate_shot',
                              text='', icon='VIEWZOOM').index = index
            split.operator('camera_sequencer.jump_to_specific_shot',
                              text=shot.code).index = index

            top_right = top.row(align=True)
            top_right.prop(data=shot,
                           property='camera_object',
                           text='',
                           icon='CAMERA_DATA')
            len_secs = shot.duration / scene.render.fps * scene.render.fps_base
            top_right.prop(data=shot,
                           property='duration',
                           text=f'{round(len_secs, 2)}s',
                           icon='TIME')
            if not shot.is_collapsed:
                block_bottom = col.row(align=True)
                block_bottom.prop(data=shot, property='notes', text='')
                block_bottom.operator('camera_sequencer.move_shot_up',
                                      icon='TRIA_UP', text='').index = index
                block_bottom.operator('camera_sequencer.move_shot_down',
                                      icon='TRIA_DOWN', text='').index = index
                block_bottom.operator('camera_sequencer.delete_shot',
                                      icon='TRASH', text='').index = index


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    PROPERTIES_PT_camera_sequencer
])
