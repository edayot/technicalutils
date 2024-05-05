
from beet import Context
from .types import NAMESPACE, Lang
from .mineral import Mineral, DEFAULT_ITEMS_DEFINITION



def beet_default(ctx: Context):
    Mineral(
        id="silver",
        name=(
            f"{NAMESPACE}.mineral.silver",
            {Lang.en_us: "Silver", Lang.fr_fr: "Argent"},
        ),
        custom_model_data=1430000,
        items_definiton=DEFAULT_ITEMS_DEFINITION,
    )
    Mineral(
        id="tin",
        name=(f"{NAMESPACE}.mineral.tin", {Lang.en_us: "Tin", Lang.fr_fr: "Étain"}),
        custom_model_data=1430020,
        items_definiton=DEFAULT_ITEMS_DEFINITION,
    )

