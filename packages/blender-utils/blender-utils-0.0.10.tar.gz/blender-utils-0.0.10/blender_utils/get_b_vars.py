import bpy

def get_types_object ():
  return bpy.types.Object

def get_app ():
  return bpy.app

def get_ui_list ():
  return bpy.types.UIList

def get_utils ():
  return bpy.utils

def get_operator_file_list_element ():
  return bpy.types.OperatorFileListElement

def get_path ():
  return bpy.path

def get_view_layer ():
  return bpy.context.view_layer

def get_property_group ():
  return bpy.types.PropertyGroup

def get_msgbus ():
  return bpy.msgbus

def get_layer_objects ():
  return bpy.types.LayerObjects

def get_ops ():
  return bpy.ops

def get_mesh ():
  return get_ops().mesh

def get_context ():
  return bpy.context

def get_object ():
  return get_ops().object

def get_armature ():
  return get_ops().armature

def get_active_object ():
  # bpy.context.view_layer.objects.active：可以更明确地操作当前视图层中的激活对象
  # bpy.context.active_object：可以快速获取当前上下文中的激活对象
  # 在大多数情况下，这两个属性的行为是一致的，但在处理复杂场景或多视图层时，
  # 使用 bpy.context.view_layer.objects.active 可能会更加明确和可靠。
  return get_context().active_object

def get_operator ():
  return bpy.types.Operator

def get_panel ():
  return bpy.types.Panel

def get_props ():
  return bpy.props

def get_scene ():
  return bpy.types.Scene 

def get_collections ():
  return bpy.data.collections

def get_bone_widget ():
  return get_ops().bonewidget

def get_data ():
  return bpy.data

