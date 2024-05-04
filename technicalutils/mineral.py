
from beet import Context, LootTable, Language
from dataclasses import dataclass, field

from typing import Any
from frozendict import frozendict
from .utils import generate_uuid

from enum import Enum
import uuid
NAMESPACE = "technicalutils"


Mineral_list : list["Mineral"] = []

def beet_default(ctx: Context):
    for mineral in Mineral_list:
        mineral().export(ctx).override(ctx)



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
class Item():
    id : str
    # the translation key, the 
    item_name : TextComponent
    lore : list[TextComponent_base] = field(default_factory=list)

    components_extra : dict[str, Any] = field(default_factory=dict)

    base_item : str = "minecraft:jigsay"
    custom_model_data : int = 1430000


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
        lore.append({"translate": f"{NAMESPACE}.name", "color": "blue", "italic": "true"})
        return lore
    

    def create_custom_data(self):
        return {
            "smithed": {
                "id": f"{NAMESPACE}:{self.id}"
            }
        }
    
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
                                        "minecraft:item_name": self.item_name,
                                        "minecraft:custom_model_data": self.custom_model_data,
                                        "minecraft:lore": self.create_lore(),
                                        "minecraft:custom_data": self.create_custom_data(),
                                    }
                                },
                                *self.set_components()
                            ]
                        }
                    ]
                }
            ]
        })

    def export(self, ctx: Context):
        self.create_loot_table(ctx)
        self.create_translation(ctx)





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
class NormalSubItem(SubItem):
    ...

@dataclass
class ToolSubItem(SubItem):
    max_damage : int

    def get_components(self):
        return {
            "minecraft:max_damage": self.max_damage
        }
    
@dataclass
class ArmorSubItem(SubItem):
    armor : float
    armor_toughness : float

    def get_components(self):
        return {
            "minecraft:attribute_modifiers": {
                "modifiers": [
                    {
                        "type": "minecraft:generic.armor",
                        "uuid": generate_uuid(),
                        "amount": self.armor
                    },
                    {
                        "type": "minecraft:generic.armor_toughness",
                        "uuid": generate_uuid(),
                        "amount": self.armor_toughness
                    }
                ]
            }
        }


DEFAULT_ITEMS_DEFINITION = {
    "ore": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.ore", {Lang.en_us: "%s Ore", Lang.fr_fr: "Minerai de %s"}),
        custom_model_data_offset = 0
    ),
    "deepslate_ore": SubItem(
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
    "raw_block": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.raw_block", {Lang.en_us: "Raw %s Block", Lang.fr_fr: "Bloc brut de %s"}),
        custom_model_data_offset = 5
    ),
    "block": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.block", {Lang.en_us: "%s Block", Lang.fr_fr: "Bloc de %s"}),
        custom_model_data_offset = 6
    ),
    "axe": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.axe", {Lang.en_us: "%s Axe", Lang.fr_fr: "Hache en %s"}),
        custom_model_data_offset = 7
    ),
    "hoe": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.hoe", {Lang.en_us: "%s Hoe", Lang.fr_fr: "Houe en %s"}),
        custom_model_data_offset = 8
    ),
    "shovel": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.shovel", {Lang.en_us: "%s Shovel", Lang.fr_fr: "Pelle en %s"}),
        custom_model_data_offset = 9
    ),
    "pickaxe": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.pickaxe", {Lang.en_us: "%s Pickaxe", Lang.fr_fr: "Pioche en %s"}),
        custom_model_data_offset = 10
    ),
    "sword": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.sword", {Lang.en_us: "%s Sword", Lang.fr_fr: "Épée en %s"}),
        custom_model_data_offset = 11
    ),
    "helmet": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.helmet", {Lang.en_us: "%s Helmet", Lang.fr_fr: "Casque en %s"}),
        custom_model_data_offset = 12
    ),
    "chestplate": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.chestplate", {Lang.en_us: "%s Chestplate", Lang.fr_fr: "Plastron en %s"}),
        custom_model_data_offset = 13,
    ),
    "leggings": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.leggings", {Lang.en_us: "%s Leggings", Lang.fr_fr: "Jambières en %s"}),
        custom_model_data_offset = 14
    ),
    "boots": SubItem(
        translation = (f"{NAMESPACE}.mineral_name.boots", {Lang.en_us: "%s Boots", Lang.fr_fr: "Bottes en %s"}),
        custom_model_data_offset = 15
    ),
}

@dataclass
class Mineral():
    id : str
    name : TranslatedString
    custom_model_data : int

    items_definiton : frozendict[str, SubItem] = field(default_factory=lambda: DEFAULT_ITEMS_DEFINITION)


    items : list[str] = field(default_factory=lambda: MINERAL_NORMAL)


    def __init__(self) -> None:
        # iterate over Mineral type annotations
        for key, type_annotation in self.__annotations__.items():
            # find the key in self.__dict__ and assign the value to it
            value = getattr(self, key)
            casted_value = type_annotation(value)
            setattr(self, key, casted_value)

    def __init_subclass__(cls) -> None:
        Mineral_list.append(cls)

    def override(self, ctx: Context):
        # override the default values, can be used in sub-classes
        pass

    def export(self, ctx: Context):
        for item in set(self.items):
            subitem = self.items_definiton[item]
            subitem.export(ctx)

            Item(
                id = f"{self.id}_{item}",
                item_name = subitem.get_item_name(self.name),
                custom_model_data = self.custom_model_data + subitem.custom_model_data_offset,
                components_extra=subitem.get_components(),
            ).export(ctx)
        return self


        







class Silver(Mineral):
    id = "silver"
    name = (f"{NAMESPACE}.mineral.silver", {Lang.en_us: "Silver", Lang.fr_fr: "Argent"})
    custom_model_data = 1430000

    items = MINERAL_TOOLS_ARMOR

class Tin(Mineral):
    id = "tin"
    name = (f"{NAMESPACE}.mineral.tin", {Lang.en_us: "Tin", Lang.fr_fr: "Étain"})
    custom_model_data = 1430020

    items = MINERAL_NORMAL






