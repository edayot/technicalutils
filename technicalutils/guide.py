from .item import Registry, Item
from .crafting import VanillaRegistry, VanillaItem, ShapedRecipeRegistry
from beet import Context, Texture, Font, ItemModifier, LootTable
from model_resolver import beet_default as model_resolver
from PIL import Image, ImageDraw, ImageFont
from .utils import NAMESPACE
import json




def beet_default(ctx: Context):
    air = VanillaItem("minecraft:air")
    items = Registry.values()
    vanilla_items = VanillaRegistry.values()
    # Render the registry
    filter : list[str] = [r.model_path for r in items] + [r.model_path for r in vanilla_items]
    all_items : list[VanillaItem | Item] = list(items) + list(vanilla_items)
    ctx.meta["model_resolver"]["filter"] = filter
    model_resolver(ctx)
    for item in all_items:
        model_path = item.model_path
        path = f"technicalutils:render/{model_path.replace(':', '/')}"
        if not path in ctx.assets.textures:
            img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        else:
            img : Image.Image = ctx.assets.textures[path].image
        img = img.copy()
        img.putpixel((0,0),(137,137,137,255))
        img.putpixel((img.width-1,img.height-1),(137,137,137,255))
        ctx.assets.textures[path] = Texture(img.copy())
        if craft := ShapedRecipeRegistry.get(item):
            if (count := craft.result[1]) == 1:
                continue
            path_count = f"{path}_{count}"
            img_overlay = image_count(count)
            # draw img_overlay over img
            img = img.copy()
            img.paste(img_overlay, (0,0), img_overlay)
            ctx.assets.textures[path_count] = Texture(img.copy())

            assert len(item._count_to_char_index) < CHAR_OFFSET - 3
            item._count_to_char_index[count] = (len(item._count_to_char_index) + 1, path_count)

    create_font(ctx, all_items)

    pages = []
    page_index = 0
    for item in items:
        if not (craft := ShapedRecipeRegistry.get(item)):
            continue
        item.page_index = page_index
        page_index += 1
        pages.append(generate_craft(
            craft.items,
            craft.result[0],
            craft.result[1]
        ))
    create_loot_table(ctx, pages)





CHAR_INDEX_NUMBER = 0x0030
CHAR_OFFSET = 0x10
def char_index_number():
    global CHAR_INDEX_NUMBER
    CHAR_INDEX_NUMBER += CHAR_OFFSET
    return CHAR_INDEX_NUMBER


