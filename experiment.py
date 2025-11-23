from kesar import *
from constants import *
import random
from visual import *

SCORE = ScoreDisplay(score=0)
METER = ScoreMeter()


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


"""
Trials:
Training types: 2 chest,

"""


class Trial:
    def __init__(self, trial_info, occluded="", prize_side=None):
        # trial_info: {stage 1: {include: True/False, prize_coins: int}, stage 2: {include: True/False, prize_coins: int}}
        self.occluded = occluded
        self.trial_info = trial_info
        self.first_prize_side = prize_side
        self.num_stages = 2 if trial_info["stage_2"]["include"] else 1

    def get_stage1(self):

        pages = []

        # page 1
        items = []
        self.left = Chest(side="left")
        self.right = Chest(side="right")

        items.append(self.left.get_html())
        items.append(self.right.get_html())

        if not self.first_prize_side:
            self.first_prize_side = random.choice(["left", "right"])

        prize_bag = FilledBag(
            name=f"prize_{self.first_prize_side}",
            side=self.first_prize_side,
            open=True,
            num_coins=self.trial_info["stage_1"]["prize_coins"],
        )
        prize_html = prize_bag.get_html(additional_class="hidden")

        items.append(prize_html)

        # add occluder:
        if self.occluded:
            flag_left = Occluder(
                name="initial_occluder", side="left", type=self.occluded
            ).get_html(additional_class="hidden")
            flag_right = Occluder(
                name="initial_occluder", side="right", type=self.occluded
            ).get_html(additional_class="hidden")

            items.extend([flag_left, flag_right])

        items.append(div_(id="stage_indicator")(1))
        items.append(SCORE.get_html())
        items.append(METER.get_html())

        animation_page = div_(id="experiment_screen", style="display: flex;")(
            *items
        )
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

        # assigning prize to chest

        prize_bag.open = False
        if self.first_prize_side == "left":
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
        items.append(SCORE.get_html())
        items.append(METER.get_html())

        choice_page = div_(id="experiment_screen", style="display: flex;")(
            *items
        )

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
        items.append(SCORE.get_html())
        items.append(METER.get_html())

        animation_page = div_(id="experiment_screen", style="display: flex;")(
            *items
        )
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
        items.append(SCORE.get_html())
        items.append(METER.get_html())

        choice_page = div_(id="experiment_screen", style="display: flex;")(
            *items
        )

        pages.append(choice_page)

        return pages


class OneStageTrainingTrial(Trial):
    def __init__(self, stage1_coins, occluded="", prize_side=None):
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
            },
            "stage_2": {
                "include": False,
                "prize_coins": 0,
            },
        }
        super().__init__(trial_info, occluded=occluded, prize_side=prize_side)


class TwoStageTrainingTrial(Trial):
    def __init__(
        self, stage1_coins, stage2_coins, occluded="", prize_side=None
    ):
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
            },
            "stage_2": {
                "include": True,
                "prize_coins": stage2_coins,
            },
        }
        super().__init__(trial_info, occluded=occluded, prize_side=prize_side)


class TestingTrial(Trial):
    def __init__(self, stage1_coins, stage2_coins, prize_side=None):
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
            },
            "stage_2": {
                "include": True,
                "prize_coins": stage2_coins,
            },
        }
        super().__init__(trial_info, occluded="full", prize_side=prize_side)


def start_page():
    return div_(id="start_page")(
        ScoreMeter().get_html(),
        button_(id="start_button", onClick="startExperiment()")(
            "Click to begin!"
        ),
    )


@kesar
def experiment(uid):
    SCORE.score = 0
    METER.curr_score = 0

    data = {}

    trials = [
        # OneStageTrainingTrial(stage1_coins=4),
        # OneStageTrainingTrial(stage1_coins=2, occluded="partial"),
        TwoStageTrainingTrial(
            stage1_coins=2, stage2_coins=4, occluded="partial"
        ),
        TestingTrial(stage1_coins=2, stage2_coins=4),
    ]

    # Begin
    yield start_page()

    for trial_num in range(len(trials)):
        print("Starting trial num: ", trial_num + 1)
        trial = trials[trial_num]
        all_pages = trial.get_stage1().copy()  # Get all pages for stage 1
        page_ind = 0

        trial_data = {
            "trial_number": trial_num + 1,
            "prize_side": trial.first_prize_side,
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
                    if trial.num_stages == 2:
                        stage2_pages = trial.get_stage2(
                            keep_side=chosen_side[0]
                        )
                        all_pages.extend(stage2_pages)
                    else:
                        # If only stage 1, assign score
                        if chosen_side[0] == trial.first_prize_side:
                            coin_amount = trial.trial_info["stage_1"][
                                "prize_coins"
                            ]
                            SCORE.score += coin_amount
                            METER.curr_score = SCORE.score

                    trial_data["Stage 1 Choice"] = response
                else:
                    trial_data["Stage 2 Choice"] = response

                    # if stage 2 choice is not the original prize side, add stage 2 coins
                    if chosen_side[0] != trial.first_prize_side:
                        coin_amount = trial.trial_info["stage_2"]["prize_coins"]

                    else:
                        coin_amount = trial.trial_info["stage_1"]["prize_coins"]
                    SCORE.score += coin_amount
                    METER.curr_score += SCORE.score
            page_ind += 1
        data[trial_num + 1] = trial_data

    return data  # to be logged


# // <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
# // <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/MotionPathPlugin.min.js"></script>
