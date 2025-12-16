from kesar import *
from constants import *
import random
from visual import *

SCORE = ScoreDisplay()
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
    trial_num = 1
    play_flag_intro = True
    play_hook_intro = True
    trigger_highlight = True

    def __init__(self, trial_info, prize_side=None):
        # trial_info: {stage 1: {include: True/False, prize_coins: int}, stage 2: {include: True/False, prize_coins: int}}
        # self.occluded = occluded
        self.trial_info = trial_info

        if not prize_side:
            self.first_prize_side = random.choice(["left", "right"])
        else:
            self.first_prize_side = prize_side
        self.num_stages = 2 if trial_info["stage_2"]["include"] else 1
        self.trial_type = ""
        self.trial_num = Trial.trial_num
        Trial.trial_num += 1
        self.occluder_type = trial_info["stage_1"]["occluder"]
        self.max_coins = max(
            trial_info["stage_1"]["prize_coins"],
            trial_info["stage_2"]["prize_coins"],
        )

    def _prep_experiment_page(self, items, curr_stage):
        items.append(div_(id="processing-overlay")(""))

        items.append(div_(id="REMOVE")(self.trial_info))

        items.append(div_(id="stage_indicator", class_="variable")(curr_stage))
        items.append(div_(id="trial_type", class_="variable")(self.trial_type))

        items.append(
            div_(id="first_trial", class_="variable")(self.trial_num == 1)
        )

        items.append(
            div_(id="occluder_type", class_="variable")(self.occluder_type)
        )
        items.append(div_(id="num_stages", class_="variable")(self.num_stages))

        items.append(div_(id="max_coins", class_="variable")(self.max_coins))

        # items.append(
        #     div_(id="trigger_highlight", class_="variable")(
        #         Trial.trigger_highlight
        #     )
        # )

        items.append(
            div_(id="play_flag_intro", class_="variable")(Trial.play_flag_intro)
        )

        if Trial.trigger_highlight:
            items.append(div_(id="score_highlight")(""))

        if Trial.play_flag_intro and self.occluder_type != "":
            Trial.play_flag_intro = False

        items.append(
            div_(id="play_hook_intro", class_="variable")(Trial.play_hook_intro)
        )
        if curr_stage == 2 and Trial.play_hook_intro:
            Trial.play_hook_intro = False

        items.append(SCORE.get_html())
        items.append(METER.get_html())
        return div_(id="experiment_screen", style="display: flex;")(*items)

    def get_stage1(self):

        pages = []

        # page 1
        items = []

        self.left = Chest(side="left")
        self.right = Chest(side="right")

        onclick_fn = (
            "selectChest"
            if self.trial_info["stage_2"]["include"]
            else "openChest"
        )

        self.left.onclick_fn = onclick_fn
        self.right.onclick_fn = onclick_fn

        # prize_bag.open = False
        # if self.first_prize_side == "left":
        #     self.left.prize = prize_bag
        # else:
        #     self.right.prize = prize_bag

        items.append(self.left.get_html())
        items.append(self.right.get_html())

        prize_bag = FilledBag(
            name=f"prize_{self.first_prize_side}",
            side=self.first_prize_side,
            open=True,
            num_coins=self.trial_info["stage_1"]["prize_coins"],
        )
        prize_html = prize_bag.get_html(additional_class="hidden")

        items.append(prize_html)

        # add occluder:
        if self.trial_info["stage_1"]["occluder"] == "full":
            flag_left = Occluder(
                name="initial_occluder", side="left", type="full"
            ).get_html(additional_class="hidden")
            flag_right = Occluder(
                name="initial_occluder", side="right", type="full"
            ).get_html(additional_class="hidden")
            items.extend([flag_left, flag_right])
        elif self.trial_info["stage_1"]["occluder"] == "partial":
            flag_left = Occluder(
                name="initial_occluder", side="left", type="partial"
            ).get_html(additional_class="hidden")
            flag_right = Occluder(
                name="initial_occluder", side="right", type="partial"
            ).get_html(additional_class="hidden")
            items.extend([flag_left, flag_right])
        elif self.trial_info["stage_1"]["occluder"] == "":
            pass
        else:
            raise ValueError(
                "Invalid occluder type: {}".format(
                    self.trial_info["stage_1"]["occluder"]
                )
            )

        # pages.append(animation_page)

        # page 2: ask for choice
        # items = []

        # setting onclick fn depending on whether stage 2 is included

        # assigning prize to chest

        # items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="clicked_side",  # name for the server log
        )
        items.append(hidden_input)

        choice_page = self._prep_experiment_page(items, curr_stage=1)
        # animation_page = self._prep_experiment_page(items, curr_stage=1)

        pages.append(choice_page)

        return pages

    def get_stage2(self, keep_side):
        pages = []

        # page 1: animation of hook
        items = []
        print("Generating stage 2 pages for chosen side:", keep_side)
        if not self.trial_info["stage_2"]["include"]:
            return []

        if keep_side == "left":
            self.left.onclick_fn = "openChest"
            if self.first_prize_side == "left":
                first_prize = FilledBag(
                    name=f"prize_{self.first_prize_side}",
                    side=self.first_prize_side,
                    open=False,
                    num_coins=self.trial_info["stage_1"]["prize_coins"],
                )
                self.left.prize = first_prize
        else:
            self.right.onclick_fn = "openChest"
            if self.first_prize_side == "right":
                first_prize = FilledBag(
                    name=f"prize_{self.first_prize_side}",
                    side=self.first_prize_side,
                    open=False,
                    num_coins=self.trial_info["stage_1"]["prize_coins"],
                )
                self.right.prize = first_prize

        replace_side = "right" if keep_side == "left" else "left"
        kept_chest = self.left if keep_side == "left" else self.right

        items.append(kept_chest.get_html())

        # declaring the new prize
        prize_obj = FilledBag(
            name=f"hooked_prize_{replace_side}",
            side=replace_side,
            open=False,
            num_coins=self.trial_info["stage_2"]["prize_coins"],
        )

        PWH_object = PrizeWithHook(prize=prize_obj, side=replace_side)

        if replace_side == "left":
            self.left = prize_obj
        else:
            self.right = prize_obj

        items.append(PWH_object.get_html())
        # items.append(chest_with_hook_(side=replace_side))

        # animation_page = self._prep_experiment_page(items, curr_stage=2)
        # pages.append(animation_page)

        # page 2
        # items = []

        # changing the chest onclick function to open

        # items.extend([self.left.get_html(), self.right.get_html()])

        # hidden input to record choice
        hidden_input = input_(
            type_="hidden",
            id="choice_input",  # id for JavaScript
            name="clicked_side",  # name for the server log
        )
        items.append(hidden_input)

        choice_page = self._prep_experiment_page(items, curr_stage=2)

        pages.append(choice_page)

        return pages


