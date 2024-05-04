
from beet import Context, LootTable, Language, FunctionTag, Function
from dataclasses import dataclass, field

from typing import Any
from frozendict import frozendict
from .utils import generate_uuid, NAMESPACE

from enum import Enum
import json

Mineral_list : list["Mineral"] = []
Registry : dict[str, "Item"] = {}

def beet_default(ctx: Context):
    Mineral(
        id = "silver",
        name = (f"{NAMESPACE}.mineral.silver", {Lang.en_us: "Silver", Lang.fr_fr: "Argent"}),
        custom_model_data = 1430000,
        items_definiton = DEFAULT_ITEMS_DEFINITION,
    )
    Mineral(
        id = "tin",
        name = (f"{NAMESPACE}.mineral.tin", {Lang.en_us: "Tin", Lang.fr_fr: "Étain"}),
        custom_model_data = 1430020,
        items_definiton = DEFAULT_ITEMS_DEFINITION,
    )
    for mineral in Mineral_list:
        mineral.export(ctx).override(ctx)



class Lang(Enum):
    en_us = "en_us"
    fr_fr = "fr_fr"

    @property
    def namespaced(self):
        return f"{NAMESPACE}:{self.value}"

class Rarity(Enum):
    common = "white"
    uncommon = "yellow"
    rare = "aqua"
    epic = "magenta"





TranslatedString = tuple[str,dict[Lang, str]]

TextComponent_base = str | dict
TextComponent = TextComponent_base | list[TextComponent_base]

def export_translated_string(ctx: Context, translation: TranslatedString):
    # create default languages files if they don't exist
    for lang in Lang:
        if lang.namespaced not in ctx.assets.languages:
            ctx.assets.languages[lang.namespaced] = Language({})

    for lang, translate in translation[1].items():
        ctx.assets.languages[f"{NAMESPACE}:{lang.value}"].data[translation[0]] = translate


@dataclass
class BlockProperties():
    base_block : str


