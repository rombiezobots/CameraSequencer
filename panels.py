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
            shot_box = box_shots.box()
            block_1 = shot_box.column(align=True)
            block_1_top = block_1.split(factor=0.3, align=True)
            block_1_top.scale_y = 1.5
            block_1_top_left = block_1_top.split(factor=0.4, align=True)
            block_1_top_left.operator('camera_sequencer.isolate_shot',
                                      text='', icon='VIEWZOOM').index = index
            block_1_top_left.operator('camera_sequencer.jump_to_specific_shot',
                                      text=shot.code).index = index
            block_1_top_right = block_1_top.row(align=True)
            block_1_top_right.prop(data=shot,
                                   property='camera_object',
                                   text='',
                                   icon='CAMERA_DATA')
            duration_seconds = shot.duration / scene.render.fps * scene.render.fps_base
            block_1_top_right.prop(data=shot,
                                   property='duration',
                                   text=f'{round(duration_seconds, 2)}s',
                                   icon='TIME')
            block_1_bottom = block_1.row(align=True)
            block_1_bottom.prop(data=shot, property='notes', text='')
            block_1_bottom.operator('camera_sequencer.move_shot_up',
                                    icon='TRIA_UP', text='').index = index
            block_1_bottom.operator('camera_sequencer.move_shot_down',
                                    icon='TRIA_DOWN', text='').index = index
            block_1_bottom.operator('camera_sequencer.delete_shot',
                                    icon='TRASH', text='').index = index


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    PROPERTIES_PT_camera_sequencer
])
