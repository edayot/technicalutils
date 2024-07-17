from beet import Context
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.mineral import Mineral
from simple_item_plugin.item import Item
from simple_item_plugin.crafting import VanillaItem, ShapedRecipe, SimpledrawerMaterial, ShapelessRecipe
from simple_item_plugin.utils import export_translated_string
import json

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
        base_item="minecraft:conduit",
        block_properties={
            'base_block': 'minecraft:conduit',
            'smart_waterlog': True,
            'base_item_placed': 'minecraft:light_gray_stained_glass_pane',
            'custom_model_data_placed': 1430000,
        }
    ).export(ctx)
    silver_ingot = ctx.meta.get("registry",{}).get("items",{}).get("silver_ingot")
    redstone = VanillaItem("minecraft:redstone")
    iron_ingot = VanillaItem("minecraft:iron_ingot")
    glass = VanillaItem("minecraft:glass")
    redstone_block = VanillaItem("minecraft:redstone_block")
    comparator = VanillaItem("minecraft:comparator")
    hopper = VanillaItem("minecraft:hopper")

    ShapedRecipe(
        [
            [iron_ingot, glass, iron_ingot],
            [silver_ingot, redstone, silver_ingot],
            [iron_ingot, glass, iron_ingot],
        ],
        (item_cable, 16)
    ).export(ctx)

    servo_extract = Item(
        id="servo_extract",
        item_name=(
            f"{NAMESPACE}.item.servo_extract",
            {Lang.en_us: "Servo Extract", Lang.fr_fr: "Servo Extracteur"},
        ),
        custom_model_data=1432002,
        base_item="minecraft:item_frame",
        components_extra={
            "minecraft:entity_data": {
                "id": "minecraft:item_frame",
                "Tags": [f"{NAMESPACE}.servo.summoned", f"{NAMESPACE}.servo.extract"],
                "Invisible": 1,
            }
        }
    ).export(ctx)

    servo_insert = Item(
        id="servo_insert",
        item_name=(
            f"{NAMESPACE}.item.servo_insert",
            {Lang.en_us: "Servo Insert", Lang.fr_fr: "Servo Inserteur"},
        ),
        custom_model_data=1432004,
        base_item="minecraft:item_frame",
        components_extra={
            "minecraft:entity_data": {
                "id": "minecraft:item_frame",
                "Tags": [f"{NAMESPACE}.servo.summoned", f"{NAMESPACE}.servo.insert"],
                "Invisible": 1,
            }
        }
    ).export(ctx)
    ShapedRecipe(
        [
            [None, redstone_block, None],
            [silver_ingot, comparator, silver_ingot],
        ],
        (servo_extract, 1)
    ).export(ctx)
    ShapedRecipe(
        [
            [silver_ingot, comparator, silver_ingot],
            [None, redstone_block, None],
        ],
        (servo_insert, 1)
    ).export(ctx)

    servo = (
        f"{NAMESPACE}.servo",
        {Lang.en_us: "Servo", Lang.fr_fr: "Servo"},
    )
    export_translated_string(ctx, servo)
    SimpledrawerMaterial(
        block=servo_extract,
        ingot=servo_insert,
        nugget=None,
        material_id=f"{NAMESPACE}.servo",
        material_name=f'{json.dumps({"translate": servo[0],})}',
        ingot_in_block=1,
        nugget_in_ingot=1,
    ).export(ctx)


    wrench = Item(
        id="wrench",
        item_name=(
            f"{NAMESPACE}.item.wrench",
            {Lang.en_us: "Wrench", Lang.fr_fr: "Clé à molette"},
        ),
        custom_model_data=1432006,
    ).export(ctx)

    ShapedRecipe(
        [
            [None, iron_ingot, None],
            [None, silver_ingot, iron_ingot],
            [iron_ingot, None, None],
        ],
        (wrench, 1)
    ).export(ctx)

    id_filter = Item(
        id="id_filter",
        item_name=(
            f"{NAMESPACE}.item.id_filter",
            {Lang.en_us: "ID Filter", Lang.fr_fr: "Filtre d'ID"},
        ),
        custom_model_data=1432007,
    ).export(ctx)

    ShapelessRecipe(
        [(id_filter, 1)],
        (id_filter, 1),
    ).export(ctx)
    ShapelessRecipe(
        [(hopper, 1), (silver_ingot, 1)],
        (id_filter, 1),
    ).export(ctx)

