import os

import psychopy
from psychopy import core, data, event, gui, logging, visual

# Simple true/false Stroop-Task based on Code by Dennis Wambacher

# In a Stroop-Task Color-Names are presented in different colors.
# The participant shall decide whether the Color-Name and the color in which it is presented match,
# by pressing the left (not) and right (matching) arrow keys.

# %% Set up paths

# Change Working Directory to Current File
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a Folder Named Data to Save the log File in
if not os.path.isdir("data"):
    os.makedirs("data")

# %% Create events
# Item Inventory / Item Dictionary with Nr. Word. Color. Correct Answer. and Trial Type.
v_itemDict = [
    {
        "ItemNr": 1,
        "Word": "Red",
        "Color": "green",
        "CorrAnsw": "left",
        "Trial": "incongruent",
    },
    {
        "ItemNr": 2,
        "Word": "Blue",
        "Color": "blue",
        "CorrAnsw": "right",
        "Trial": "congruent",
    },
    {
        "ItemNr": 3,
        "Word": "Red",
        "Color": "red",
        "CorrAnsw": "right",
        "Trial": "congruent",
    },
    {
        "ItemNr": 4,
        "Word": "Green",
        "Color": "blue",
        "CorrAnsw": "left",
        "Trial": "incongruent",
    },
    {
        "ItemNr": 5,
        "Word": "Red",
        "Color": "red",
        "CorrAnsw": "right",
        "Trial": "congruent",
    },
    {
        "ItemNr": 6,
        "Word": "Blue",
        "Color": "red",
        "CorrAnsw": "left",
        "Trial": "incongruent",
    },
    {
        "ItemNr": 7,
        "Word": "Green",
        "Color": "red",
        "CorrAnsw": "left",
        "Trial": "incongruent",
    },
    {
        "ItemNr": 8,
        "Word": "Green",
        "Color": "green",
        "CorrAnsw": "right",
        "Trial": "congruent",
    },
    {
        "ItemNr": 9,
        "Word": "Blue",
        "Color": "blue",
        "CorrAnsw": "right",
        "Trial": "congruent",
    },
]

# Variables for Instruction Text and End Text
v_instrText = "Press the left arrow key if the word and color don't match."
v_instrText += "\n\nPress the right arrow key if the word and color match."
v_instrText += "\n\n\nPress space to start the experiment"

v_finishText = "Thank you for your participation.\n\n\n"
v_finishText += "Press space to end the experiment and close the program"

# %% Get Your Participant Information

# Creating a Dialog Object for Participant Info and Check for Ok
personal_info = {
    "Participant Code": "",
    "Session": "",
    "Age": "",
    "Sex": ["", "f", "m", "d"],
}
v_dialogObj = gui.DlgFromDict(
    personal_info,
    title="StroopBids: Personal Info",
    order=["Participant Code", "Session", "Age", "Sex"],
)

# Create csv File as log File
if v_dialogObj.OK:
    v_logFileName = "data/%s/%s.csv" % (v_dialogObj.data[0], v_dialogObj.data[1])
    v_logFileObj = logging.LogFile(f=v_logFileName, filemode="w")
    # Write the column labels into the log file
    v_logFileObj.write(
        "onset;duration;event_type;word;color;pressed_key;trial_type;response_time;trial_number;response_accuracy\n"
    )
else:
    core.quit()

# %% Create Objects for Experiment Presentation

# Create a Window for the Text
v_winObj = visual.Window(size=[2560, 1080], color="white", fullscr=True)
v_textObj = visual.TextStim(v_winObj, text="", color="black")

# Create Onset Dictionary for Getting Exact Timings
onset_dict = dict.fromkeys(["onset", "event_onset"])

# Create a Clock for the Response Times
v_reactionClock = core.Clock()

# Create a Cursor(Mouse)-Object to Turn it Invisible During the Experiment
v_mouseObj = event.Mouse(v_winObj)
v_mouseObj.setVisible(False)

# %% Start Experiment Presentation

# Show Instructions until Button Press
v_textObj.setText(v_instrText)
v_textObj.setHeight(0.06)
v_textObj.draw()
v_winObj.timeOnFlip(onset_dict, "onset")  # get exact time of presentation
v_winObj.flip()
v_reactionClock.reset()  # reset reaction clock to get the time difference between stimulus and response
event.waitKeys(keyList=["space"])
v_reactionTime = v_reactionClock.getTime()

