from dataclasses import dataclass, field
from .types import TextComponent, TextComponent_base, NAMESPACE
from beet import Context, FunctionTag, Function, LootTable, Model
from typing import Any
from .utils import export_translated_string
from beet.contrib.vanilla import Vanilla

from nbtlib.tag import Compound, String, Byte
import json


Registry: dict[str, "Item"] = {}


@dataclass
class BlockProperties:
    base_block: str
    all_same_faces: bool = True


@dataclass
class Item:
    id: str
    # the translation key, the
    item_name: TextComponent
    lore: list[TextComponent_base] = field(default_factory=list)

    components_extra: dict[str, Any] = field(default_factory=dict)

    base_item: str = "minecraft:jigsay"
    custom_model_data: int = 1430000

    block_properties: BlockProperties = None
    is_cookable: bool = False

    def __post_init__(self):
        assert self.id not in Registry, f"Item {self.id} already exists"
        Registry[self.id] = self

    def result_command(self, count: int) -> str:    
        loot_table_name = f"{NAMESPACE}:items/{self.id}"
        if count == 1:
            return f"loot replace block ~ ~ ~ container.16 loot {loot_table_name}"
        loot_table_inline = {
            "pools": [
                {
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:loot_table",
                            "value": loot_table_name,
                            "functions": [
                                {
                                    "function": "minecraft:set_count",
                                    "count": count
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return f"loot replace block ~ ~ ~ container.16 loot {json.dumps(loot_table_inline)}"

    def to_nbt(self, i: int) -> Compound:
        # return the nbt tag of the item smithed id "SelectedItem.components."minecraft:custom_data".smithed.id"
        return Compound(
            {
                "components": Compound(
                    {
                        "minecraft:custom_data": Compound(
                            {"smithed": Compound({"id": String(f"{NAMESPACE}:{self.id}")})}
                        )
                    }
                ),
                "Slot": Byte(i), 
            }
        )

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
        res = {
            "smithed": {"id": f"{NAMESPACE}:{self.id}"},
        }
        if self.is_cookable:
            res["nbt_smelting"] = Byte(1)
        return res

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
                                    },
                                }
                            ],
                        }
                    ],
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
            ctx.data.function_tags[smithed_function_tag_id].data["values"].append(
                f"#{NAMESPACE}:calls/smithed.custom_block/on_place"
            )

        if internal_function_id not in ctx.data.functions:
            ctx.data.functions[internal_function_id] = Function("# @public\n\n")

        ctx.data.functions[internal_function_id].append(
            f"""
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
                data merge entity @s {{brightness:{{sky:10,block:15}}}}
"""
        )
        loot_table_name = f"{NAMESPACE}:items/{self.id}"
        destroy_function_id = f"{NAMESPACE}:impl/blocks/destroy/{self.id}"
        ctx.data.functions[destroy_function_id] = Function(f"""

execute
    as @e[type=item,nbt={{Item:{{id:"{self.block_properties.base_block}",count:1}}}},limit=1,sort=nearest,distance=..3]
    run function ~/spawn_item:
        loot spawn ~ ~ ~ loot {loot_table_name}
        kill @s

kill @s
""")
        all_same_function_id = f"{NAMESPACE}:impl/blocks/destroy_{self.block_properties.base_block.replace('minecraft:', '')}"
        if all_same_function_id not in ctx.data.functions:
            ctx.data.functions[all_same_function_id] = Function()
        ctx.data.functions[all_same_function_id].append(f"execute if entity @s[tag={NAMESPACE}.block.{self.block_properties.base_block.replace('minecraft:', '')}] run function {destroy_function_id}")

    def set_components(self):
        res = []
        for key, value in self.components_extra.items():
            res.append(
                {"function": "minecraft:set_components", "components": {key: value}}
            )
        return res

    def create_loot_table(self, ctx: Context):
        ctx.data.loot_tables[f"{NAMESPACE}:items/{self.id}"] = LootTable(
            {
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
                                        },
                                    },
                                    {
                                        "function": "minecraft:set_name",
                                        "entity": "this",
                                        "target": "item_name",
                                        "name": self.item_name,
                                    },
                                    {
                                        "function": "minecraft:set_lore",
                                        "entity": "this",
                                        "lore": self.create_lore(),
                                        "mode": "replace_all",
                                    },
                                    *self.set_components(),
                                    *self.create_block_placement_data(),
                                ],
                            }
                        ],
                    }
                ]
            }
        )

    def create_assets(self, ctx: Context):
        key = f"minecraft:item/{self.base_item.split(':')[1]}"
        if not key in ctx.assets.models:
            vanilla = ctx.inject(Vanilla).releases[ctx.meta["minecraft_version"]]
            # get the default model for this item
            ctx.assets.models[key] = vanilla.assets.models[key]
            ctx.assets.models[key].data["overrides"] = []
        
        # add the custom model data to the model
        ctx.assets.models[key].data["overrides"].append({
            "predicate": {
            "custom_model_data": self.custom_model_data
            },
            "model": (model_path := f"{NAMESPACE}:item/{self.id}")
        })
        # create the custom model
        if not self.block_properties:
            ctx.assets.models[model_path] = Model(
                {
                    "parent": "item/generated",
                    "textures": {
                        "layer0": model_path
                    }
                }
            )
        elif self.block_properties.all_same_faces:
            ctx.assets.models[model_path] = Model(
                {
                    "parent": "minecraft:block/cube_all",
                    "textures": {
                        "all": f"{NAMESPACE}:block/{self.id}"
                    }
                }
            )
        else:
            ctx.assets.models[model_path] = Model(
                {
                    "parent": "minecraft:block/orientable_with_bottom",
                    "textures": {
                        "top": f"{NAMESPACE}:block/{self.id}_top",
                        "side": f"{NAMESPACE}:block/{self.id}_side",
                        "bottom": f"{NAMESPACE}:block/{self.id}_bottom",
                        "front": f"{NAMESPACE}:block/{self.id}_front",
                    }
                }
            )
            

    def export(self, ctx: Context):
        self.create_loot_table(ctx)
        self.create_translation(ctx)
        self.create_custom_block(ctx)
        self.create_assets(ctx)
