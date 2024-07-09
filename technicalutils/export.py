from .item import Registry, Item
from .crafting import VanillaRegistry, VanillaItem
from beet import Context, Texture, Font
from model_resolver import beet_default as model_resolver
from PIL import Image
from .utils import NAMESPACE


CHAR_INDEX_NUMBER = 0xff01
def char_index_number():
    global CHAR_INDEX_NUMBER
    CHAR_INDEX_NUMBER += 3
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



def beet_default(ctx: Context):
    """
    We need to export items in custom_model_data order
    """
    items = Registry.values()
    items = sorted(items, key=lambda x: x.custom_model_data)
    for item in items:
        item.export(ctx)

    # Render the registry
    filter = [r.model_path for r in items] + [r.model_path for r in VanillaRegistry.values()]
    all_items : list[VanillaItem | Item] = items + list(VanillaRegistry.values())
    ctx.meta["model_resolver"]["filter"] = filter
    model_resolver(ctx)
    for model_path in filter:
        path = f"technicalutils:render/{model_path.replace(':', '/')}"
        if not path in ctx.assets.textures:
            continue
        img : Image.Image = ctx.assets.textures[path].image
        img = img.copy()
        img.putpixel((0,0),(137,137,137,255))
        img.putpixel((img.width-1,img.height-1),(137,137,137,255))
        ctx.assets.textures[path] = Texture(img)

    create_font(ctx, all_items)
    