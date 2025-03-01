import inspect

from .get_b_vars import get_scene, get_props

def report_info (self, text):
  self.report({'INFO'}, text)

def report_warning (self, text):
  self.report({'WARNING'}, text)

def report_error (self, text):
  self.report({'ERROR'}, text)

def remove_scene_custom_prop (prop):
  delattr(get_scene(), prop)

def add_row_with_label_and_operator (
  layout, 
  data, 
  prop, 
  text,
  op,
  op_text = '',
  icon = ''
):
  row = layout.row()
  row.prop(data, prop, text = text)
  return _add_row_with_operator(row, op, op_text, icon)
      
def _add_row_with_operator (row, operator, text = '', icon = None):
  if icon:
    return row.operator(operator, text = text, icon = icon)
  
  return row.operator(operator, text = text)

def add_row (layout, data, prop, text):
  row = layout.column().row()
  row.prop(data, prop, text = text)

def add_row_with_label (layout, label, data, prop, factor):
  split = layout.column().split(factor = factor)
  row_label = split.row()
  row_label.label(text = label)
  row_prop = split.row()
  row_prop.prop(data, prop, text = "")

def add_row_with_operator (layout, operator, text = '', icon = None):
  row = layout.column().row()
  _add_row_with_operator(row, operator, text, icon)

def add_scene_custom_prop (
  name = None, 
  prop_type = None, 
  default = None, 
  desc = None,
  min = None,
  max = None,
  type = None,
  items = None,
  update = None,
  step = None,
  size = None,
  subtype = None,
  set = None,
  precision = None
):
  kwargs = {}
  
  if name is not None:
    kwargs['name'] = name
  if type is not None:
    kwargs['type'] = type
  if default is not None:
    kwargs['default'] = default
  if desc is not None:
    kwargs['description'] = desc
  if min is not None:
    kwargs['min'] = min
  if max is not None:
    kwargs['max'] = max
  if items is not None:
    kwargs['items'] = items
  if update is not None:
    kwargs['update'] = update
  if step is not None:
    kwargs['step'] = step
  if size is not None:
    kwargs['size'] = size
  if subtype is not None:
    kwargs['subtype'] = subtype
  if set is not None:
    kwargs['set'] = set
  if precision is not None:
    kwargs['precision'] = precision

  print(kwargs)
  fn = getattr(get_props(), f'{ prop_type }Property')
  scene = get_scene()
  setattr(scene, name, fn(**kwargs))
