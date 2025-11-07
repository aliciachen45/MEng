from kesar import *
from constants import *
import random

# import visual
# import os


# def chest_(
#     prize=None,
#     side="left",
#     onclick_fn=None,
#     additional_style="",
#     clickable=False,
# ):
#     return Chest(
#         "chest",
#         side=side,
#         clickable=clickable,
#         prize=prize,
#         onclick_fn=onclick_fn,c
#     ).get_html(additional_style=additional_style)
# items = ChestShell(name="chest", side=side, clickable=clickable).get_html(
#     additional_style=additional_style
# )

# if prize:
#     prize_object = prize(name=f"prize_image_{side}", side=side)
#     items.extend(prize_object.get_html())

#     # add the sound effect
# else:
#     pass
#     # add the sound effect

# return div_(
#     id=f"chest_container_{side}",
#     style=f"display: flex; justify-content: flex-start;",
#     onClick=f"{onclick_fn}(this);" if onclick_fn else "",
# )(*items)


# def coin_(id, additional_style="", additional_class=""):
#     """
#     Generate base HTML for a coin
#     """

#     return Coin(name=id).get_html(
#         additional_style=additional_style, additional_class=additional_class
#     )


def chest_with_hook_(side="left"):
    """
    Generate base HTML for a chest with hook
    """
    # Get chest object
    print("Generating chest with hook for side:", side)
    chest = Chest(side=side).get_html()

    # Get hook object
    hook_x = LEFT_HOOK_POSITION_X if side == "left" else RIGHT_HOOK_POSITION_X
    hook = Hook(
        name=f"hook_chest_{side}",
        side=side,
        left=hook_x,
        top=CHEST_HOOK_POSITION_Y,
    ).get_html(additional_class="hidden")

    return div_(id=f"chest_with_hook_container_{side}")(chest, hook)


# def prize_with_hook_(prize, side="left"):
#     """
#     Generate base HTML for a coin with hook
#     """
#     # Get prize object

#     prize_object = prize(name="hooked_prize", side=side)
#     prize_html = prize_object.get_html(
#         additional_style="z-index: 4;", additional_class="hidden"
#     )

#     prize_top = prize_object.info["y"]
#     prize_left = (
#         prize_object.info["left_x"]
#         if side == "left"
#         else prize_object.info["right_x"]
#     )

#     # Calculate hook positions based on prize position and dimensions
#     hook_y = f"calc({prize_top} - {DEFAULT_HOOK_HEIGHT} + 2vh)"

#     if side == "left":
#         hook_x = f"calc({prize_left} + {prize_object.info['width']} - {DEFAULT_HOOK_WIDTH})"
#     else:
#         hook_x = prize_left

#     # Get hook object
#     hook = Hook(
#         name=f"hook_prize_{side}",
#         side=side,
#         left=hook_x,
#         top=hook_y,
#     ).get_html(additional_class="hidden")

#     return div_(id=f"prize_with_hook_container")(prize_html, hook)


class Object:
    def __init__(self, name="", clickable=False):
        self.name = name
        self.clickable = clickable
        self.clickfn_mutable = True

    def get_html(self):
        raise NotImplementedError("Subclasses must implement get_html method.")


class ChestShell(Object):
    def __init__(self, name="", side="left", clickable=False):
        super().__init__(name=name, clickable=clickable)
        self.side = side

    def get_html(self, additional_style=""):
        if self.clickable:
            additional_style += " cursor: pointer;"

        items = [
            img_(
                id=f"chest_top_image_{self.side}",
                class_=f"chest_top_image",
                src="images/chest_top.png",
                alt="A treasure chest top",
                style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_TOP_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if self.side == 'left' else RIGHT_CHEST_POSITION_X}; {additional_style}",
            ),
            img_(
                id=f"chest_bottom_image_{self.side}",
                class_=f"chest_bottom_image",
                src="images/chest_bottom.png",
                alt="A treasure chest bottom",
                style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_BOTTOM_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if self.side == 'left' else RIGHT_CHEST_POSITION_X}; {additional_style}",
            ),
        ]
        return items


class Chest(Object):
    def __init__(
        self,
        name="",
        side="left",
        clickable=False,
        prize_class=None,
        prize=None,
        onclick_fn=None,
    ):
        super().__init__(name=name, clickable=clickable)
        self.side = side
        self.onclick_fn = onclick_fn
        if not prize:
            if prize_class:
                self.prize = prize_class(
                    name=f"prize_image_{self.side}", side=self.side
                )
            else:
                self.prize = None
        else:
            self.prize = prize

    def get_html(self, additional_style=""):
        items = ChestShell(
            name=self.name, side=self.side, clickable=self.clickable
        ).get_html(additional_style=additional_style)

        if self.prize:
            items.append(self.prize.get_html(additional_style=additional_style))

            # add the sound effect
        else:
            pass
            # add the sound effect

        return div_(
            id=f"chest_container_{self.side}",
            style=f"display: flex; justify-content: flex-start;",
            onClick=f"{self.onclick_fn}(this);" if self.clickable else "",
        )(*items)