@dataclass
class Item():
    id : str
    # the translation key, the 
    item_name : TextComponent
    lore : list[TextComponent_base] = field(default_factory=list)

    components_extra : dict[str, Any] = field(default_factory=dict)

    base_item : str = "minecraft:jigsay"
    custom_model_data : int = 1430000

    block_properties : BlockProperties = None

    def create_translation(self, ctx: Context):
        # add the translations to the languages files for item_name
        if not isinstance(self.item_name, dict):
            export_translated_string(ctx, self.item_name)

        # add the translations to the languages files for lore
        for lore_line in self.lore:
            export_translated_string(ctx, lore_line)
        
    
    def create_lore(self):
        lore = []
        if self.lore:
            lore.append(*self.lore)
        lore.append({"translate": f"{NAMESPACE}.name", "color": "blue", "italic": True})
        return lore
    

    def create_custom_data(self):
        return {
            "smithed": {
                "id": f"{NAMESPACE}:{self.id}"
            }
        }
    
    def create_block_placement_data(self):
        if self.block_properties:
            return [
                {
                    "function": "minecraft:set_contents",
                    "component": "minecraft:container",
                    "entries": [
                        {
                            "type": "minecraft:item",
                            "name": "minecraft:stone",
                            "functions": [
                                {
                                    "function": "minecraft:set_components",
                                    "components": {
                                        "minecraft:custom_data": {
                                            "smithed": {
                                                "block": {
                                                    "id": f"{NAMESPACE}:{self.id}"
                                                }
                                        }
                                    }
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        return []
    
    def create_custom_block(self, ctx: Context):
        if not self.block_properties:
            return
        smithed_function_tag_id = f"smithed.custom_block:event/on_place"
        internal_function_id = f"{NAMESPACE}:impl/smithed.custom_block/on_place"
        if smithed_function_tag_id not in ctx.data.function_tags:
            ctx.data.function_tags[smithed_function_tag_id] = FunctionTag()
            ctx.data.function_tags[smithed_function_tag_id].data["values"].append(internal_function_id)

        if internal_function_id not in ctx.data.functions:
            ctx.data.functions[internal_function_id] = Function()
        
        ctx.data.functions[internal_function_id].append(f"""
execute
    if data storage smithed.custom_block:main {{blockApi:{{id:"{NAMESPACE}:{self.id}"}}}}
    run function ./on_place/{self.id}:
        setblock ~ ~ ~ {self.block_properties.base_block}
        execute 
            summon item_display
            run function ./on_place/{self.id}/place_entity:
                tag @s add {NAMESPACE}.{self.id}
                tag @s add {NAMESPACE}.block
                tag @s add {NAMESPACE}.block.{self.block_properties.base_block.replace("minecraft:", "")}
                tag @s add smithed.block
                tag @s add smithed.strict
                tag @s add smithed.entity

                data modify entity @s item set value {{id:"{self.base_item}",count:1,components:{{"minecraft:custom_model_data":{self.custom_model_data}}}}}

                data merge entity @s {{transformation:{{scale:[1.001f,1.001f,1.001f]}}}}
""")

    def set_components(self):
        res = []
        for key, value in self.components_extra.items():
            res.append({
                "function": "minecraft:set_component",
                "components": {
                    key: value
                }
            })
        return res
    

    
    def create_loot_table(self, ctx: Context):
        ctx.data.loot_tables[f"{NAMESPACE}:items/{self.id}"] = LootTable({
            "pools": [
                {
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:item",
                            "name": self.base_item,
                            "functions": [
                                {
                                    "function": "minecraft:set_components",
                                    "components": {
                                        "minecraft:custom_model_data": self.custom_model_data,
                                        "minecraft:custom_data": self.create_custom_data(),
                                    }
                                },
                                {
                                    "function": "minecraft:set_name",
                                    "entity": "this",
                                    "target": "item_name",
                                    "name": self.item_name
                                },
                                {
                                    "function": "minecraft:set_lore",
                                    "entity": "this",
                                    "lore": self.create_lore(),
                                    "mode": "replace_all"
                                },
                                *self.set_components(),
                                *self.create_block_placement_data()
                            ]
                        }
                    ]
                }
            ]
        })

    def export(self, ctx: Context):
        assert self.id not in Registry, f"Item {self.id} already exists"
        Registry[self.id] = self
        self.create_loot_table(ctx)
        self.create_translation(ctx)
        self.create_custom_block(ctx)





MINERAL_NORMAL = [
    "ore",
    "deepslate_ore",
    "raw_ore",
    "ingot",
    "nugget",
    "raw_block",
    "block",
]

MINERAL_TOOLS = MINERAL_NORMAL + [
    "axe",
    "hoe",
    "shovel",
    "pickaxe",
    "sword",
]

MINERAL_ARMOR = MINERAL_NORMAL + [
    "helmet",
    "chestplate",
    "leggings",
    "boots",
]

MINERAL_TOOLS_ARMOR = MINERAL_TOOLS + MINERAL_ARMOR


@dataclass
class SubItem():
    translation : TranslatedString
    custom_model_data_offset : int
    block_properties : BlockProperties = None

    def get_item_name(self, translation: TranslatedString):
        return {
            "translate": self.translation[0],
            "with": [
                {"translate": translation[0]}
            ],
            "color": "white"
        }
    
    def get_components(self):
        return {}
    
    def get_base_item(self):
        return "minecraft:jigsaw"
    
    def export(self, ctx: Context):
        export_translated_string(ctx, self.translation)

@dataclass
class SubItemBlock(SubItem):
    block_properties : BlockProperties = field(default_factory=lambda: BlockProperties("minecraft:lodestone"))
    def get_base_item(self):
        return "minecraft:furnace"


DEFAULT_ITEMS_DEFINITION = {
    "ore": SubItemBlock(
        translation = (f"{NAMESPACE}.mineral_name.ore", {Lang.en_us: "%s Ore", Lang.fr_fr: "Minerai de %s"}),
        custom_model_data_offset = 0
    ),
    "deepslate_ore": SubItemBlock(
        translation = (f"{NAMESPACE}.mineral_name.deepslate_ore", {Lang.en_us: "Deepslate %s Ore", Lang.fr_fr: "Minerai de deepslate de %s"}),
        custom_model_data_offset = 1
    ),
    "raw_ore": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.raw_ore", {Lang.en_us: "Raw %s Ore", Lang.fr_fr: "Minerai brut de %s"}),
        custom_model_data_offset = 2
    ),
    "ingot": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.ingot", {Lang.en_us: "%s Ingot", Lang.fr_fr: "Lingot de %s"}),
        custom_model_data_offset = 3
    ),
    "nugget": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.nugget", {Lang.en_us: "%s Nugget", Lang.fr_fr: "Pépite de %s"}),
        custom_model_data_offset = 4
    ),
    "raw_block": SubItemBlock(
        translation = (f"{NAMESPACE}.mineral_name.raw_block", {Lang.en_us: "Raw %s Block", Lang.fr_fr: "Bloc brut de %s"}),
        custom_model_data_offset = 5
    ),
    "block": SubItemBlock(
        translation = (f"{NAMESPACE}.mineral_name.block", {Lang.en_us: "%s Block", Lang.fr_fr: "Bloc de %s"}),
        custom_model_data_offset = 6
    ),
}

@dataclass
class Mineral():
    id : str
    name : TranslatedString
    custom_model_data : int

    items_definiton : dict[str, SubItem]


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
                id = f"{self.id}_{item}",
                item_name = subitem.get_item_name(self.name),
                custom_model_data = self.custom_model_data + subitem.custom_model_data_offset,
                components_extra=subitem.get_components(),
                base_item = subitem.get_base_item(),
                block_properties = subitem.block_properties,
            ).export(ctx)
        return self


        









