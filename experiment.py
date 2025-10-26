from kesar import *
from constants import *
import random

# import visual
# import os


def chest_(
    prize=None,
    side="left",
    onclick_fn="selectChest",
):
    items = Chest(name="chest", side=side).get_html()

    if prize:
        prize_object = prize(name=f"prize_image_{side}", side=side)
        items.extend(prize_object.get_html())

        # add the sound effect
    else:
        pass
        # add the sound effect

    return div_(
        id=f"chest_container_{side}",
        style=f"display: flex; justify-content: flex-start; cursor: pointer;",
        onClick=f"{onclick_fn}(this);",
    )(*items)


def coin_(id, additional_style="", additional_class=""):
    """
    Generate base HTML for a coin
    """

    return Coin(name=id).get_html(
        additional_style=additional_style, additional_class=additional_class
    )[0]


def chest_with_hook_(side="left"):
    """
    Generate base HTML for a chest with hook
    """
    # Get chest object
    print("Generating chest with hook for side:", side)
    chest = chest_(side=side)

    # Get hook object
    hook_x = LEFT_HOOK_POSITION_X if side == "left" else RIGHT_HOOK_POSITION_X
    hook = Hook(
        name=f"hook_chest_{side}",
        side=side,
        left=hook_x,
        top=CHEST_HOOK_POSITION_Y,
    ).get_html(additional_class="hidden")[0]

    return div_(id=f"chest_with_hook_container_{side}")(chest, hook)


def prize_with_hook_(prize, side="left"):
    """
    Generate base HTML for a coin with hook
    """
    # Get prize object

    prize_object = prize(name="hooked_prize", side=side)
    prize_html = prize_object.get_html(
        additional_style="z-index: 4;", additional_class="hidden"
    )[0]

    prize_top = prize_object.info["y"]
    prize_left = (
        prize_object.info["left_x"]
        if side == "left"
        else prize_object.info["right_x"]
    )

    # Calculate hook positions based on prize position and dimensions
    hook_y = f"calc({prize_top} - {DEFAULT_HOOK_HEIGHT} + 2vh)"

    if side == "left":
        hook_x = f"calc({prize_left} + {prize_object.info['width']} - {DEFAULT_HOOK_WIDTH})"
    else:
        hook_x = prize_left

    # Get hook object
    hook = Hook(
        name=f"hook_prize_{side}",
        side=side,
        left=hook_x,
        top=hook_y,
    ).get_html(additional_class="hidden")[0]

    return div_(id=f"prize_with_hook_container")(prize_html, hook)


class Object:
    def __init__(self, name=""):
        self.name = name

    def get_html(self):
        raise NotImplementedError("Subclasses must implement get_html method.")


class Chest(Object):
    def __init__(self, name="", side="left"):
        super().__init__(name=name)
        self.side = side

    def get_html(self):
        items = [
            img_(
                id=f"chest_top_image_{self.side}",
                class_=f"chest_top_image",
                src="images/chest_top.png",
                alt="A treasure chest top",
                style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_TOP_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if self.side == 'left' else RIGHT_CHEST_POSITION_X};",
            ),
            img_(
                id=f"chest_bottom_image_{self.side}",
                class_=f"chest_bottom_image",
                src="images/chest_bottom.png",
                alt="A treasure chest bottom",
                style=f"width: {DEFAULT_CHEST_WIDTH}; top: {CHEST_BOTTOM_POSITION_Y}; left: {LEFT_CHEST_POSITION_X if self.side == 'left' else RIGHT_CHEST_POSITION_X};",
            ),
        ]
        return items


class Prize(Object):
    def __init__(self, name=""):
        super().__init__(name=name)


class Coin(Prize):
    def __init__(self, name="", side="left"):
        super().__init__(name=name)
        self.info = COIN_INFO
        self.side = side

    def get_html(self, additional_style="", additional_class=""):
        prize_width, _ = (
            self.info["width"],
            self.info["height"],
        )

        prize_left = (
            self.info["left_x"] if self.side == "left" else self.info["right_x"]
        )

        prize_top = self.info["y"]
        return [
            img_(
                id=self.name,
                class_=f"prize {additional_class}",
                src="images/coin.png",
                alt="Coin",
                style=f"width: {prize_width}; top: {prize_top}; left: {prize_left}; {additional_style}",
            )
        ]


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
        return [hook]


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
        return [flag]


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
        items.append(chest_(id="left", side="left"))
        items.append(chest_(id="right", side="right"))
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
            prize=Coin(),
            side="right",
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
        items.append(chest_(side="left"))
        items.append(chest_(side="right"))

        coin_side = random.choice(["left", "right"])

        coin = Coin(name="stage_1_coin", side=coin_side).get_html(
            additional_class="coin_stage_1 hidden"
        )[0]

        items.append(coin)

        # add occluder:
        flag_left = Flag(name="initial_occluder", side="left").get_html(
            additional_class="hidden"
        )[0]
        flag_right = Flag(name="initial_occluder", side="right").get_html(
            additional_class="hidden"
        )[0]

        items.extend([flag_left, flag_right])
        items.append(div_(id="stage_indicator")(1))

        animation_page = div_(style="display: flex;")(*items)
        pages.append(animation_page)

        # page 2: ask for choice

        items = []

        if coin_side == "left":
            self.chest_left = chest_(
                prize=Coin,
                side="left",
            )
            self.chest_right = chest_(side="right")
        else:
            self.chest_left = chest_(side="left")
            self.chest_right = chest_(
                prize=Coin,
                side="right",
            )

        items.extend([self.chest_left, self.chest_right])

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
            prize_with_hook_(prize=Coin, side=replace_side),
            chest_with_hook_(side=replace_side),
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