class Prize(Object):
    def __init__(self, name=""):
        super().__init__(name=name)
        self.clickfn_mutable = False


class Coin(Object):
    def __init__(self, name="", side="left", clickable=False, x=None, y=None):
        super().__init__(name=name)
        self.info = COIN_INFO
        self.side = side
        self.clickable = clickable
        self.onclick_fn = "revealCoin"
        self.width = self.info["width"]
        if x:
            self.x = x
        else:
            self.x = (
                self.info["left_x"]
                if self.side == "left"
                else self.info["right_x"]
            )

        if y:
            self.y = y
        else:
            self.y = self.info["y"]

    def get_html(self, additional_style="", additional_class=""):
        return img_(
            id=self.name,
            class_=f"prize {additional_class}",
            src="images/coin.png",
            alt="Coin",
            onClick=f"{self.onclick_fn}(this);" if self.clickable else "",
            style=f"width: {self.width}; top: {self.y}; left: {self.x}; {additional_style}; {'cursor: pointer;' if self.clickable else ''}",
        )


class Bag(Prize):
    def __init__(self, name="", side="left", open=True, clickable=False):
        super().__init__(name=name)
        self.side = side
        self.open = open
        self.clickable = clickable
        self.onclick_fn = "revealCoinsFromBag"
        self.info = BAG_INFO
        self.x = (
            LEFT_BAG_POSITION_X if self.side == "left" else RIGHT_BAG_POSITION_X
        )
        self.y = BAG_POSITION_Y
        self.height = (
            DEFAULT_OPEN_BAG_HEIGHT if self.open else DEFAULT_CLOSED_BAG_HEIGHT
        )
        self.width = DEFAULT_BAG_WIDTH

    def get_html(self, additional_style="", additional_class=""):
        src = "images/open_bag.png" if self.open else "images/closed_bag.png"
        return img_(
            id=self.name,
            class_=f"prize prize_bag {additional_class}",
            src=src,
            alt="Bag",
            style=f"width: {self.width}; height: {self.height}; position: absolute; left: {self.x}; top: {self.y}; {additional_style}; ",
        )


class FilledBag(Bag):
    def __init__(
        self,
        name="",
        side="left",
        open: bool = False,
        num_coins: int = 1,
        clickable=False,
    ):
        super().__init__(name=name, side=side, open=open, clickable=clickable)
        self.num_coins = num_coins
        if self.num_coins not in [1, 2, 4]:
            raise ValueError("num_coins must be 1, 2, or 4")

    def get_html(self, additional_style="", additional_class=""):
        items = []

        # Add coins inside the bag
        for i, (coin_x, coin_y) in enumerate(self.get_coin_arrangements()):
            coin = Coin(
                name=f"filled_bag_coin_{self.side}_{i}",
                side=self.side,
                x=coin_x,
                y=coin_y,
            ).get_html(
                additional_style=additional_style,
                additional_class=additional_class,
            )
            items.append(coin)

        # Get the bag wrapper
        items.append(
            super().get_html(
                additional_style=additional_style,
                additional_class=additional_class,
            )
        )
        return div_(
            id=f"{self.name}_bag",
            class_=f"bag_container",
            onClick=f"{self.onclick_fn}(this);" if self.clickable else "",
            style=f"display: flex; justify-content: flex-start; {'cursor: pointer;' if self.clickable else ''}",
        )(*items)

    def get_coin_arrangements(self):
        # Define coin arrangement logic here

        positions = []
        if self.num_coins == 1:
            coin_y = (
                f"calc({BAG_POSITION_Y} + 3*{DEFAULT_OPEN_BAG_HEIGHT}/4 - 1vh)"
            )
            coin_x = f"calc({self.x} + {self.width}/2 - {COIN_INFO['width']}/2)"
            positions.append((coin_x, coin_y))
        elif self.num_coins == 2:
            coin_y = f"calc({BAG_POSITION_Y} + 3*{DEFAULT_OPEN_BAG_HEIGHT}/5)"
            coin_x1 = (
                f"calc({self.x} + 2*{self.width}/7 - {COIN_INFO['width']}/2)"
            )
            coin_x2 = (
                f"calc({self.x} + 5*{self.width}/7 - {COIN_INFO['width']}/2)"
            )
            positions.append((coin_x1, coin_y))
            positions.append((coin_x2, coin_y))
        elif self.num_coins == 4:
            coin_y1 = (
                f"calc({BAG_POSITION_Y} + 3*{DEFAULT_OPEN_BAG_HEIGHT}/4 - 1vh)"
            )
            coin_y2 = (
                f"calc({BAG_POSITION_Y} + 2.3*{DEFAULT_OPEN_BAG_HEIGHT}/4)"
            )
            coin_y3 = f"calc({BAG_POSITION_Y} + 1.6*{DEFAULT_OPEN_BAG_HEIGHT}/4 + 1vh)"
            coin_x1 = (
                f"calc({self.x} + {self.width}/2 - {COIN_INFO['width']}/2)"
            )
            coin_x2 = (
                f"calc({self.x} + {self.width}/5 - {COIN_INFO['width']}/2)"
            )
            coin_x3 = (
                f"calc({self.x} + 4*{self.width}/5 - {COIN_INFO['width']}/2)"
            )

            positions.append((coin_x1, coin_y1))
            positions.append((coin_x2, coin_y2))
            positions.append((coin_x3, coin_y2))
            positions.append((coin_x1, coin_y3))

        return positions


