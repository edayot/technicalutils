from dataclasses import dataclass, field
from .types import TextComponent, TextComponent_base, NAMESPACE
from beet import Context, FunctionTag, Function, LootTable
from typing import Any
from .utils import export_translated_string


Registry: dict[str, "Item"] = {}


@dataclass
class BlockProperties:
    base_block: str


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
        return {"smithed": {"id": f"{NAMESPACE}:{self.id}"}}

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
                internal_function_id
            )

        if internal_function_id not in ctx.data.functions:
            ctx.data.functions[internal_function_id] = Function()

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
"""
        )

    def set_components(self):
        res = []
        for key, value in self.components_extra.items():
            res.append(
                {"function": "minecraft:set_component", "components": {key: value}}
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

    def export(self, ctx: Context):
        assert self.id not in Registry, f"Item {self.id} already exists"
        Registry[self.id] = self
        self.create_loot_table(ctx)
        self.create_translation(ctx)
        self.create_custom_block(ctx)