class OneStageTrainingTrial(Trial):
    def __init__(self, stage1_coins, occluded="", prize_side=None):
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
                "occluder": occluded,
            },
            "stage_2": {
                "include": False,
                "prize_coins": 0,
            },
        }
        super().__init__(trial_info, prize_side=prize_side)
        self.trial_type = "training"


class TwoStageTrainingTrial(Trial):
    def __init__(
        self,
        stage1_coins,
        stage2_coins,
        occluded="",
        prize_side=None,
    ):
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
                "occluder": occluded,
            },
            "stage_2": {
                "include": True,
                "prize_coins": stage2_coins,
            },
        }
        super().__init__(trial_info, prize_side=prize_side)
        self.trial_type = "training"


class TestingTrial(Trial):
    def __init__(
        self,
        stage1_coins,
        stage2_coins,
        prize_side=None,
        one_chest=True,
    ):

        if one_chest:
            occluder_type = "partial"
        else:
            occluder_type = "full"
        trial_info = {
            "stage_1": {
                "include": True,
                "prize_coins": stage1_coins,
                "occluder": occluder_type,  # can also be full, partial, one-side (implies partial)
            },
            "stage_2": {
                "include": True,
                "prize_coins": stage2_coins,
            },
        }
        super().__init__(trial_info, prize_side=prize_side)
        self.trial_type = "testing"


def start_page():
    return div_(id="start_page")(
        button_(id="start_button", onClick="startExperiment()")(
            "Click to begin!"
        ),
    )