# Write the Instruction into the csv File
v_logFileObj.write(
    "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    % (
        onset_dict["onset"],
        v_reactionTime,
        "instruction",
        "instruction_text",
        "black",
        "space",
        "n/a",
        v_reactionTime,
        "n/a",
        "n/a",
    )
)
# Write the Response into the csv File
v_logFileObj.write(
    "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    % (
        onset_dict["onset"] + v_reactionTime,
        "n/a",
        "response",
        "n/a",
        "n/a",
        "space",
        "n/a",
        v_reactionTime,
        "n/a",
        "n/a",
    )
)

# %% The experiment loop
for v_item in v_itemDict:
    # A Fixation Cross for 0.5 Seconds
    v_textObj.setText("+")
    v_textObj.setColor("black")
    v_textObj.setHeight(0.3)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    core.wait(0.5)

    # Write the Fixation into the csv File
    v_logFileObj.write(
        "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
        % (
            onset_dict["onset"],
            0.5,
            "fixation",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
        )
    )

    # Present the Stimulus Word
    v_textObj.setText(v_item["Word"])
    v_textObj.setColor(v_item["Color"])
    v_textObj.setHeight(0.2)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    v_reactionClock.reset()

    # Wait 1 Seconds for a Button Press
    v_keyPress = event.waitKeys(maxWait=1.0, keyList=["left", "right", "escape"])
    v_reactionTime = v_reactionClock.getTime()

    # Get the Key and its Correctness
    if v_keyPress:
        stim_duration = v_reactionTime
        if v_keyPress[0] == "escape":
            v_winObj.close()
            core.quit()
        elif v_keyPress[0] == v_item["CorrAnsw"]:
            v_correct = "correct"
            feedback_text = "Correct!"
            feedback_color = "green"
        else:
            v_correct = "wrong"
            feedback_text = "Wrong!"
            feedback_color = "red"
    else:
        stim_duration = 1.0
        feedback_text = "Too Slow!"
        feedback_color = "orange"
        v_correct = "missing"
        v_reactionTime = "n/a"
        v_keyPress = ["none"]

    # Write the Stimulus into the csv File
    v_logFileObj.write(
        "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
        % (
            onset_dict["onset"],
            stim_duration,
            "stimulus",
            v_item["Word"],
            v_item["Color"],
            v_keyPress[0],
            v_item["Trial"],
            v_reactionTime,
            v_item["ItemNr"],
            v_correct,
        )
    )
    if not v_reactionTime == "n/a":
        # Write the Response into the csv File
        v_logFileObj.write(
            "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
            % (
                onset_dict["onset"] + v_reactionTime,
                "n/a",
                "response",
                v_item["Word"],
                v_item["Color"],
                v_keyPress[0],
                v_item["Trial"],
                v_reactionTime,
                v_item["ItemNr"],
                v_correct,
            )
        )

    # Display the Feedback for 1 Second
    v_textObj.setText(feedback_text)
    v_textObj.setColor(feedback_color)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    core.wait(1.0)
    # Write the Feedback into the csv File
    v_logFileObj.write(
        "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
        % (
            onset_dict["onset"],
            1.0,
            "feedback",
            feedback_text,
            feedback_color,
            "n/a",
            v_item["Trial"],
            "n/a",
            v_item["ItemNr"],
            "n/a",
        )
    )

# %% End the Experiment
# Show the End Text
v_textObj.setText(v_finishText)
v_textObj.setColor("black")
v_textObj.setHeight(0.06)
v_textObj.draw()
v_winObj.timeOnFlip(onset_dict, "onset")
v_winObj.flip()
v_reactionClock.reset()
event.waitKeys(keyList=["space"])
v_reactionTime = v_reactionClock.getTime()
# Close Presentation Window
v_winObj.close()

# Write the Instruction into the csv File
v_logFileObj.write(
    "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    % (
        onset_dict["onset"],
        v_reactionTime,
        "instruction",
        "end_text",
        "black",
        "space",
        "n/a",
        v_reactionTime,
        "n/a",
        "n/a",
    )
)
# Write the Response into the csv File
v_logFileObj.write(
    "%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    % (
        onset_dict["onset"] + v_reactionTime,
        "n/a",
        "response",
        "n/a",
        "n/a",
        "space",
        "n/a",
        v_reactionTime,
        "n/a",
        "n/a",
    )
)

core.quit()
