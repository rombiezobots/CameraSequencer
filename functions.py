##############################################################################
# Imports
##############################################################################


import bpy
import math


##############################################################################
# Functions
##############################################################################


def autorename_shots():
    """Auto-rename all shots"""

    for index, shot in enumerate(bpy.context.scene.camera_sequencer_shots):
        shot.code = f"SH{(index + 1):02}"


def camera_collection() -> bpy.types.Collection:
    """Return the scene's camera collection"""

    collections = bpy.data.collections
    
    # If the collection doesn't exist yet, create it
    if not "cameras.GRP.001" in collections.keys():
        camera_collection = collections.new("cameras.GRP.001")
    else:
        camera_collection = collections['cameras.GRP.001']

    # If the collection isn't in the scene yet, link it
    scene_collection = bpy.context.scene.collection
    if not "cameras.GRP.001" in scene_collection.children:
        scene_collection.children.link(camera_collection)

    return camera_collection


def delete_shot(index: int):
    """Delete the selected shot and the associated camera"""
    bpy.context.scene.camera_sequencer_shots.remove(index)


def clear_shots():
    """Clear the shot list and delete the associated cameras"""

    scene = bpy.context.scene
    for shot in scene.camera_sequencer_shots:
        bpy.data.objects.remove(shot.camera_object)
    scene.camera_sequencer_shots.clear()


def import_milkshake_shots():
    scene = bpy.context.scene
    for old_shot in scene.milkshake_shots:
        new_shot = scene.camera_sequencer_shots.add()
        new_shot.code = old_shot.code
        new_shot.duration = old_shot.duration
        new_shot.camera_object = old_shot.camera_object
        new_shot.notes = old_shot.notes
    scene.milkshake_shots.clear()


def isolate_shot(target_index: int):
    """Use this shot's frame range as the timeline's preview range"""

    scene = bpy.context.scene
    counter = scene.frame_start
    for index, shot in enumerate(scene.camera_sequencer_shots):
        if index == target_index:
            if scene.use_preview_range and scene.frame_preview_start == counter and scene.frame_preview_end == counter + shot.duration - 1:
                scene.use_preview_range = False
            else:
                scene.use_preview_range = True
                # if the target preview range comes after the current one, set
                # the end frame first (inherent issue caused by Blender clamping)
                if counter >= scene.frame_preview_start:
                    scene.frame_preview_end = counter + shot.duration - 1
                    scene.frame_preview_start = counter
                # if not, reverse
                else:
                    scene.frame_preview_start = counter
                    scene.frame_preview_end = counter + shot.duration - 1
                # set frame to shot start
                scene.frame_set(counter)
                break
        counter += shot.duration


def jump_shots(previous: bool):
    """Jump to the first frame of the next/previous shot in the timeline"""

    scene = bpy.context.scene
    counter = scene.frame_start
    for index, shot in enumerate(scene.camera_sequencer_shots):
        if counter <= scene.frame_current < counter + shot.duration:
            if not previous and index < len(scene.camera_sequencer_shots) - 1:
                counter += shot.duration
                scene.frame_set(counter)
                break
            elif previous and index > 0:
                counter -= scene.camera_sequencer_shots[index - 1].duration
                scene.frame_set(counter)
                break
        counter += shot.duration


def jump_to_specific_shot(index: int):
    """Jump to a specific shot in the timeline"""

    scene = bpy.context.scene
    counter = scene.frame_start
    if index > 0:
        for i in range(index):
            counter += scene.camera_sequencer_shots[i].duration
    scene.frame_set(counter)


def move_shot_up(index: int):
    """Move the shot up the timeline"""

    shots = bpy.context.scene.camera_sequencer_shots
    if index > 0:
        previous_index = index - 1
        shots.move(index, previous_index)
        # force update scene camera setting here too


