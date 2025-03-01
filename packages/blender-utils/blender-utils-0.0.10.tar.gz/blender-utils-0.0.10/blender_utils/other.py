import bpy

from .get_b_vars import get_context, get_active_object, get_object

def set_current_frame (frame):
  return bpy.context.scene.frame_set(frame)

def get_current_frame ():
  return bpy.context.scene.frame_current

def get_materials ():
  return get_context().object.data.materials

def update_view ():
  bpy.context.view_layer.update()

def get_shape_keys (name):
  shape_keys = bpy.data.shape_keys.get(name)

  return shape_keys.key_blocks if shape_keys else None

def get_material (material_name):
  return bpy.data.materials.get(material_name)

def create_material (material_name):
  return bpy.data.materials.new(material_name)

def get_mode ():
  return bpy.context.mode

def set_mode (mode):
  bpy.ops.object.mode_set(mode = mode)

def get_selected_objects ():
  return get_context().selected_objects

def get_selected_object ():
  return get_context().selected_objects[0]

def get_object_ (name):
  return bpy.data.objects.get(name)

def select_all_objects (action = 'SELECT'):
  # TOGGLE – Toggle selection for all elements.
  # SELECT – Select all elements.
  # DESELECT – Deselect all elements.
  # INVERT – Invert selection of all elements.

  get_object().select_all(action = action)

def snap_cursor (location = (0, 0, 0)):
  context = get_context()
  prev_context = context.area.type
  context.area.type = 'VIEW_3D'
  # bpy.ops.view3d.snap_cursor_to_center()
  context.scene.cursor.location = location
  context.area.type = prev_context
  
def snap_cursor_to_selected ():
  context = get_context()
  prev_context = context.area.type
  context.area.type = 'VIEW_3D'
  bpy.ops.view3d.snap_cursor_to_selected()
  location = context.scene.cursor.location
  context.area.type = prev_context

  return location

def snap_selected_to_cursor ():
  context = get_context()
  prev_context = context.area.type
  context.area.type = 'VIEW_3D'
  bpy.ops.view3d.snap_selected_to_cursor()
  context.area.type = prev_context

def active_object_ (object):
  get_context().view_layer.objects.active = object

def register_classes (classes):
  register, unregister = bpy.utils.register_classes_factory(classes)
  register()

def unregister_classes (classes):
  register, unregister = bpy.utils.register_classes_factory(classes)
  unregister()
