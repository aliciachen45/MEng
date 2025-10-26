from kesar import *
from constants import *
import random

# import visual
# import os


def chest_(
    prize_info={},
    prize=None,
    position="left",
    onclick_fn="selectChest",
):
    # Get the chest object
    items = [
        img_(
            id=f"chest_top_image_{position}",
            class_=f"chest_top_image",
            src="images/chest_top.png",
            alt="A treasure chest top",
            style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_TOP_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if position == 'left' else RIGHT_CHEST_POSITION_X};",
        ),
        img_(
            id=f"chest_bottom_image_{position}",
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
        )

        prize_left = (
            prize_info["left_x"]
            if position == "left"
            else prize_info["right_x"]
        )

        prize_top = prize_info["y"]
        items.append(
            prize(
                id=f"prize_image_{position}",
                width=prize_width,
                left=prize_left,
                top=prize_top,
            )
        )

        # add the sound effect
    else:
        pass
        # add the sound effect

    return div_(
        id=f"chest_container_{position}",
        style=f"display: flex; justify-content: flex-start; cursor: pointer;",
        onClick=f"{onclick_fn}(this);",
        # onClick=f"openChest('chest_top_image_{position}', '{prize_id}');",
    )(*items)


def coin_(id, width=1, left=0, top=0, additional_style="", additional_class=""):
    """
    Generate base HTML for a coin
    """
    return img_(
        id=id,
        class_=f"prize {additional_class}",
        src="images/coin.png",
        alt="Coin",
        style=f"width: {width}; top: {top}; left: {left}; {additional_style}",
    )


def chest_with_hook_(position="left"):
    """
    Generate base HTML for a chest with hook
    """
    # Get chest object
    chest = chest_(position=position)

    # Get hook object
    hook = img_(
        id=f"hook_chest_{position}",
        class_=f"hook hidden",
        src="images/hook.png",
        alt="Chest Hook",
        style=f"width: {DEFAULT_HOOK_WIDTH}; height: {DEFAULT_HOOK_HEIGHT}; top: {CHEST_HOOK_POSITION_Y}; left: {LEFT_HOOK_POSITION_X if position == 'left' else RIGHT_HOOK_POSITION_X};",
    )

    return div_(id=f"chest_with_hook_container_{position}")(chest, hook)