class Hook(Object):
    def __init__(
        self,
        name="",
        side="left",
        left=LEFT_HOOK_POSITION_X,
        top=CHEST_HOOK_POSITION_Y,
    ):
        super().__init__(name=name)
        self.side = side
        self.left = left
        self.top = top
        self.width = DEFAULT_HOOK_WIDTH
        self.height = DEFAULT_HOOK_HEIGHT

    def get_html(self, additional_style="", additional_class=""):
        hook = img_(
            id=self.name,
            class_=f"hook hook_{self.side} {additional_class}",
            src="images/hook.png",
            alt="Chest Hook",
            style=f"width: {self.width}; height: {self.height}; top: {self.top}; left: {self.left}; {additional_style}",
        )
        return hook


class Flag(Object):
    def __init__(self, name="", side="left"):
        super().__init__(name=name)
        self.side = side

    def get_html(self, additional_style="", additional_class=""):
        flag = img_(
            id=self.name,
            class_=f"occluder {additional_class}",
            src="images/pirate_flag.png",
            alt="Flag",
            style=f"width: {DEFAULT_FLAG_WIDTH}; height: {DEFAULT_FLAG_HEIGHT}; position: absolute; left: {LEFT_FLAG_POSITION_X if self.side == 'left' else RIGHT_FLAG_POSITION_X}; top: {FLAG_POSITION_Y}; {additional_style}",
        )
        return flag


class PrizeWithHook(Object):
    """
    Generate base HTML for a coin with hook
    """

    def __init__(self, prize: Prize, side="left"):
        super().__init__()
        self.side = side
        self.prize = prize

    def get_html(self, additional_style="", additional_class=""):
        # Get prize object
        prize_html = self.prize.get_html(
            additional_style="z-index: 9;",
            additional_class="hidden",
        )

        prize_top = self.prize.info["y"]
        prize_left = (
            self.prize.info["left_x"]
            if self.side == "left"
            else self.prize.info["right_x"]
        )

        # Calculate hook positions based on prize position and dimensions
        hook_y = f"calc({prize_top} - {DEFAULT_HOOK_HEIGHT} + 2vh)"

        if self.side == "left":
            hook_x = LEFT_HOOK_POSITION_X
        else:
            hook_x = RIGHT_HOOK_POSITION_X

        # Get hook object
        hook = Hook(
            name=f"hook_prize_{self.side}",
            side=self.side,
            left=hook_x,
            top=hook_y,
        ).get_html(additional_class="hidden")

        return div_(id=f"prize_with_hook_container")(prize_html, hook)


"""
Trials:
Training types: 2 chest,

"""


