from .get_b_vars import get_context, get_collections, get_view_layer

def get_active_collection ():
  return get_view_layer().active_layer_collection

def active_collection (collection_name):
  view_layer = get_view_layer()
  view_layer.active_layer_collection = view_layer.layer_collection.children[collection_name]

def create_collection (collection_name, parent_collection = None):
  new_collection = get_collections().new(collection_name)
  parent_collection = (
    get_collection(parent_collection) 
    if parent_collection 
    else get_context().scene.collection
  )
  parent_collection.children.link(new_collection)

  return new_collection

def get_collection (collection_name):
  return get_collections().get(collection_name)