def prize_with_hook_(prize_info, prize, position="left"):
    """
    Generate base HTML for a coin with hook
    """
    # Get prize object
    prize_left = (
        prize_info["left_x"] if position == "left" else prize_info["right_x"]
    )

    prize_top = prize_info["y"]
    coin = prize(
        id=f"hooked_prize",
        width=prize_info["width"],
        left=prize_left,
        top=prize_top,
        additional_style="z-index: 4;",
        additional_class="hidden",
    )

    # Calculate hook positions based on prize position and dimensions
    hook_y = f"calc({prize_top} - {DEFAULT_HOOK_HEIGHT} + 2vh)"

    if position == "left":
        hook_x = (
            f"calc({prize_left} + {prize_info['width']} - {DEFAULT_HOOK_WIDTH})"
        )
    else:
        hook_x = prize_left

    # Get hook object
    hook = img_(
        id=f"hook_prize_{position}",
        class_=f"hook hook_{position} hidden",
        src="images/hook.png",
        alt="Chest Hook",
        style=f"width: {DEFAULT_HOOK_WIDTH}; height: {DEFAULT_HOOK_HEIGHT}; top: {hook_y}; left: {hook_x};",
    )

    return div_(id=f"prize_with_hook_container")(coin, hook)


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

    def get_stage1(self):

        pages = []

        # page 1
        items = []
        items.append(chest_(position="left"))
        items.append(chest_(position="right"))

        coin_side = random.choice(["left", "right"])
        coin = img_(
            id="stage_1_coin",
            class_="prize coin_stage_1 hidden",
            src="images/coin.png",
            alt="Coin",
            style=f"top: {COIN_POSITION_Y}; left: {LEFT_COIN_POSITION_X if coin_side == 'left' else RIGHT_COIN_POSITION_X};",
        )

        items.append(coin)

        # add occluder:
        flag_left = img_(
            id="initial_occluder",
            class_="occluder hidden",
            src="images/pirate_flag.png",
            alt="Flag",
            style=f"width: {DEFAULT_FLAG_WIDTH}; height: {DEFAULT_FLAG_HEIGHT}; position: absolute; left: {LEFT_FLAG_POSITION_X}; top: {FLAG_POSITION_Y};",
        )

        flag_right = img_(
            id="initial_occluder",
            class_="occluder hidden",
            src="images/pirate_flag.png",
            alt="Flag",
            style=f"width: {DEFAULT_FLAG_WIDTH}; height: {DEFAULT_FLAG_HEIGHT}; position: absolute; left: {RIGHT_FLAG_POSITION_X}; top: {FLAG_POSITION_Y};",
        )

        items.extend([flag_left, flag_right])
        items.append(div_(id="stage_indicator")(1))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        # page 2: ask for choice

        items = []

        if coin_side == "left":
            chest_left = chest_(
                prize_info=COIN_INFO,
                prize=coin_,
                position="left",
            )
            chest_right = chest_(position="right")
        else:
            chest_left = chest_(position="left")
            chest_right = chest_(
                prize_info=COIN_INFO,
                prize=coin_,
                position="right",
            )

        self.chest_left = chest_left
        self.chest_right = chest_right

        items.extend([chest_left, chest_right])

        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="chest_clicked",  # name for the server log
        )
        items.append(hidden_input)

        choice_page = div_(style="display: flex;")(*items)

        pages.append(choice_page)

        return pages

    def get_stage2(self, keep_side):
        print("Generating stage 2 pages for chosen side:", keep_side)

        replace_side = "right" if keep_side == "left" else "left"

        pages = []
        items = [
            self.chest_left if keep_side == "left" else self.chest_right,
            prize_with_hook_(
                prize_info=COIN_INFO, prize=coin_, position=replace_side
            ),
            chest_with_hook_(position=replace_side),
        ]

        items.append(div_(id="stage_indicator")(2))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        return pages


@kesar
def experiment(uid):
    data = {}
    animals = ["cat", "dog", "beaver"]

    # trial_pages = [coin]

    for animal in animals:
        print(animal)
        trial = OccludedTrial()

        all_pages = trial.get_stage1().copy()  # Get all pages for stage 1
        i = 0

        while i < len(all_pages):
            print("Displaying page", i + 1, "of", len(all_pages))
            response = yield all_pages[i]

            print("Recieved_response:", response)

            if "chest_clicked" in response:
                chosen_side = response["chest_clicked"]
                print("Chosen side:", chosen_side)

                # After choice, add stage 2 pages
                stage2_pages = trial.get_stage2(keep_side=chosen_side[0])
                all_pages.extend(stage2_pages)

                data[i] = response
            i += 1

        # for i, page in enumerate(trial.get_stage1()):  # Inject the coin HTML
        #     response = yield page
        #     if response["chest_clicked"] == "left":

        #     data[i] = response

        # yield div_(style="display: flex;")(
        #     chest_with_hook_(position="right"),
        #     chest_with_hook_(position="left"),
        # )

        # trial = Trial()
        # test = svg_(
        #     width="400",
        #     height="400",
        #     viewBox="0 0 400 400",
        #     style="position: absolute; top: 0; left: 0;",
        # )(
        #     path_(
        #         id="spiralPath",
        #         fill="none",
        #         d="M 200 200 L 200 10 C 200 10 390 10 390 200 C 390 390 10 390 10 200 C 10 10 380 10 380 200 C 380 380 20 380 20 200 C 20 20 370 20 370 200 C 370 370 30 370 30 200 C 30 30 360 30 360 200",
        #     )
        # )

        # dot = div_(id="dot")()
        # # yield dot
        # yield div_()(test, dot, gsap_lib)

        # yield chest_()
        # yield visual.get_full_chest_()
        # print("asdf d", animal)
        # text_input_("rating", f"Do you have a pet {animal}? (y/n)"),
        # submit_(),

        # data[animal] = response["rating"]
    return data  # to be logged
