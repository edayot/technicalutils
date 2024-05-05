

from .item import Registry
from .mineral import Mineral_list
from beet import Context


def beet_default(ctx: Context):
    """
    We need to export items in custom_model_data order
    """
    for mineral in Mineral_list:
        mineral.export(ctx)
    items = Registry.values()
    items = sorted(items, key=lambda x: x.custom_model_data)
    for item in items:
        item.export(ctx)




