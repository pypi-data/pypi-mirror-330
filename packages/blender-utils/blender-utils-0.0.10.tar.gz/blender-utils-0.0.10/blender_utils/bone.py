from .get_b_vars import *
from .other import set_mode

def deselect ():
  get_armature().select_all(action = 'DESELECT')

def select_bone (bone):
  if bone:
    bone.select = True
    bone.select_head = True
    bone.select_tail = True

def select_bone_head (bone):
  if bone:
    bone.select = False
    bone.select_head = True
    bone.select_tail = False
   
def select_bone_tail (bone):
  if bone:
    bone.select = False
    bone.select_head = False
    bone.select_tail = True

def scale_bone (bone, scale_factor):
  bone.length *= scale_factor

def get_bone_collections (armature):
  return armature.data.collections

def copy_bone (
  bone, 
  name = None, 
  scale_factor = None, 
  parent = None,
  use_connect = True,
  clear_parent = False,
  roll = False,
  roll_type = 'GLOBAL_POS_Z'
):
  deselect()
  select_bone(bone)
  # 如果复制前1不关闭相连项，会出现  context.selected_bones 长度为0，原因还没找到
  if bone.use_connect == True:
    bone.use_connect = False
    get_armature().duplicate()
    bone.use_connect = True
  else:
    get_armature().duplicate()
  # 复制完成后会自动选中新的内容同时取消选中之前的内容
  copyed_bone = get_context().selected_bones[0]    
  
  if name:
    copyed_bone.name = name

  if scale_factor:
    scale_bone(copyed_bone, scale_factor)

  if parent:
    set_parent(copyed_bone, parent, use_connect)

  if clear_parent:
    set_parent(copyed_bone, None, False)

  if roll:
    calculate_roll(copyed_bone, roll_type)

  deselect()
  
  return copyed_bone

def duplicate ():
  get_armature().duplicate()

def calculate_roll (bone, type = 'GLOBAL_POS_Z'):
    bone.select = True
    bone.select_head = True
    bone.select_tail = True
    get_armature().calculate_roll(type = type)
    deselect()

def extrude_bone (
  bone, 
  direction, 
  vector_or_target_bone, 
  target_bone_direction = 'head', 
  use_connect = False,
  name = None,
  parent = None,
  parent_connect = True,
  clear_parent = False,
  roll = False,
  roll_type = 'GLOBAL_POS_Z'
):
    bone.select = False

    if direction == 'head':
        bone.select_head = True
        bone.select_tail = False
    else:
        bone.select_head = False
        bone.select_tail = True

    if isinstance(vector_or_target_bone, tuple):
        vector = vector_or_target_bone
    elif target_bone_direction == 'head':
        if direction == 'head':
            vector = vector_or_target_bone.head - bone.head
        else:
            vector = vector_or_target_bone.head - bone.tail
    elif direction == 'head':
        vector = vector_or_target_bone.tail - bone.head
    else:
        vector = vector_or_target_bone.tail - bone.tail

    get_armature().extrude_move(TRANSFORM_OT_translate={ "value": vector })
    deselect()

    new_bone = get_active_object().data.edit_bones[-1]
    new_bone.use_connect = use_connect
    
    if name:
       new_bone.name = name

    if parent:
      set_parent(new_bone, parent, parent_connect)

    if clear_parent:
      set_parent(new_bone, None)

    if roll:
      calculate_roll(new_bone, roll_type)

    return new_bone

def symmetrize_bones (bone_names):
  set_mode('EDIT')

  for bone_name in bone_names:
    bone = get_edit_bone(bone_name)
    select_bone(bone)

  get_armature().symmetrize()
  deselect()

def get_pose_bones (armature = None):
  if armature:
    return armature.pose.bones
  else:
    return get_active_object().pose.bones

def get_pose_bone (name, armature = None):
  return get_pose_bones(armature).get(name)

def get_edit_bones (armature = None):
  if armature:
    return armature.data.edit_bones
  else:
    return get_active_object().data.edit_bones

def get_edit_bone (name, armature = None):
  return get_edit_bones(armature).get(name)

def get_last_bone (bone):
  last_bone = bone
  
  while len(last_bone.children):
      last_bone = last_bone.children[0]

  return last_bone

def get_selected_bone ():
  selected_bones = get_selected_bones()
  
  return selected_bones[0] if len(selected_bones) else None

def get_selected_bones ():
  return get_context().selected_bones

def get_selected_pose_bone ():
  selected_pose_bones = get_selected_pose_bones()
  
  return selected_pose_bones[0] if len(selected_pose_bones) else None

def get_selected_pose_bones ():
  return get_context().selected_pose_bones

def get_bone_chain (bone):
  last_bone = bone
  list = [last_bone]

  while len(last_bone.children):
    last_bone = last_bone.children[0]
    list.append(last_bone)

  return list

def set_parent (bone, target, use_connect = True):
  bone.use_connect = use_connect
  bone.parent = target

def switch_direction (bone):
  select_bone(bone)
  get_armature().switch_direction()
