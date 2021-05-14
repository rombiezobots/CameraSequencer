# Camera Sequencer
Camera Sequencer provides a shot list interface for Blender's native timeline. It allows you to create shots, define their duration, rearrange them, keep notes, and reallocate cameras.

## Tools
Press the `+` button to **create a new shot**. It will automatically be linked to a new camera, found in the `cameras.GRP.001` collection and attached to a marker in the Timeline. This causes Blender to automatically switch cameras when playing or rendering your scene. Your first shot will start on the default starting frame, configurable **above the main interface**.

**Changing the shot's duration** will update the timeline, including moving subsequent shots, and updating the scene's end frame. Each shot's duration in seconds is automatically calculated based on the scene's frame rate, configurable in Blender's Output Properties.

`×` clears the entire shot list and deletes the associated cameras. `🧹` removes any cameras that aren't linked to any shots, and auto-renames the ones that are.

## Navigation
Use the `◂` and `▸` buttons to **skip to shots** in the timeline. Click a shot's name to **jump to that shot**. `🔎` uses Blender's Preview Range to isolate the selected shot during playback.