class Trial:
    def __init__(self, trial_info, occluded=False, prize_side=None):
        # trial_info: {stage 1: {include: True/False, prize_coins: int}, stage 2: {include: True/False, prize_coins: int}}
        self.occluded = occluded
        self.trial_info = trial_info
        self.prize_side = prize_side

    def get_stage1(self):

        pages = []

        # page 1
        items = []
        self.left = Chest(side="left")
        self.right = Chest(side="right")

        items.append(self.left.get_html())
        items.append(self.right.get_html())

        if not self.prize_side:
            self.prize_side = random.choice(["left", "right"])

        prize_bag = FilledBag(
            name=f"prize_{self.prize_side}",
            side=self.prize_side,
            open=True,
            num_coins=self.trial_info["stage_1"]["prize_coins"],
        )
        prize_html = prize_bag.get_html(additional_class="hidden")

        items.append(prize_html)

        # add occluder:
        if self.occluded:
            flag_left = Flag(name="initial_occluder", side="left").get_html(
                additional_class="hidden"
            )
            flag_right = Flag(name="initial_occluder", side="right").get_html(
                additional_class="hidden"
            )

            items.extend([flag_left, flag_right])
        items.append(div_(id="stage_indicator")(1))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        # page 2: ask for choice

        items = []

        # setting onclick fn depending on whether stage 2 is included
        onclick_fn = (
            "selectChest"
            if self.trial_info["stage_2"]["include"]
            else "openChest"
        )

        self.left.clickable = True
        self.right.clickable = True

        self.left.onclick_fn = onclick_fn
        self.right.onclick_fn = onclick_fn

        prize_bag.open = False
        if self.prize_side == "left":
            self.left.prize = prize_bag
        else:
            self.right.prize = prize_bag

        items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="clicked_side",  # name for the server log
        )
        items.append(hidden_input)

        choice_page = div_(style="display: flex;")(*items)

        pages.append(choice_page)

        return pages

    def get_stage2(self, keep_side):
        print("Generating stage 2 pages for chosen side:", keep_side)
        if not self.trial_info["stage_2"]["include"]:
            return []

        replace_side = "right" if keep_side == "left" else "left"

        pages = []

        # page 1: animation of hook
        items = []

        kept_chest = self.left if keep_side == "left" else self.right
        kept_chest.clickable = False  # Disable clicking on kept chest
        items.append(kept_chest.get_html())

        # declaring the new prize
        prize_obj = FilledBag(
            name=f"hooked_prize_{replace_side}",
            side=replace_side,
            open=False,
            clickable=False,
            num_coins=self.trial_info["stage_2"]["prize_coins"],
        )

        PWH_object = PrizeWithHook(prize=prize_obj, side=replace_side)

        if replace_side == "left":
            self.left = prize_obj
        else:
            self.right = prize_obj

        items.append(PWH_object.get_html())
        items.append(chest_with_hook_(side=replace_side))

        items.append(div_(id="stage_indicator")(2))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        # page 2
        items = []

        self.left.clickable = True
        self.right.clickable = True

        # changing the chest onclick function to open
        if keep_side == "left":
            self.left.onclick_fn = "openChest"
        else:
            self.right.onclick_fn = "openChest"

        items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="clicked_side",  # name for the server log
        )
        items.append(hidden_input)

        choice_page = div_(style="display: flex;")(*items)

        pages.append(choice_page)

        return pages


@kesar
def experiment(uid):
    data = {}
    animals = ["cat", "dog", "beaver"]

    # trial_pages = [coin]
    trial_num = 0
    for trial_num in range(1):
        print("Starting trial num: ", trial_num + 1)
        trial_info = {
            "stage_1": {"include": True, "prize_coins": 4},
            "stage_2": {"include": True, "prize_coins": 4},
        }

        trial = Trial(trial_info=trial_info, occluded=True)

        all_pages = trial.get_stage1().copy()  # Get all pages for stage 1
        page_ind = 0

        trial_data = {
            "trial_number": trial_num + 1,
            "prize_side": trial.prize_side,
        }

        while page_ind < len(all_pages):
            print("Displaying page", page_ind + 1, "of", len(all_pages))
            response = yield all_pages[page_ind]

            print("Recieved_response:", response)

            if "clicked_side" in response:
                if page_ind == 1:
                    chosen_side = response["clicked_side"]
                    print("Chosen side:", chosen_side)

                    # After choice, add stage 2 pages
                    if trial_info["stage_2"]["include"]:
                        stage2_pages = trial.get_stage2(
                            keep_side=chosen_side[0]
                        )
                        all_pages.extend(stage2_pages)

                    trial_data["Stage 1 Choice"] = response
                else:
                    trial_data["Stage 2 Choice"] = response
            page_ind += 1
        data[trial_num + 1] = trial_data
    # items = []
    # items.append(
    #     FilledBag(
    #         name="test_bag", side="left", open=False, num_coins=4
    #     ).get_html(additional_style="z-index: 5;")
    # )

    # items.append(Chest(side="left").get_html())

    # items.append(
    #     FilledBag(
    #         name="test_bag", side="right", open=True, num_coins=4
    #     ).get_html(additional_style="z-index: 5;")
    # )

    # items.append(Chest(side="right").get_html())
    # yield div_(style="display: flex;")(*items)

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
