from dataclasses import dataclass
from nbtlib import serialize_tag
from nbtlib.tag import (
    String,
    List,
    Compound,
    IntArray,
    Int,
    Byte,
    Short,
    Long,
    Float,
    Double,
)
from typing import Any
from beet import Context, Function, FunctionTag
from .item import Item
from .types import NAMESPACE


@dataclass
class VanillaItem:
    id: str

    def to_nbt(self, i: int):
        return Compound({"id": String(self.id), "Slot": Byte(i)})

    def result_command(self, count: int) -> str:
        return f"item replace block ~ ~ ~ container.16 with {self.id} {count} "


@dataclass
class ShapedRecipe:
    items: list[list[Item | VanillaItem | None]] 
    result: tuple[Item | VanillaItem, int]

    def export(self, ctx: Context):
        """
        This function export the smithed crafter recipes to the ctx variable.
        """
        air = lambda i: Compound({"id": String("minecraft:air"), "Slot": Byte(i)})

        smithed_recipe = {}
        for i, item_row in enumerate(self.items):
            row_check_list = [
                x.to_nbt(i) if x is not None else air(i) for i, x in enumerate(item_row)
            ]
            smithed_recipe[String(i)] = List[Compound](row_check_list)

        if_data_storage = f"if data storage smithed.crafter:input recipe{serialize_tag(Compound(smithed_recipe))}"

        if len(self.items) < 3:
            for i in range(len(self.items), 3):
                if_data_storage += f"\n\tif data storage smithed.crafter:input {{{i}:[]}}"


        function_path = f"{NAMESPACE}:impl/smithed.crafter/recipes"
        command = f"""
execute 
    store result score @s smithed.data 
    if entity @s[scores={{smithed.data=0}}] 
    {if_data_storage}
    run {self.result[0].result_command(self.result[1])}
"""
        tag_smithed_crafter_recipes = "smithed.crafter:event/recipes"
        if not tag_smithed_crafter_recipes in ctx.data.function_tags:
            ctx.data.function_tags[tag_smithed_crafter_recipes] = FunctionTag()
        if function_path not in ctx.data.functions:
            ctx.data.functions[function_path] = Function("# @public\n\n")
            ctx.data.functions[function_path].append("data modify storage test test set from storage smithed.crafter:input")
            ctx.data.function_tags[tag_smithed_crafter_recipes].data["values"].append(f"#{NAMESPACE}:calls/smithed.crafter/recipes")

        ctx.data.functions[function_path].append(command)






@dataclass
class ShapelessRecipe:
    items: list[tuple[Item | VanillaItem, int]]
    result: tuple[Item | VanillaItem, int]

    def export(self, ctx: Context):
        """
        This function export the smithed crafter recipes to the ctx variable.
        """
        count = len(self.items)

        recipe = List[Compound]([])
        for i, (item, count) in enumerate(self.items):
            nbt = item.to_nbt(i)
            nbt["count"] = Int(count)
            del nbt["Slot"]
            recipe.append(nbt)

        result_command = self.result[0].result_command(self.result[1])


        command = f"""
execute 
    store result score @s smithed.data 
    if entity @s[scores={{smithed.data=0}}] 
    if score count smithed.data matches {count} 
    if data storage smithed.crafter:input {{recipe:{serialize_tag(recipe)}}}
    run {result_command}
"""
        function_path = f"{NAMESPACE}:impl/smithed.crafter/shapeless_recipes"
        tag_smithed_crafter_shapeless_recipes = "smithed.crafter:event/shapeless_recipes"
        if not tag_smithed_crafter_shapeless_recipes in ctx.data.function_tags:
            ctx.data.function_tags[tag_smithed_crafter_shapeless_recipes] = FunctionTag()
        if function_path not in ctx.data.functions:
            ctx.data.functions[function_path] = Function("# @public\n\n")
            ctx.data.functions[function_path].append("data modify storage test test set from storage smithed.crafter:input")
            ctx.data.function_tags[tag_smithed_crafter_shapeless_recipes].data["values"].append(f"#{NAMESPACE}:calls/smithed.crafter/shapeless_recipes")
        
        ctx.data.functions[function_path].append(command)

        