def create_font(ctx: Context, ITEMS: list[VanillaItem | Item]):
    font_path = f"{NAMESPACE}:pages"
    ctx.assets.fonts[font_path] = Font({
        "providers": [
        {
            "type": "reference",
            "id": "minecraft:include/space"
        },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/none_2_release.png",				"ascent": 7, "height": 8, "chars": ["\uef00"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/none_3_release.png",				"ascent": 7, "height": 8, "chars": ["\uef01"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/none_4_release.png",				"ascent": 7, "height": 8, "chars": ["\uef02"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/none_5_release.png",				"ascent": 7, "height": 8, "chars": ["\uef03"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/template_craft.png",				"ascent": -3, "height": 68, "chars": ["\uef13"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/font/template_result.png",				"ascent": -20, "height": 34, "chars": ["\uef14"] },

        # { "type": "bitmap", "file": f"{NAMESPACE}:item/font/technicalutils.png",				        "ascent": 7, "height": 64, "chars": ["\uee00"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/logo/github.png",				        "ascent": 7, "height": 25, "chars": ["\uee01"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/logo/pmc.png",				            "ascent": 7, "height": 25, "chars": ["\uee02"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/logo/smithed.png",				        "ascent": 7, "height": 25, "chars": ["\uee03"] },
        { "type": "bitmap", "file": f"{NAMESPACE}:item/logo/modrinth.png",				        "ascent": 7, "height": 25, "chars": ["\uee04"] },
        ],
    })
    for item in ITEMS:
        if not item.char_index:
            item.char_index = char_index_number()
        render = f"{NAMESPACE}:render/{item.model_path.replace(':','/')}"
        for i in range(3):
            char_item = f"\\u{item.char_index+i:04x}".encode().decode("unicode_escape")
            ctx.assets.fonts[font_path].data["providers"].append(
                {
                    "type": "bitmap",
                    "file": f"{render}.png",
                    "ascent": {0: 8, 1: 7, 2: 6}.get(i),
                    "height": 16,
                    "chars": [char_item]
                }
            )

        for count, (index, path) in item._count_to_char_index.items():
            char_item = f"\\u{item.count_to_char_index(count):04x}".encode().decode("unicode_escape")
            ctx.assets.fonts[font_path].data["providers"].append(
                {
                    "type": "bitmap",
                    "file": f"{path}.png",
                    "ascent": 7,
                    "height": 16,
                    "chars": [char_item]
                }
            )





def get_item_json(item: Item | VanillaItem, font_path: str, char : str = "\uef01"):
    if item.minimal_representation.get("id") == "minecraft:air":
        return {
            "text":char,
            "font":font_path,
            "color":"white"
        }
    if item.page_index == -1:
        return {
            "text":char,
            "font":font_path,
            "color":"white",
            "hoverEvent":{"action":"show_item","contents": item.minimal_representation}
        }
    return {
        "text":char,
        "font":font_path,
        "color":"white",
        "hoverEvent":{"action":"show_item","contents": item.minimal_representation},
        "clickEvent":{"action":"change_page","value":f"{item.page_index}"}
    }

def generate_craft(craft: list[list[Item| VanillaItem]], result: Item, count: int):
    if len(craft) != 3:
        craft.append([None, None, None])
    # Create a font for the page
    font_path = f'{NAMESPACE}:pages'
    page = [""]
    page.append({
        "text":f"\n\uef13 \uef14\n",
        "font":font_path,
        "color":"white"
    })
    page.append("\n")
    for i in range(3):
        for e in range(2):
            page.append({"text":"\uef00\uef00","font":font_path,"color":"white"})
            for j in range(3):
                item = craft[i][j]
                if item is None:
                    item = VanillaRegistry.get("minecraft:air")
                    craft[i][j] = item
                char_item = f"\\u{item.char_index + i:04x}".encode().decode("unicode_escape")
                page.append(get_item_json(item, font_path, f'\uef03{char_item}\uef03' if e == 0 else "\uef01"))
            if (i == 0 and e == 1) or (i == 1 and e == 1) or (i == 2 and e == 0):
                page.append({"text":"\uef00\uef00\uef00\uef00","font":font_path,"color":"white"})
                page.append(get_item_json(result, font_path, "\uef02\uef02"))
            if i == 1 and e == 0:
                page.append({"text":"\uef00\uef00\uef00\uef00","font":font_path,"color":"white"})
                if count == 1:
                    char_result = f"\\u{result.char_index:04x}".encode().decode("unicode_escape")
                else:
                    char_result = f"\\u{result.count_to_char_index(count):04x}".encode().decode("unicode_escape")
                char_space = "\uef00\uef00\uef03"
                page.append(get_item_json(result, font_path, f'{char_space}{char_result}{char_space}\uef00'))
            page.append("\n")
    return json.dumps(page)


def image_count(count: int) -> Image:
	""" Generate an image showing the result count
	Args:
		count (int): The count to show
	Returns:
		Image: The image with the count
	"""
	# Create the image
	size = 256
	img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	font_size = 64
	font = ImageFont.truetype(f"./assets/minecraft_font.ttf", size = font_size)

	# Calculate text size and positions of the two texts
	text_width = draw.textlength(str(count), font = font)
	text_height = font_size + 6
	pos_1 = (size-text_width), (size-text_height)
	pos_2 = (pos_1[0]-2, pos_1[1]-2)
	
	# Draw the count
	draw.text(pos_1, str(count), (50, 50, 50), font = font)
	draw.text(pos_2, str(count), (255, 255, 255), font = font)
	return img



def create_loot_table(ctx: Context, pages: list[str]):
    item_modifier_path = f"{NAMESPACE}:impl/guide_modifier"
    loot_table = {
        "pools": [
            {
                "rolls": 1,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": "minecraft:written_book",
                        "functions": [
                            {
                                "function": "minecraft:reference",
                                "name": item_modifier_path
                            }
                        ]
                    }
                ]
            }
        ]
    }
    item_modifier = [
        {
            "function": "minecraft:set_components",
            "components": {
                "minecraft:written_book_content": {
                    "title": "Guide",
                    "author": "AirDox_",
                    "pages": pages,
                    "resolved": True
                },
                "minecraft:custom_model_data": 1431000,
                "minecraft:custom_data": {
                    "ctc": {
                        "id": "guide",
                        "from": f"airdox_:{NAMESPACE}",
                    },
                    "smithed": {
                        "id": f"airdox_:{NAMESPACE}/guide",
                    }
                },
                "minecraft:item_name": json.dumps({"translate":f"{NAMESPACE}.guide","color":"white"}),
                "minecraft:enchantment_glint_override": False,
                "minecraft:lore": [
                    f"{{\"translate\":\"{NAMESPACE}.name\",\"color\":\"blue\",\"italic\":true}}"
                ]
            }
        }
    ]

    ctx.data.item_modifiers[item_modifier_path] = ItemModifier(item_modifier)

    loot_table_path = f"{NAMESPACE}:impl/items/guide"
    ctx.data.loot_tables[loot_table_path] = LootTable(loot_table)
    