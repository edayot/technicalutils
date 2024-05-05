
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
            "ore":None,
            "deepslate_ore":None,
            "block":None,
            "raw_ore_block":None,
            "ingot":None,
            "nugget":None,
            "raw_ore":None,
            "dust":None,
            "pickaxe": {
                "tier" : "iron",
                "speed" : 4.8,
                "max_damage" : 300,
                "attack_damage" : 4,
                "attack_speed" : -3,
            },
            'axe': {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 9,
                "attack_speed": -3,
            },
            'shovel': {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 2,
                "attack_speed": -3,
            },
            'hoe': {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 1,
                "attack_speed": -3,
            },
            'sword': {
                "tier": "iron",
                "speed": 4.8,
                "max_damage": 300,
                "attack_damage": 6,
                "attack_speed": -3,
            },
        }

    )


