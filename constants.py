# image dimensions in pixels
CHEST_BOTTOM_HEIGHT = 145
CHEST_BOTTOM_WIDTH = 485

CHEST_TOP_HEIGHT = 187
CHEST_TOP_WIDTH = 481

COIN_WIDTH = 125
COIN_HEIGHT = 124

FLAG_HEIGHT = 594
FLAG_WIDTH = 594


######################################################################
# Desired image dimensions in vw/vh, while maintaining aspect ratios
######################################################################


# CHEST
DEFAULT_CHEST_WIDTH = "30vw"  # vw
DEFAULT_CHEST_TOP_HEIGHT = (
    f"calc({CHEST_TOP_HEIGHT / CHEST_TOP_WIDTH} * {DEFAULT_CHEST_WIDTH})"  # vw
)


LEFT_CHEST_POSITION_X = f"calc(25vw - {DEFAULT_CHEST_WIDTH} / 2)"  # vw
RIGHT_CHEST_POSITION_X = f"calc(75vw - {DEFAULT_CHEST_WIDTH} / 2)"  # vw
CHEST_TOP_POSITION_Y = "50vh"  # vh
CHEST_BOTTOM_POSITION_Y = (
    f"calc({CHEST_TOP_POSITION_Y} + {DEFAULT_CHEST_TOP_HEIGHT})"
)


# COIN
DEFAULT_COIN_WIDTH = "6vw"  # vw
DEFAULT_COIN_HEIGHT = "6vw"  # vw

LEFT_COIN_POSITION_X = f"calc(25vw - {DEFAULT_COIN_WIDTH}/2"  # vw
RIGHT_COIN_POSITION_X = f"calc(75vw - {DEFAULT_COIN_WIDTH}/2"  # vw
COIN_POSITION_Y = (
    f"calc({CHEST_BOTTOM_POSITION_Y} - {DEFAULT_COIN_HEIGHT}/2)"  # vw
)
LEFT_COIN_POSITION_X = f"calc(25vw - {DEFAULT_COIN_WIDTH}/2)"  # vw
RIGHT_COIN_POSITION_X = f"calc(75vw - {DEFAULT_COIN_WIDTH}/2)"

COIN_INFO = {
    "width": DEFAULT_COIN_WIDTH,
    "height": DEFAULT_COIN_HEIGHT,
}


# FLAG

DEFAULT_FLAG_WIDTH = f"calc({DEFAULT_CHEST_WIDTH}*1.05)"  # vw
DEFAULT_FLAG_HEIGHT = (
    f"calc({FLAG_HEIGHT / FLAG_WIDTH} * {DEFAULT_FLAG_WIDTH})"  # vw
)
FLAG_INFO = {
    "width": FLAG_WIDTH,
    "height": FLAG_HEIGHT,
}
LEFT_FLAG_POSITION_X = f"calc(25vw - {DEFAULT_FLAG_WIDTH}/2)"  # vw
RIGHT_FLAG_POSITION_X = f"calc(75vw - {DEFAULT_FLAG_WIDTH}/2)"  # vw
FLAG_POSITION_Y = (
    f"calc({CHEST_TOP_POSITION_Y} - {DEFAULT_FLAG_HEIGHT}/2.5)"  # vw
)