# def run_onestagetraining(trial_num):
def run_training_trial1(data):
    possible_coins = [2]
    # One stage training trial with no occluders

    while True:
        n = possible_coins[0]
        trial = OneStageTrainingTrial(stage1_coins=n)
        print("Starting trial num: ", trial.trial_num)

        all_pages = trial.get_stage1().copy()
        correct_side = trial.first_prize_side
        trial_data = {
            "trial_number": trial.trial_num,
            "prize_side": correct_side,
            "coins1": n,
        }

        # yield all_pages[0]

        choice = yield all_pages[0]
        print("Recieved_response:", choice)
        trial_data["choice1"] = choice

        data[trial.trial_num] = trial_data

        if choice["clicked_side"][0] == trial.first_prize_side:
            coin_amount = trial.trial_info["stage_1"]["prize_coins"]
            SCORE.score += coin_amount
            METER.curr_score = SCORE.score

        if trial_data["choice1"]["clicked_side"][0] == trial_data["prize_side"]:
            Trial.trigger_highlight = False
            break


def run_training_trial2(data):
    possible_coins = [1]
    # One stage training tiral w/occluders:

    while True:
        n = possible_coins[0]
        trial = OneStageTrainingTrial(stage1_coins=n, occluded="partial")
        print("Starting trial num: ", trial.trial_num)

        all_pages = trial.get_stage1().copy()
        correct_side = trial.first_prize_side
        trial_data = {
            "trial_number": trial.trial_num,
            "prize_side": correct_side,
            "coins1": n,
        }

        # yield all_pages[0]

        choice = yield all_pages[0]
        print("Recieved_response:", choice)
        trial_data["choice1"] = choice

        data[trial.trial_num] = trial_data

        if choice["clicked_side"][0] == trial.first_prize_side:
            coin_amount = trial.trial_info["stage_1"]["prize_coins"]
            SCORE.score += coin_amount
            METER.curr_score = SCORE.score

        if trial_data["choice1"]["clicked_side"][0] == trial_data["prize_side"]:
            break


def run_training_trial3(data):
    possible_combos = [
        # (4, 1),
        # (2, 1),
        (4, 2),
    ]

    # Two stage training trial, correct choice is chest
    while True:
        n1, n2 = possible_combos[0]
        trial = TwoStageTrainingTrial(
            stage1_coins=n1,
            stage2_coins=n2,
            occluded="partial",
        )
        print("Starting trial num: ", trial.trial_num)

        stage1_pages = trial.get_stage1().copy()
        correct_side = trial.first_prize_side
        trial_data = {
            "trial_number": trial.trial_num,
            "prize_side": correct_side,
            "coins1": n1,
            "coins2": n2,
        }

        # yield stage1_pages[0]

        first_response = yield stage1_pages[0]
        first_choice = first_response["clicked_side"][0]
        print("Recieved_response:", first_choice)
        trial_data["choice1"] = first_response

        # Stage 2 pages
        stage2_pages = trial.get_stage2(keep_side=first_choice)

        # yield stage2_pages[0]

        second_response = yield stage2_pages[0]
        second_choice = second_response["clicked_side"][0]
        trial_data["choice2"] = second_response

        if second_choice != first_choice:
            print(
                "Stage 2 choice differs from stage 1 choice. They chose stage 2 coins"
            )
            coin_amount = trial.trial_info["stage_2"]["prize_coins"]
        else:
            if first_choice == trial.first_prize_side:
                coin_amount = trial.trial_info["stage_1"]["prize_coins"]
            else:
                coin_amount = 0

        SCORE.score += coin_amount
        METER.curr_score = SCORE.score

        data[trial.trial_num] = trial_data
        if coin_amount == trial.max_coins:
            break
        # if (
        #     trial.trial_info["stage_2"]["prize_coins"]
        #     > trial.trial_info["stage_1"]["prize_coins"]
        # ):  # correct choice is to switch
        #     if second_choice != trial.first_prize_side:
        #         break
        # else:  # correct choice is to stay
        #     if second_choice == trial.first_prize_side:
        #         break


