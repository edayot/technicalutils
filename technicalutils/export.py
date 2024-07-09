from .item import Registry, Item
from .crafting import VanillaRegistry, VanillaItem
from beet import Context, Texture, Font
from model_resolver import beet_default as model_resolver
from PIL import Image
from .utils import NAMESPACE






def beet_default(ctx: Context):
    """
    We need to export items in custom_model_data order
    """
    items = Registry.values()
    items = sorted(items, key=lambda x: x.custom_model_data)
    for item in items:
        item.export(ctx)

    
    