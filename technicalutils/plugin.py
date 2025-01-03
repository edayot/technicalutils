from beet import Context
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.mineral import Mineral
from simple_item_plugin.item import Item, BlockProperties, WorldGenerationParams, ItemGroup
from simple_item_plugin.crafting import VanillaItem, ShapedRecipe, SimpledrawerMaterial, ShapelessRecipe, ExternalItem
from simple_item_plugin.utils import export_translated_string
import json

def beet_default(ctx: Context):
    # Registering Items
    guide = Item(
        id="guide",
        base_item="minecraft:written_book",
        item_name=(
            f"{NAMESPACE}.item.guide",
            {Lang.en_us: "Guide", Lang.fr_fr: "Guide"},
        ),
        components_extra={
            "minecraft:enchantment_glint_override": False,
            "special:item_modifier": f"{NAMESPACE}:impl/guide",
        },
        guide_description=(f"{NAMESPACE}.guide.description", {
            Lang.en_us: "The guide you are currently holding.",
            Lang.fr_fr: "Le guide que vous tenez actuellement."
        })
    ).export(ctx)

    smooth_stone = VanillaItem(id="minecraft:smooth_stone").export(ctx)
    oak_log = VanillaItem(id="minecraft:oak_log").export(ctx)
    crafting_table = VanillaItem(id="minecraft:crafting_table").export(ctx)

    heavy_workbench = ExternalItem(
        id="smithed:crafter",
        loot_table_path="smithed.crafter:blocks/table",
        item_model="smithed.crafter:table",
        minimal_representation={
            "id":"minecraft:furnace",
            "components": {
                "minecraft:item_name": json.dumps({"translate":"block.smithed.crafter"})
            }
        }, 
        guide_description=(f"{NAMESPACE}.guide.heavy_workbench", {
            Lang.fr_fr: "C'est une table de craft qui permet de crafter les items de Grappling Hook.",
            Lang.en_us: "It's a crafting table that allows you to craft Grappling Hook items."
        })
    ).export(ctx)
    ShapedRecipe(
        items=(
            (oak_log, oak_log, oak_log),
            (oak_log, crafting_table, oak_log),
            (smooth_stone, smooth_stone, smooth_stone),
        ),
        result=(heavy_workbench, 1),
    ).export(ctx, True)

    ItemGroup(
        id="tutorial",
        name=(
            f"{NAMESPACE}.item_group.tutorial",
            {Lang.en_us: "Tutorial", Lang.fr_fr: "Tutoriel"},
        ),
        item_icon=guide,
        items_list=[heavy_workbench, guide],
    ).export(ctx)

    Mineral(
        id="silver",
        name=(
            f"{NAMESPACE}.mineral.silver",
            {Lang.en_us: "Silver", Lang.fr_fr: "Argent"},
        ),
        overrides={
            "ore": {
                "block_properties": BlockProperties(
                    base_block="minecraft:lodestone",
                    world_generation=[
                        WorldGenerationParams(
                            min_y=10,
                            max_y=40,
                            min_veins=1,
                            max_veins=3,
                            min_vein_size=4,
                            max_vein_size=10,
                            ignore_restrictions=0
                        )
                    ]
                )
            },
            "deepslate_ore": {
                "block_properties": BlockProperties(
                    base_block="minecraft:lodestone",
                    world_generation=[
                        WorldGenerationParams(
                            min_y=-10,
                            max_y=5,
                            min_veins=1,
                            max_veins=2,
                            min_vein_size=4,
                            max_vein_size=5,
                            ignore_restrictions=0
                        )
                    ]
                )
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
                "armor": 3.25,
                "armor_toughness": 2,
                "max_damage": 200,
            },
            "chestplate": {
                "armor": 6.25,
                "armor_toughness": 1,
                "max_damage": 300,
            },
            "leggings": {
                "armor": 5.25,
                "armor_toughness": 2,
                "max_damage": 290,
            },
            "boots": {
                "armor": 2.25,
                "armor_toughness": 1,
                "max_damage": 250
            },
        },
        armor_additional_attributes={
            "minecraft:movement_speed": {
                "amount": -0.0015,
                "slot": "armor",
            }
        }
    ).export(ctx)
    item_cable = Item(
        id="item_cable",
        item_name=(
            f"{NAMESPACE}.item.item_cable",
            {Lang.en_us: "Item Cable", Lang.fr_fr: "Câble d'objet"},
        ),
        base_item="minecraft:conduit",
        block_properties=BlockProperties(
            base_block="minecraft:conduit",
            smart_waterlog=True,
            base_item_placed="minecraft:light_gray_stained_glass_pane",
            item_model_placed="technicalutils:item_cable_placed",
        )
    ).export(ctx)

    servo_extract = Item(
        id="servo_extract",
        item_name=(
            f"{NAMESPACE}.item.servo_extract",
            {Lang.en_us: "Servo Extract", Lang.fr_fr: "Servo Extracteur"},
        ),
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
        base_item="minecraft:item_frame",
        components_extra={
            "minecraft:entity_data": {
                "id": "minecraft:item_frame",
                "Tags": [f"{NAMESPACE}.servo.summoned", f"{NAMESPACE}.servo.insert"],
                "Invisible": 1,
            }
        }
    ).export(ctx)
    id_filter = Item(
        id="id_filter",
        item_name=(
            f"{NAMESPACE}.item.id_filter",
            {Lang.en_us: "ID Filter", Lang.fr_fr: "Filtre d'ID"},
        ),
    ).export(ctx)
    wrench = Item(
        id="wrench",
        item_name=(
            f"{NAMESPACE}.item.wrench",
            {Lang.en_us: "Wrench", Lang.fr_fr: "Clé à molette"},
        ),
    ).export(ctx)

    ItemGroup(
        id="networking",
        name=(
            f"{NAMESPACE}.item_group.networking",
            {Lang.en_us: "Networking", Lang.fr_fr: "Réseau"},
        ),
        item_icon=item_cable,
        items_list=[item_cable, servo_extract, servo_insert, id_filter, wrench],
    ).export(ctx)

    # Crafting Part

    silver_ingot = Item.get(ctx, "silver_ingot")
    assert silver_ingot is not None
    redstone = VanillaItem(id="minecraft:redstone").export(ctx)
    iron_ingot = VanillaItem(id="minecraft:iron_ingot").export(ctx)
    glass = VanillaItem(id="minecraft:glass").export(ctx)
    redstone_block = VanillaItem(id="minecraft:redstone_block").export(ctx)
    comparator = VanillaItem(id="minecraft:comparator").export(ctx)
    hopper = VanillaItem(id="minecraft:hopper").export(ctx)

    ShapedRecipe(
        items=(
            (iron_ingot, glass, iron_ingot),
            (silver_ingot, redstone, silver_ingot),
            (iron_ingot, glass, iron_ingot),
        ),
        result=(item_cable, 16)
    ).export(ctx)

    ShapedRecipe(
        items=(
            (None, redstone_block, None),
            (silver_ingot, comparator, silver_ingot),
            (None, None, None),
        ),
        result=(servo_extract, 1)
    ).export(ctx)
    ShapedRecipe(
        items=(
            (silver_ingot, comparator, silver_ingot),
            (None, redstone_block, None),
            (None, None, None),
        ),
        result=(servo_insert, 1)
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


    ShapedRecipe(
        items=(
            (None, iron_ingot, None),
            (None, silver_ingot, iron_ingot),
            (iron_ingot, None, None),
        ),
        result=(wrench, 1)
    ).export(ctx)


    ShapelessRecipe(
        [(id_filter, 1)],
        (id_filter, 1),
    ).export(ctx)
    ShapelessRecipe(
        [(hopper, 1), (silver_ingot, 1)],
        (id_filter, 1),
    ).export(ctx)
