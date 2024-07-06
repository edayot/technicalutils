from beet import Context
from .types import NAMESPACE, Lang
from .mineral import Mineral
from .item import Item, Registry
from .crafting import VanillaItem, ShapedRecipe


def beet_default(ctx: Context):
    Mineral(
        id="silver",
        name=(
            f"{NAMESPACE}.mineral.silver",
            {Lang.en_us: "Silver", Lang.fr_fr: "Argent"},
        ),
        custom_model_data=1431000,
        items={
            "ore": {
                "block_properties": {
                    "base_block": "minecraft:lodestone",
                    "world_generation": [{
                        "min_y": 10,
                        "max_y": 40,
                        "min_veins": 1,
                        "max_veins": 3,
                        "min_vein_size": 4,
                        "max_vein_size": 10,
                        "ignore_restrictions": 0
                    }]
                }
            },
            "deepslate_ore": {
                "block_properties": {
                    "base_block": "minecraft:lodestone",
                    "world_generation": [{
                        "min_y": -10,
                        "max_y": 5,
                        "min_veins": 1,
                        "max_veins": 2,
                        "min_vein_size": 4,
                        "max_vein_size": 5,
                        "ignore_restrictions": 0,
                    }]
                }
            },
            "block": {},
            "raw_ore_block": {},
            "ingot": {},
            "nugget": {},
            "raw_ore": {},
            "dust": {},
            "pickaxe": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 4,
                "attack_speed": 1.2,
            },
            "axe": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 9,
                "attack_speed": 0.9,
            },
            "shovel": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 2,
                "attack_speed": 1,
            },
            "hoe": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 1,
                "attack_speed": 3,
            },
            "sword": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 6,
                "attack_speed": 1.6,
            },
            "helmet": {
                "armor": 6,
                "armor_toughness": 2,
                "max_damage": 200,
                "additional_attributes": {
                    "minecraft:generic.movement_speed": {
                        "amount": -0.0015,
                        "slot": "armor",
                    }
                }
            },
            "chestplate": {
                "armor": 3,
                "armor_toughness": 1,
                "max_damage": 300,
                "additional_attributes": {
                    "minecraft:generic.movement_speed": {
                        "amount": -0.0015,
                        "slot": "armor",
                    }
                }
            },
            "leggings": {
                "armor": 5,
                "armor_toughness": 2,
                "max_damage": 290,
                "additional_attributes": {
                    "minecraft:generic.movement_speed": {
                        "amount": -0.0015,
                        "slot": "armor",
                    }
                }
            },
            "boots": {
                "armor": 2,
                "armor_toughness": 1,
                "max_damage": 250,
                "additional_attributes": {
                    "minecraft:generic.movement_speed": {
                        "amount": -0.0015,
                        "slot": "armor",
                    }
                }
            },
        },
    ).export(ctx)
    item_cable = Item(
        id="item_cable",
        item_name=(
            f"{NAMESPACE}.item.item_cable",
            {Lang.en_us: "Item Cable", Lang.fr_fr: "Câble d'objet"},
        ),
        custom_model_data=1432001,
        custom_model_data_placed=1430000,
        base_item="minecraft:furnace",
        base_item_placed="minecraft:light_gray_stained_glass_pane",
        block_properties={
            'base_block': 'minecraft:conduit',
            'smart_waterlog': True,
        }
    )
    silver_ingot = Registry.get("silver_ingot")
    redstone = VanillaItem("minecraft:redstone")
    iron_ingot = VanillaItem("minecraft:iron_ingot")
    glass = VanillaItem("minecraft:glass")

    ShapedRecipe(
        [
            [iron_ingot, glass, iron_ingot],
            [silver_ingot, redstone, silver_ingot],
            [iron_ingot, glass, iron_ingot],
        ],
        (item_cable, 16)
    ).export(ctx)

