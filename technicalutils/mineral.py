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

Mineral_list: list["Mineral"] = []


def beet_default(ctx: Context):
    Mineral(
        id="silver",
        name=(
            f"{NAMESPACE}.mineral.silver",
            {Lang.en_us: "Silver", Lang.fr_fr: "Argent"},
        ),
        custom_model_data=1430000,
        items_definiton=DEFAULT_ITEMS_DEFINITION,
    )
    Mineral(
        id="tin",
        name=(f"{NAMESPACE}.mineral.tin", {Lang.en_us: "Tin", Lang.fr_fr: "Étain"}),
        custom_model_data=1430020,
        items_definiton=DEFAULT_ITEMS_DEFINITION,
    )
    for mineral in Mineral_list:
        mineral.export(ctx).override(ctx)


@dataclass
class SubItem:
    translation: TranslatedString
    custom_model_data_offset: int
    block_properties: BlockProperties = None
    is_cookable: bool = False

    def get_item_name(self, translation: TranslatedString):
        return {
            "translate": self.translation[0],
            "with": [{"translate": translation[0]}],
            "color": "white",
        }

    def get_components(self):
        return {}

    def get_base_item(self):
        return "minecraft:jigsaw"

    def export(self, ctx: Context):
        export_translated_string(ctx, self.translation)


@dataclass
class SubItemBlock(SubItem):
    block_properties: BlockProperties = field(
        default_factory=lambda: BlockProperties("minecraft:lodestone")
    )

    def get_base_item(self):
        return "minecraft:furnace"


DEFAULT_ITEMS_DEFINITION = {
    "ore": SubItemBlock(
        translation=(
            f"{NAMESPACE}.mineral_name.ore",
            {Lang.en_us: "%s Ore", Lang.fr_fr: "Minerai de %s"},
        ),
        custom_model_data_offset=0,
        is_cookable=True,
    ),
    "deepslate_ore": SubItemBlock(
        translation=(
            f"{NAMESPACE}.mineral_name.deepslate_ore",
            {Lang.en_us: "Deepslate %s Ore", Lang.fr_fr: "Minerai de deepslate de %s"},
        ),
        custom_model_data_offset=1,
        is_cookable=True,
    ),
    "raw_ore": SubItem(
        translation=(
            f"{NAMESPACE}.mineral_name.raw_ore",
            {Lang.en_us: "Raw %s Ore", Lang.fr_fr: "Minerai brut de %s"},
        ),
        custom_model_data_offset=2,
        is_cookable=True,
    ),
    "ingot": SubItem(
        translation=(
            f"{NAMESPACE}.mineral_name.ingot",
            {Lang.en_us: "%s Ingot", Lang.fr_fr: "Lingot de %s"},
        ),
        custom_model_data_offset=3,
    ),
    "nugget": SubItem(
        translation=(
            f"{NAMESPACE}.mineral_name.nugget",
            {Lang.en_us: "%s Nugget", Lang.fr_fr: "Pépite de %s"},
        ),
        custom_model_data_offset=4,
    ),
    "raw_ore_block": SubItemBlock(
        translation=(
            f"{NAMESPACE}.mineral_name.raw_block",
            {Lang.en_us: "Raw %s Block", Lang.fr_fr: "Bloc brut de %s"},
        ),
        custom_model_data_offset=5,
    ),
    "block": SubItemBlock(
        translation=(
            f"{NAMESPACE}.mineral_name.block",
            {Lang.en_us: "%s Block", Lang.fr_fr: "Bloc de %s"},
        ),
        custom_model_data_offset=6,
    ),
    "dust": SubItem(
        translation=(
            f"{NAMESPACE}.mineral_name.dust",
            {Lang.en_us: "%s Dust", Lang.fr_fr: "Poudre de %s"},
        ),
        custom_model_data_offset=7,
        is_cookable=True,
    ),
}


@dataclass
class Mineral:
    id: str
    name: TranslatedString
    custom_model_data: int

    items_definiton: dict[str, SubItem]

    def __post_init__(self):
        Mineral_list.append(self)

    def override(self, ctx: Context):
        # override the default values, can be used in sub-classes
        pass

    def export(self, ctx: Context):
        export_translated_string(ctx, self.name)
        for item in self.items_definiton:
            subitem = self.items_definiton[item]
            subitem.export(ctx)
            Item(
                id=f"{self.id}_{item}",
                item_name=subitem.get_item_name(self.name),
                custom_model_data=self.custom_model_data + subitem.custom_model_data_offset,
                components_extra=subitem.get_components(),
                base_item=subitem.get_base_item(),
                block_properties=subitem.block_properties,
                is_cookable=subitem.is_cookable,
            )
        self.generate_crafting_recipes(ctx)
        return self
    
    def get_item(self, item: str):
        return Registry[f"{self.id}_{item}"]

    def generate_crafting_recipes(self, ctx: Context):
        block = self.get_item("block")
        raw_ore_block = self.get_item("raw_ore_block")
        ingot = self.get_item("ingot")
        nugget = self.get_item("nugget")
        raw_ore = self.get_item("raw_ore")
        ore = self.get_item("ore")
        deepslate_ore = self.get_item("deepslate_ore")
        

        ShapedRecipe(
            items=[
                [raw_ore, raw_ore, raw_ore],
                [raw_ore, raw_ore, raw_ore],
                [raw_ore, raw_ore, raw_ore],
            ],
            result=(raw_ore_block,1),
        ).export(ctx)

        ShapedRecipe(
            items=[
                [ingot, ingot, ingot],
                [ingot, ingot, ingot],
                [ingot, ingot, ingot],
            ],
            result=(block,1),
        ).export(ctx)

        ShapedRecipe(
            items=[
                [nugget, nugget, nugget],
                [nugget, nugget, nugget],
                [nugget, nugget, nugget],
            ],
            result=(ingot,1),
        ).export(ctx)

        ShapelessRecipe(
            items=[(ingot, 1)],
            result=(nugget, 9),
        ).export(ctx)

        ShapelessRecipe(
            items=[(block, 1)],
            result=(ingot, 9),
        ).export(ctx)

        ShapelessRecipe(
            items=[(raw_ore_block, 1)],
            result=(raw_ore, 9),
        ).export(ctx)

        NBTSmelting(
            item=raw_ore,
            result=ingot,
        ).export(ctx)
