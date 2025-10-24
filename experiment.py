from kesar import *
from constants import *

# import visual
# import os


def chest_(
    id,
    prize_info={},
    prize=None,
    occluder_info={},
    occluder=None,
    width=DEFAULT_CHEST_WIDTH,
    top=25,
    position="left",
):
    """
    Generate HTML for a treasure chest with an optional prize.
    """
    # chest_width = width  # vw
    # chest_top_top = top  # vh
    # chest_bottom_top = (
    #     chest_top_top + CHEST_TOP_HEIGHT / CHEST_TOP_WIDTH * chest_width
    # )

    chest_width = DEFAULT_CHEST_WIDTH  # vw
    chest_top_top = f"{CHEST_TOP_POSITION_Y}vh"  # vh
    # chest_bottom_top = (
    #     f"{chest_top_top}vh + {DEFAULT_CHEST_TOP_HEIGHT}vw * 1vh/1vw"
    # )
    chest_bottom_top = (
        f"calc({CHEST_TOP_POSITION_Y}vh + {DEFAULT_CHEST_TOP_HEIGHT}vw)"
    )
    # chest_bottom_top = CHEST_BOTTOM_POSITION_Y  # vw

    # print(
    #     "vals",
    #     DEFAULT_CHEST_WIDTH,
    #     DEFAULT_CHEST_TOP_HEIGHT,
    #     CHEST_BOTTOM_POSITION_Y,
    #     CHEST_TOP_POSITION_Y,
    # )

    items = [
        img_(
            id=f"chest_top_image_{id}",
            class_=f"chest_top_image",
            src="images/chest_top.png",
            alt="A treasure chest top",
            style=f"width: {chest_width}vw; top: {chest_top_top}; left: {LEFT_CHEST_POSITION_X if position == 'left' else RIGHT_CHEST_POSITION_X}vw;",
        ),
        img_(
            id=f"chest_bottom_image_{id}",
            class_=f"chest_bottom_image",
            src="images/chest_bottom.png",
            alt="A treasure chest bottom",
            style=f"width: {chest_width}vw; top: {chest_bottom_top}; left: {LEFT_CHEST_POSITION_X if position == 'left' else RIGHT_CHEST_POSITION_X}vw;",
        ),
    ]

    # Adds a prize if there is a prize for this chest
    if prize_info:

        # prize_width, prize_height = chest_width / 4, chest_width / 4  # vw
        prize_width, prize_height = (
            prize_info["width"],
            prize_info["height"],
        )  # vw

        prize_left = (
            25 - prize_width / 2 if position == "left" else 75 - prize_width / 2
        )  # vw
        prize_top = f"calc({chest_bottom_top} - {prize_height/2}vw)"
        items.append(
            prize(
                id=f"prize_image_{id}",
                width=prize_width,
                left=prize_left,
                top=prize_top,
            )
        )

        # add the sound effect
    else:
        pass
        # add the sound effect

    # Adds an occluder if there is an occlude for this chest
    # if occluder_info:
    #     occluder_width, occluder_height = (
    #         chest_width * 1.5,
    #         chest_width * 1.5,
    #     )  # vw
    #     occluder_left = (10 if position == "left" else 60) + (
    #         chest_width - occluder_width
    #     ) / 2
    #     occluder_top = chest_top_top - (occluder_height) / 2
    #     items.append(
    #         occluder(
    #             id=f"occluder_image_{id}",
    #             width=occluder_width,
    #             left=occluder_left,
    #             top=occluder_top,
    #         )
    #     )

    prize_id = f"prize_image_{id}" if prize_info else ""
    occluder_id = f"occluder_image_{id}" if occluder_info else ""
    return div_(
        id=f"chest_container_{id}",
        style=f"display: flex; justify-content: flex-start; cursor: pointer; transform-origin: center;",
        onClick=f"openChest('chest_top_image_{id}', '{prize_id}', '{occluder_id}');",
        # onClick=f"swipeRight(this);",
        # onClick=f"select(this);",
    )(*items)


def coin_(id, width=1, left=0, top=0):
    """
    Generate base HTML for a coin
    """
    return img_(
        id=id,
        class_="prize",
        src="images/coin.png",
        alt="Coin",
        style=f"width: {width}vw; position: absolute; top: {top}; left: {left}vw;",
    )


def flag_(id, hidden=False, width=1, left=0, top=0):
    """
    Generate base HTML for a flag
    """
    classes = "occluder"
    if hidden:
        classes += " hidden"
    return img_(
        id=id,
        class_=classes,
        src="images/pirate_flag.png",
        alt="Flag",
        width=f"{width}px",
        style=f"position: absolute; top: {top}px; left: {left}px;",
        onClick="select(this);",
    )


"""
Trials:
Training types: 2 chest,





"""


class Trial:
    def __init__(self, name=""):
        self.name = name
        self.additional_choice = False

    def get_html(self):
        # figure out how to make it dynamic with page size

        # page 1: show chests: two chests
        # - open both (empty)
        # - put coin in one chest
        # - close both chest

        # page 1
        items = []
        items.append(chest_(id="left", position="left"))
        items.append(chest_(id="right", position="right"))
        coin = img_(
            id="initial_coin_to_either",
            class_="prize initial_coin",
            src="images/coin.png",
            alt="Coin",
            # style=f"",
        )
        items.append(coin)
        yield div_(style="display: flex;")(*items)

        # page 2: ask for choice
        items = []
        chest1 = chest_(
            id="1",
            prize_info=COIN_INFO,
            prize=coin_,
            position="right",
        )
        chest2 = chest_(
            id="2",
        )

        # coin = coin_(
        #     id="initial_coin",
        #     width=DEFAULT_CHEST_WIDTH / 4,
        #     left=50 - DEFAULT_CHEST_WIDTH / 8,
        #     top=10,
        # )
        # coin = img_(
        #     id="coin",
        #     class_="prize",
        #     src="images/coin.png",
        #     alt="Coin",
        #     style=f"width: {DEFAULT_CHEST_WIDTH/4}vw; position: absolute; top: {10}vh; left: {50-DEFAULT_CHEST_WIDTH/8}vw;",
        # )
        items.extend([chest1, chest2])

        # flag1 = flag_(id="flag1", hidden=False, width=100, left=400, top=200)

        yield div_(style="display: flex;")(*items)
        # return flag1

        # return div_(style="display: flex; margin: 0; width: 100%;")(
        #     chest1,
        #     chest2,
        # )


@kesar
def experiment(uid):
    data = {}
    animals = ["cat", "dog", "beaver"]

    # trial_pages = [coin]

    for animal in animals:
        print(animal)
        trial = Trial()

        for page in trial.get_html():  # Inject the coin HTML
            print(page)
            response = yield page
            print(response)
        # yield chest_()
        # yield visual.get_full_chest_()
        print("asdf d", animal)
        # text_inpu t_("rating", f"Do you have a pet {animal}? (y/n)"),
        # submit_(),

        # data[animal] = response["rating"]
    return data  # to be logged
