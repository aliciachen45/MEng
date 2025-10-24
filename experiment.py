from kesar import *
from constants import *

# import visual
# import os


def chest_(
    id,
    prize_info={},
    prize=None,
    position="left",
):
    items = [
        img_(
            id=f"chest_top_image_{id}",
            class_=f"chest_top_image",
            src="images/chest_top.png",
            alt="A treasure chest top",
            style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_TOP_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if position == 'left' else RIGHT_CHEST_POSITION_X};",
        ),
        img_(
            id=f"chest_bottom_image_{id}",
            class_=f"chest_bottom_image",
            src="images/chest_bottom.png",
            alt="A treasure chest bottom",
            style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_BOTTOM_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if position == 'left' else RIGHT_CHEST_POSITION_X};",
        ),
    ]

    # Adds a prize if there is a prize for this chest
    if prize_info:

        prize_width, prize_height = (
            prize_info["width"],
            prize_info["height"],
        )  # vw

        prize_left = (
            LEFT_COIN_POSITION_X
            if position == "left"
            else RIGHT_COIN_POSITION_X
        )

        prize_top = COIN_POSITION_Y
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
    return div_(
        id=f"chest_container_{id}",
        style=f"display: flex; justify-content: flex-start; cursor: pointer; transform-origin: center;",
        onClick=f"openChest('chest_top_image_{id}', '{prize_id}');",
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
        style=f"width: {width}; position: absolute; top: {top}; left: {left};",
    )


# def flag_(id, hidden=False, width=1, left=0, top=0):
#     """
#     Generate base HTML for a flag
#     """
#     classes = "occluder"
#     if hidden:
#         classes += " hidden"
#     return img_(
#         id=id,
#         class_=classes,
#         src="images/pirate_flag.png",
#         alt="Flag",
#         width=f"{width}px",
#         style=f"position: absolute; top: {top}px; left: {left}px;",
#         onClick="select(this);",
#     )


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

        print(items)
        yield div_(style="display: flex;")(*items)
        # return flag1

        # return div_(style="display: flex; margin: 0; width: 100%;")(
        #     chest1,
        #     chest2,
        # )


class OccludedTrial(Trial):
    def __init__(self, name=""):
        super().__init__(name=name)

    def get_html(self):
        # page 1: show chests: two chests
        # - open both (empty)
        # - put coin in one chest
        # - close both chest

        # page 1
        items = []
        items.append(chest_(id="left", position="left"))
        items.append(chest_(id="right", position="right"))

        final_pos = "left"  # or "right"
        coin = img_(
            id="initial_coin_to_either",
            class_="prize coin_stage_1",
            src="images/coin.png",
            alt="Coin",
            style=f"top: {COIN_POSITION_Y}; left: {LEFT_COIN_POSITION_X};",
            # style=f"",
        )

        items.append(coin)

        # add occluder:
        flag_left = img_(
            id="initial_occluder",
            class_="occluder",
            src="images/pirate_flag.png",
            alt="Flag",
            style=f"width: {DEFAULT_FLAG_WIDTH}; height: {DEFAULT_FLAG_HEIGHT}; position: absolute; left: {LEFT_FLAG_POSITION_X}; top: {FLAG_POSITION_Y};",
        )

        flag_right = img_(
            id="initial_occluder",
            class_="occluder",
            src="images/pirate_flag.png",
            alt="Flag",
            style=f"width: {DEFAULT_FLAG_WIDTH}; height: {DEFAULT_FLAG_HEIGHT}; position: absolute; left: {RIGHT_FLAG_POSITION_X}; top: {FLAG_POSITION_Y};",
        )

        items.extend([flag_left, flag_right])
        print(items)
        yield div_(style="display: flex;")(*items)

        # # page 2: ask for choice
        # items = []
        # chest1 = chest_(
        #     id="1",
        #     prize_info=COIN_INFO,
        #     prize=coin_,
        #     position="right",
        #     occluder_info=FLAG_INFO,
        #     occluder=flag_,
        # )
        # chest2 = chest_(
        #     id="2",
        #     position="left",
        #     occluder_info=FLAG_INFO,
        #     occluder=flag_,
        # )

        # items.extend([chest1, chest2])

        # yield div_(style="display: flex;")(*items)


@kesar
def experiment(uid):
    data = {}
    animals = ["cat", "dog", "beaver"]

    # trial_pages = [coin]

    for animal in animals:
        print(animal)
        trial = OccludedTrial()
        # trial = Trial()

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
