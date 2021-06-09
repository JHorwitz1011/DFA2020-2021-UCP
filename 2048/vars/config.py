import vars.constants as c
from collections import deque

# Saving
color = 'blue'               # stores current tracking color value. defaults to blue

# Scoring
currentScore = 0             # changed after runtime
highScore = 0                # changed after runtime

# Color Tracking
colorUpper = (0,0,0)         # upper bound for color tracking
colorLower = (0,0,0)         # lower bound for color tracking
threshold = 150              # color threshold
cooldown = 0                 # cooldown variable to ignore similar inputs after a certain amount of time
pts = deque(maxlen=c.maxlen) # queue to hold the locations of previous tracks to draw the line
last_input = False           # tracks last input (ex left, right, up, down)

# GUI manipulation
wrapper = None               # pointer for the wrapper object - needs to be accessed over multiple files.

# Recalibration
recalibrate = False

# pause/play state
tracking_enabled = True