def run_training_trial4(data):
    possible_combos = [
        # (1, 2),
        # (1, 4),
        (2, 4)
    ]
    # Two stage training trial, correct choice is bag
    while True:
        n1, n2 = possible_combos[0]
        trial = TwoStageTrainingTrial(
            stage1_coins=n1,
            stage2_coins=n2,
            occluded="partial",
        )
        print("Starting trial num: ", trial.trial_num)

        stage1_pages = trial.get_stage1().copy()
        correct_side = trial.first_prize_side
        trial_data = {
            "trial_number": trial.trial_num,
            "prize_side": correct_side,
            "coins1": n1,
            "coins2": n2,
        }

        # yield stage1_pages[0]

        first_response = yield stage1_pages[0]
        first_choice = first_response["clicked_side"][0]
        print("Recieved_response:", first_choice)
        trial_data["choice1"] = first_response

        # Stage 2 pages
        stage2_pages = trial.get_stage2(keep_side=first_choice)

        # yield stage2_pages[0]

        second_response = yield stage2_pages[0]
        second_choice = second_response["clicked_side"][0]
        trial_data["choice2"] = second_response

        if second_choice != first_choice:
            print(
                "Stage 2 choice differs from stage 1 choice. They chose stage 2 coins"
            )
            coin_amount = trial.trial_info["stage_2"]["prize_coins"]
        else:
            if first_choice == trial.first_prize_side:
                coin_amount = trial.trial_info["stage_1"]["prize_coins"]
            else:
                coin_amount = 0

        SCORE.score += coin_amount
        METER.curr_score = SCORE.score

        data[trial.trial_num] = trial_data

        if coin_amount == trial.max_coins:
            break
        # if (
        #     trial.trial_info["stage_2"]["prize_coins"]
        #     > trial.trial_info["stage_1"]["prize_coins"]
        # ):  # correct choice is to switch
        #     if second_choice != trial.first_prize_side:
        #         break
        # else:  # correct choice is to stay
        #     if second_choice == trial.first_prize_side:
        #         break


def run_testing_trial(data):
    num_testing_trials = 1

    test_trials = [
        {
            "stage1_coins": 2,
            "stage2_coins": 1,
            "one_chest": True,
        },  # Equivalent to 1 cup trial, higher chest EV, No chest Uncertainty, OG
        # {
        #     "stage1_coins": 4,
        #     "stage2_coins": 1,
        #     "one_chest": False,
        # },  # Equivalent to 2 cup trial, higher chest EV, high chest uncertainty,
        # {
        #     "stage1_coins": 2,
        #     "stage2_coins": 1,
        #     "one_chest": False,
        # },  # Equivalent to 2 cup trial, equal chest EV, high chest uncertainty, OG
        # {
        #     "stage1_coins": 4,
        #     "stage2_coins": 2,
        #     "one_chest": False,
        # },  # Equivalent to 2 cup trial, equal chest EV, high chest uncertainty, modified for higher numbers
    ]
    for _ in range(num_testing_trials):
        for trial_info in test_trials:
            trial = TestingTrial(
                stage1_coins=trial_info["stage1_coins"],
                stage2_coins=trial_info["stage2_coins"],
                one_chest=trial_info["one_chest"],
            )
            print("Starting trial num: ", trial.trial_num)

            stage1_pages = trial.get_stage1().copy()
            correct_side = trial.first_prize_side
            trial_data = {
                "trial_number": trial.trial_num,
                "prize_side": correct_side,
                "coins1": trial_info["stage1_coins"],
                "coins2": trial_info["stage2_coins"],
            }

            first_response = yield stage1_pages[0]
            first_choice = first_response["clicked_side"][0]
            print("Recieved_response:", first_choice)
            trial_data["choice1"] = first_response

            # Stage 2 pages
            stage2_pages = trial.get_stage2(keep_side=first_choice)

            second_response = yield stage2_pages[0]
            second_choice = second_response["clicked_side"][0]
            trial_data["choice2"] = second_response

            if second_choice != first_choice:
                print(
                    "Stage 2 choice differs from stage 1 choice. They chose stage 2 coins"
                )
                coin_amount = trial.trial_info["stage_2"]["prize_coins"]
            else:
                coin_amount = trial.trial_info["stage_1"]["prize_coins"]

            SCORE.score += coin_amount
            METER.curr_score = SCORE.score

            data[trial.trial_num] = trial_data


@kesar
def experiment(uid):
    # Reset the experiment state
    SCORE.score = 0
    METER.curr_score = SCORE.score
    data = {"uid": uid}
    Trial.trial_num = 1  # reset trial numbering
    Trial.play_flag_intro = True
    Trial.play_hook_intro = True
    Trial.trigger_highlight = True

    # Begin
    yield start_page()

    # yield from run_training_trial1(data)
    # yield from run_training_trial2(data)
    # yield from run_training_trial3(data)
    # yield from run_training_trial4(data)
    yield from run_testing_trial(data)

    return data
