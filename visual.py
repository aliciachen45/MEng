from kesar import *
from constants import *


class ScoreDisplay:
    def __init__(self, name="score_display", score=0):
        self.name = name
        self.score = score

    def get_html(self):
        return div_(
            id=self.name,
            class_=f"score_display",
        )(f"{self.score}")


class Object:
    def __init__(self, name="", clickable=False):
        self.name = name
        self.clickable = clickable

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


class Coin(Object):
    def __init__(self, name="", side="left", clickable=False, x=None, y=None):
        super().__init__(name=name, clickable=clickable)
        self.side = side
        self.width = DEFAULT_COIN_WIDTH
        if x:
            self.x = x
        else:
            self.x = (
                LEFT_COIN_POSITION_X
                if self.side == "left"
                else RIGHT_COIN_POSITION_X
            )

        if y:
            self.y = y
        else:
            self.y = COIN_POSITION_Y

    def get_html(self, additional_style="", additional_class=""):
        return img_(
            id=self.name,
            class_=f"prize {additional_class}",
            src="images/coin.png",
            alt="Coin",
            onClick=f"{self.onclick_fn}(this);" if self.clickable else "",
            style=f"width: {self.width}; top: {self.y}; left: {self.x}; {additional_style}; {'cursor: pointer;' if self.clickable else ''}",
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


class Occluder(Object):
    def __init__(self, name="", side="left", type="partial"):
        super().__init__(name=name)
        self.side = side
        self.type = type
        self.occluder_info = (
            PARTIAL_OCCLUDER_INFO if type == "partial" else FULL_OCCLUDER_INFO
        )

    def get_html(self, additional_style="", additional_class=""):
        print("Occluder types", self.type)
        flag = img_(
            id=self.name,
            class_=f"occluder {additional_class}",
            src=f"images/{self.type}_occluder.png",
            alt=f"{self.type.capitalize()} Occluder",
            style=f"width: {self.occluder_info['width']}; height: {self.occluder_info['height']}; position: absolute; left: {self.occluder_info['left_x'] if self.side == 'left' else self.occluder_info['right_x']}; top: {self.occluder_info['y']}; {additional_style}",
        )
        return flag


class Prize(Object):
    def __init__(self, name="", clickable=False, prize_info={}):
        super().__init__(name=name, clickable=clickable)
        self.info = prize_info


class Bag(Prize):
    def __init__(self, name="", side="left", open=True, clickable=False):
        super().__init__(name=name, clickable=clickable, prize_info=BAG_INFO)
        self.side = side
        self.open = open
        self.onclick_fn = "revealCoinsAndBag"
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
        # prize_left = (
        #     self.prize.info["left_x"]
        #     if self.side == "left"
        #     else self.prize.info["right_x"]
        # )

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
