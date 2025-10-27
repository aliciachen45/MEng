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


def coin_(id, additional_style="", additional_class=""):
    """
    Generate base HTML for a coin
    """

    return Coin(name=id).get_html(
        additional_style=additional_style, additional_class=additional_class
    )


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
        self, name="", side="left", clickable=False, prize=None, onclick_fn=None
    ):
        super().__init__(name=name, clickable=clickable)
        self.side = side
        self.prize = prize
        self.onclick_fn = onclick_fn

    def get_html(self, additional_style=""):
        items = ChestShell(
            name=self.name, side=self.side, clickable=self.clickable
        ).get_html(additional_style=additional_style)

        if self.prize:
            prize_object = self.prize(
                name=f"prize_image_{self.side}", side=self.side
            )
            items.append(
                prize_object.get_html(additional_style=additional_style)
            )

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


class Coin(Prize):
    def __init__(self, name="", side="left", clickable=False):
        super().__init__(name=name)
        self.info = COIN_INFO
        self.side = side
        self.clickable = clickable
        self.onclick_fn = "revealCoin"

    def get_html(self, additional_style="", additional_class=""):
        prize_width, _ = (
            self.info["width"],
            self.info["height"],
        )

        prize_left = (
            self.info["left_x"] if self.side == "left" else self.info["right_x"]
        )

        prize_top = self.info["y"]
        return img_(
            id=self.name,
            class_=f"prize {additional_class}",
            src="images/coin.png",
            alt="Coin",
            onClick=f"{self.onclick_fn}(this);" if self.clickable else "",
            style=f"width: {prize_width}; top: {prize_top}; left: {prize_left}; {additional_style}; {'cursor: pointer;' if self.clickable else ''}",
        )


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

    def __init__(self, prize, side="left"):
        super().__init__()
        self.side = side
        self.prize = prize(name=f"hooked_prize_{side}", side=self.side)

    def get_html(self, additional_style="", additional_class=""):
        # Get prize object
        prize_html = self.prize.get_html(
            additional_style="z-index: 4;", additional_class="hidden"
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
            hook_x = f"calc({prize_left} + {self.prize.info['width']} - {DEFAULT_HOOK_WIDTH})"
        else:
            hook_x = prize_left

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
    def __init__(
        self, occluded=False, two_stage=False, prize_class=None, prize_side=None
    ):
        self.occluded = occluded
        self.two_stage = two_stage
        self.prize = prize_class
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

        coin = Coin(name="stage_1_coin", side=self.prize_side).get_html(
            additional_class="coin_stage_1 hidden"
        )

        items.append(coin)

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

        onclick_fn = "selectChest" if self.two_stage else "openChest"

        self.left.clickable = True
        self.right.clickable = True

        self.left.onclick_fn = onclick_fn
        self.right.onclick_fn = onclick_fn

        if self.prize_side == "left":
            self.left.prize = self.prize_class
        else:
            self.right.prize = self.prize_class

        items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
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
        if not self.two_stage:
            return []

        replace_side = "right" if keep_side == "left" else "left"

        pages = []

        # page 1: animation of hook
        items = []

        kept_chest = self.left if keep_side == "left" else self.right
        kept_chest.clickable = False  # Disable clicking on kept chest
        items.append(kept_chest.get_html())

        PWH_object = PrizeWithHook(prize=Coin, side=replace_side)

        if replace_side == "left":
            self.left = PWH_object.prize
        else:
            self.right = PWH_object.prize

        items.append(PWH_object.get_html())
        items.append(chest_with_hook_(side=replace_side))

        items.append(div_(id="stage_indicator")(2))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        # page 2
        items = []

        onclick_fn = "openChest"

        self.left.clickable = True
        self.right.clickable = True
        if self.left.clickfn_mutable:
            self.left.onclick_fn = onclick_fn
        if self.right.clickfn_mutable:
            self.right.onclick_fn = onclick_fn

        items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="chest_clicked",  # name for the server log
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
    for trial_num in range(3):
        print("Starting trial num: ", trial_num + 1)

        trial = Trial(occluded=True, two_stage=True, prize_class=Coin)

        all_pages = trial.get_stage1().copy()  # Get all pages for stage 1
        page_ind = 0

        while page_ind < len(all_pages):
            print("Displaying page", page_ind + 1, "of", len(all_pages))
            response = yield all_pages[page_ind]

            print("Recieved_response:", response)

            if "chest_clicked" in response:
                if page_ind == 1:
                    chosen_side = response["chest_clicked"]
                    print("Chosen side:", chosen_side)

                    # After choice, add stage 2 pages
                    stage2_pages = trial.get_stage2(keep_side=chosen_side[0])
                    all_pages.extend(stage2_pages)

                data[page_ind] = response
            page_ind += 1

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
