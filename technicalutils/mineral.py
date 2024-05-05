from beet import Context, LootTable, Language, FunctionTag, Function
from dataclasses import dataclass, field

from typing import Any, Literal, TypedDict
from frozendict import frozendict
from .utils import export_translated_string, generate_uuid
from .types import Lang, TranslatedString, NAMESPACE
from .item import Item, BlockProperties, Registry
from .crafting import ShapedRecipe, ShapelessRecipe, NBTSmelting

from pydantic import BaseModel

from enum import Enum
import json

Mineral_list: list["Mineral"] = []
ToolType = Literal["pickaxe","axe","shovel","hoe","sword"]


class SubItem(BaseModel):
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


class SubItemBlock(SubItem):
    block_properties: BlockProperties = field(
        default_factory=lambda: BlockProperties("minecraft:lodestone")
    )

    def get_base_item(self):
        return "minecraft:furnace"



class SubItemDamagable(SubItem):
    max_damage: int 

    def get_components(self):
        return {
            "minecraft:max_stack_size": 1,
            "minecraft:max_damage": self.max_damage,
        }


class SubItemWeapon(SubItemDamagable):
    attack_damage: float
    attack_speed: float

    def get_components(self):
        res = super().get_components()
        res.update({
            "minecraft:attribute_modifiers": {
                "modifiers": [
                {
                    "type": "minecraft:generic.attack_damage",
                    "amount": self.attack_damage,
                    "name": "Tool modifier",
                    "operation": "add_value",
                    "slot": "mainhand",
                    "uuid": generate_uuid(),
                },
                {
                    "type": "minecraft:generic.attack_speed",
                    "amount": self.attack_speed,
                    "name": "Tool modifier",
                    "operation": "add_value",
                    "slot": "mainhand",
                    "uuid": generate_uuid(),
                }
                ]
            }
        })
        return res

class SubItemTool(SubItemWeapon):
    type: ToolType
    tier: Literal["wooden","stone","iron","golden","diamond","netherite"] = "wooden"
    speed : float = 2.0


    def get_components(self):
        res = super().get_components()
        res.update({
            "minecraft:tool": {
                "rules": [
                    {
                        "blocks": f"#minecraft:incorrect_for_{self.tier}_tool",
                        "correct_for_drops": False,
                    },
                    {
                        "blocks": "#minecraft:mineable/pickaxe",
                        "correct_for_drops": True,
                        "speed": self.speed,
                    }
                ],
                "damage_per_block": 1,
            }
        })
        return res
    
    def get_base_item(self):
        return f"minecraft:{self.tier}_{self.type}"



DEFAULT_MINERALS = {
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

class TypingToolArgs(TypedDict):
    attack_damage: float
    attack_speed: float
    max_damage: int
    speed: float
    tier: Literal["wooden","stone","iron","golden","diamond","netherite"]
    translation: TranslatedString
    custom_model_data_offset: int

DEFAULT_TOOLS_ARGS : dict[ToolType,TypingToolArgs] = {
    "pickaxe": {
        "translation": (
            f"{NAMESPACE}.mineral_name.pickaxe",
            {Lang.en_us: "%s Pickaxe", Lang.fr_fr: "Pioche en %s"},
        ),
        "custom_model_data_offset": 10,
    },
    "axe": {
        "translation": (
            f"{NAMESPACE}.mineral_name.axe",
            {Lang.en_us: "%s Axe", Lang.fr_fr: "Hache en %s"},
        ),
        "custom_model_data_offset": 11,
    },
    "shovel": {
        "translation": (
            f"{NAMESPACE}.mineral_name.shovel",
            {Lang.en_us: "%s Shovel", Lang.fr_fr: "Pelle en %s"},
        ),
        "custom_model_data_offset": 12,
    },
    "hoe": {
        "translation": (
            f"{NAMESPACE}.mineral_name.hoe",
            {Lang.en_us: "%s Hoe", Lang.fr_fr: "Houe en %s"},
        ),
        "custom_model_data_offset": 13,
    },
    "sword": {
        "translation": (
            f"{NAMESPACE}.mineral_name.sword",
            {Lang.en_us: "%s Sword", Lang.fr_fr: "Épée en %s"},
        ),
        "custom_model_data_offset": 14,
    },

}




@dataclass
class Mineral:
    id: str
    name: TranslatedString
    custom_model_data: int

    items: dict[ToolType,TypingToolArgs] = field(default_factory=lambda: {})

    def __post_init__(self):
        Mineral_list.append(self)


    def export(self, ctx: Context):
        export_translated_string(ctx, self.name)
        self.export_subitem(ctx)

    def export_subitem(self, ctx: Context):
        for item in self.items.keys():
            if not item in self.items:
                continue
            if self.items[item] is None:
                subitem = DEFAULT_MINERALS[item]
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
            else:
                if item in DEFAULT_TOOLS_ARGS.keys():
                    args = DEFAULT_TOOLS_ARGS[item]
                    args.update(self.items[item])
                    args["type"] = item
                    subitem = SubItemTool(**args)
                else:
                    args = self.items[item]
                    subitem = SubItem(**args)
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
        dust = self.get_item("dust")
        

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
            result=(ingot,1),
            types=["furnace","blast_furnace"],
        ).export(ctx)

        NBTSmelting(
            item=ore,
            result=(ingot,1),
            types=["furnace","blast_furnace"],
        ).export(ctx)

        NBTSmelting(
            item=deepslate_ore,
            result=(ingot,1),
            types=["furnace","blast_furnace"],
        ).export(ctx)

        NBTSmelting(
            item=dust,
            result=(ingot,2),
            types=["furnace","blast_furnace"],
        ).export(ctx)


