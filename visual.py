from kesar import *


def get_full_chest_():
    print("alskdjf")
    return div_(
        id="full_chest_container",
        style="display: flex; flex-direction: column; cursor: pointer;",
    )(
        img_(
            id="chest_top_image",
            src="images/chest_top.png",
            alt="A treasure chest",
            width="200",
            style="margin-bottom: 0px",
        ),
        img_(
            id="chest_bottom_image",
            src="images/chest_bottom.png",
            alt="A treasure chest",
            width="200",
            style="margin-top: 0px",
        ),
    )


def get_full_chest_():
    # The container that all elements will be positioned relative to
    return div_(
        id="full_chest_container",
        style="display: flex; flex-direction: column; align-items: center; cursor: pointer;",
    )(
        # Coin sits behind the chest parts
        img_(
            id="coin_image",
            src="images/coin.png",
            alt="Coin",
        ),
        # Wrapper to stack the chest pieces visually
        # div_(
        #     id="chest_wrapper",
        #     style="display: flex; flex-direction: column; cursor: pointer;",
        # )(
        img_(
            id="chest_top_image",
            src="images/chest_top.png",
            alt="A treasure chest top",
            width="200",
        ),
        img_(
            id="chest_bottom_image",
            src="images/chest_bottom.png",
            alt="A treasure chest bottom",
            width="200",
        ),
        # ),
    )


# TODO: open chest
# TODO: animation for closed to open
def get_open_chest_():
    return div_(style="display: flex; flex-direction: column;")(
        img_(
            src="images/chest_top.png",
            alt="An open treasure chest",
            width="200",
            margin_bottom="50px",
        ),
        img_(
            src="images/chest_bottom.png",
            alt="An open treasure chest",
            width="200",
            margin_top="0px",
        ),
    )


css_block = style_()(static_("static/styles.css"))
js_block = script_()(static_("static/script.js"))


def swivel_coin_():
    return div_(id_="coin_container")(
        img_(
            id_="coin_image",
            src="images/coin.png",
            alt="Coin",
            onclick="startRotation()",
        ),  # <-- Reference the image path
    )
