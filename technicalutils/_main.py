from beet import Context
from .types import NAMESPACE, Lang
from .mineral import Mineral


def beet_default(ctx: Context):
    Mineral(
        id="silver",
        name=(
            f"{NAMESPACE}.mineral.silver",
            {Lang.en_us: "Silver", Lang.fr_fr: "Argent"},
        ),
        custom_model_data=1430000,
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
                        "max_y": 0,
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
                "attack_speed": -3,
            },
            "axe": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 9,
                "attack_speed": -3,
            },
            "shovel": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 2,
                "attack_speed": -3,
            },
            "hoe": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 1,
                "attack_speed": -3,
            },
            "sword": {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 6,
                "attack_speed": -3,
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
    )
