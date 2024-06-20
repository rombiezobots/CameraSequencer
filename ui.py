########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def camera_sequencer_ui(self, context):
    row = self.layout.row()
    row.separator()
    row.label(text='Camera Sequencer')
    sub = row.row(align=True)
    prev = sub.operator('camera_sequencer.skip_shots', icon='FRAME_PREV', text='')
    prev.previous = True
    next = sub.operator('camera_sequencer.skip_shots', icon='FRAME_NEXT', text='')
    next.previous = False
    sub.operator('camera_sequencer.clear_shots', icon='X', text='')


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.types.DOPESHEET_HT_header.append(camera_sequencer_ui)


def unregister():
    bpy.types.DOPESHEET_HT_header.remove(camera_sequencer_ui)
