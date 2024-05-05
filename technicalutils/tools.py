from beet import Context, LootTable, Language, FunctionTag, Function
from dataclasses import dataclass, field

from typing import Any
from frozendict import frozendict
from .utils import export_translated_string
from .types import Lang, TranslatedString, NAMESPACE
from .item import Item, BlockProperties, Registry
from .crafting import ShapedRecipe, ShapelessRecipe, NBTSmelting

from enum import Enum
import json



def beet_default(ctx: Context):
    pass