def move_shot_down(index: int):
    """Move the shot down the timeline"""

    shots = bpy.context.scene.camera_sequencer_shots
    if index < len(shots) - 1:
        next_index = index + 1
        shots.move(index, next_index)
        # force update scene camera setting here too


def new_shot():
    """Create a new shot and camera"""

    shot = bpy.context.scene.camera_sequencer_shots.add()
    camera = bpy.data.cameras.new("Camera")
    camera.display_size = 1
    camera.dof.aperture_blades = 5
    camera.dof.aperture_fstop = 4
    camera.dof.aperture_ratio = 1
    camera.dof.aperture_rotation = math.radians(10)
    camera.dof.focus_distance = 1
    camera.dof.use_dof = True
    camera.lens = 35
    camera.passepartout_alpha = 0.85
    camera.sensor_fit = 'HORIZONTAL'
    camera.sensor_height = 13.365
    camera.sensor_width = 23.76
    camera.show_limits = True
    camera_object = bpy.data.objects.new("Camera", camera)

    cam_collection = camera_collection()
    cam_collection.objects.link(camera_object)
    shot.camera_object = camera_object


def object_must_be_camera(self, ob):
    return ob.type == 'CAMERA'


def sync_timeline(self, context) -> None:
    """Sync Blender's timeline and markers with the shot list"""

    scene = context.scene
    scene.timeline_markers.clear()
    new_start_frame = 1001
    for shot in scene.camera_sequencer_shots:
        marker = scene.timeline_markers.new(
            shot.code, frame=new_start_frame)
        if shot.camera_object != None:
            marker.camera = shot.camera_object
        new_start_frame += shot.duration
    scene.frame_start = 1001
    scene.frame_end = new_start_frame - 1
    return None  # Required by bpy


def setup_metadata_stamping():
    render = bpy.context.scene.render
    render.use_stamp_date = False
    render.use_stamp_time = False
    render.use_stamp_render_time = False
    render.use_stamp_frame = True
    render.use_stamp_frame_range = False
    render.use_stamp_memory = False
    render.use_stamp_hostname = False
    render.use_stamp_camera = True
    render.use_stamp_lens = False
    render.use_stamp_scene = False
    render.use_stamp_marker = False
    render.use_stamp_filename = False
    render.use_stamp_sequencer_strip = False
    render.use_stamp_note = True
    render.stamp_note_text = ''
    render.use_stamp = True
    render.use_stamp_labels = False
    render.stamp_font_size = 20
    render.stamp_foreground = (1, 1, 1, 1)
    render.stamp_background = (0, 0, 0, 0.5)


def enable_dynamic_metadata_note(scene):
    """Frame change handler to update the Metadata Note with every shot's
    description. Released on file close"""

    # Get current shot
    counter = scene.frame_start
    current_shot = None
    for shot in scene.camera_sequencer_shots.values():
        if counter <= scene.frame_current < counter + shot.duration:
            current_shot = shot
            break
        counter += shot.duration

    # Set RenderSettings.stamp_note_text to the current shot's description
    if current_shot:
        camera = current_shot.camera_object.data
        n = shot.notes
        f = round(camera.lens)
        a = camera.dof.aperture_fstop
        d = round(camera.dof.focus_distance, 3)
        scene.render.stamp_note_text = f'{n}\nFocal length: {f}mm\nAperture: {a}\nFocal distance: {d}m'


def clean_up_cameras():
    shots = bpy.context.scene.camera_sequencer_shots
    shot_cameras = [shot.camera_object
                    for shot in shots]
    all_cameras = [ob
                   for ob in bpy.data.objects
                   if ob.type == 'CAMERA']
    # Remove unused cameras
    for camera in all_cameras:
        if camera not in shot_cameras:
            bpy.data.objects.remove(camera)
    # Rename remaining cameras
    for shot in shots:
        shot.camera_object.name = f'{shot.code}.CAM.001'
        shot.camera_object.data.name = shot.camera_object.name
