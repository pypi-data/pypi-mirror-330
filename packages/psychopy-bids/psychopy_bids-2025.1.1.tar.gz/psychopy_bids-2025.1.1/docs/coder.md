# Psychopy Coder Tutorial

## Getting Started

Psychopy BIDS introduces the _BIDSHandler_ object, the _BIDSBehEvent_ object and the _BIDSTaskEvent_ object. The _BIDSHandler_ handles information about your experiment and writes this information into a valid BIDS dataset. The Event objects hold representations of experimental events that are validated against BIDS. These should be passed on to the BIDSHandler to write your event files.

In the following python code we initiate a BIDS dataset and add a few BIDS events.

We are using seedir to display the directory structure. Install it with:

```bash
pip install seedir
```

```python
import seedir as sd
import pandas as pd

from psychopy_bids.bids import BIDSTaskEvent
from psychopy_bids.bids import BIDSHandler

subject = {"participant_id": "01", "sex": "male", "age": 20}

handler = BIDSHandler(
    dataset="example_dataset",
    subject=subject["participant_id"],
    session="1",
    task="example"
)
handler.createDataset()

start = BIDSTaskEvent(onset=0, duration=0, trial_type="start", text="Let's get started!", color="black")
presentation = BIDSTaskEvent(onset=0.5, duration=5, trial_type="presentation", text="stimulus", color="green")
stop = BIDSTaskEvent(onset=10, duration=0, trial_type="stop", text="We are done!", color="black")

handler.addEvent(start)
handler.addEvent(presentation)
handler.addEvent(stop)

handler.writeEvents(subject,execute_sidecar=False)

sd.seedir("example_dataset")
```

This results in the following directory structure:

```plaintext
example_dataset/
├── .bidsignore
├── CHANGES
├── LICENCE
├── README
├── dataset_description.json
├── participants.json
├── participants.tsv
├── requirements.txt
├── code/
│   └── example_script.py
└── sub-01/
    └── beh/
        └── sub-01_task-task1_run-1_events.tsv
```

The .tsv looks as follows:

|onset|duration|trial_type|
|--|--|--|
|0.0|0|start|
|0.5|5|presentation|
|10.0|0|stop|

In the following tutorial we show how to add these objects to existing experiment code.

## Stroop Task

In this example, we modified an existing Stroop task by adding code to store the output event data according to [BIDS](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/task-events.html). The provided code can be easily integrated into any existing code using PsychoPy and Python.

The underlying experiment was developed by Dennis Wambacher in the course of the seminar Methods of Technical Experiment Control using Python and PsychoPy. Before you begin, please download the base code [here](files/stroop_basecode.py).

### **Step 1:** Creating a BIDS Dataset

To obtain a BIDS dataset directly from the experiment we have to collect the right metadata during the experiment and pass it on to the BIDSHandler to create our dataset.

For this experiment, the participant data is collected from the dialog box. The only required field for BIDS is the participant id. Here we also add participant age and sex.

```py linenums="59"
# Retrieve the Participant Information
participant_info = {"participant_id": v_dialogObj.data[0], "age": v_dialogObj.data[2], "sex": v_dialogObj.data[3]}  
```

Next, we initialize the BIDSHandler. The BIDSHandler requires the dataset name (string input). Additionally, we add participant ID, session, task and data_type. This information is necessary to place the data we will collect in the correct structure. Then we create the dataset from the BIDSHandler. This method checks whether a BIDS dataset with corresponding folder structure and necessary files already exist, and creates it if necessary.

```py linenums="62"
# Create Dataset = Directory structure
bids_example = BIDSHandler(
                dataset="StroopBids",
                subject=participant_info["participant_id"],
                session=v_dialogObj.data[1],
                task="stroopbids",
                data_type="beh" # defines the dataset folder structure, could also be "func"
                )
bids_example.createDataset()
```

Then we initialize an empty list where we'll write our BIDS events before passing it to the BIDSHandler at the end of the experiment.

```py linenums="72"
# Create Event List for the BIDSHandler
events=[]
```

### **Step 2:** Identify all events

Before we start creating the events, we need to define all the events and what information about them is required.

Anything that happens in a participant's environment is part of their cognitive state, even if it is not directly relevant to the research question. To ensure that no events are missed, consider the following: Events that are not part of an experimental design can be things like the presentation of "get ready" before a trial, a fixation cross between stimuli, or feedback. In addition to logging the events themselves, it is important to also log their properties, such as color and position.

The entities identified for our event file are:

[**onset**](https://bids-specification.readthedocs.io/en/stable/glossary.html#onset-columns):
For each event, the start time in seconds must be logged.

[**duration**](https://bids-specification.readthedocs.io/en/stable/glossary.html#duration-columns):
The duration of an event in seconds. In this case, for the instruction and stimuli, the duration is equal to the reaction time. Since the duration of a keystroke (the response) is not measured, it will be marked as "n/a".

**event_role**:
The role of the event in the experiment. In this case, we have instructions, responses, fixations, stimuli, and feedback.

**word**:
Here we describe the presented event in more detail. In this example, we add a description of the instruction, the ''+'' presented as fixation, the word presented, and the specific feedback that was presented.

**color**:
Our stimuli and feedback are presented in different colors, so we append a special column to specify the color in which the event was presented. For consistency, we also add it for the instructions.

**trial_type**:
Our experiments consists of two different types of trials: congruent and incongruent, since the color in which the word is presented is either congruent or incongruent with the presented word. It is important to note that the response and feedback are also part of a trial, as the stimulus, response, and feedback form a unit.

**trial_number**:
We have decided to add numbers to the trials in addition to the trail_type. This is convenient to obtain trial level information later.

**pressed_key**:
The particular key pressed by the participant.

[**response_time**](https://bids-specification.readthedocs.io/en/stable/glossary.html#response_time-columns):
The time taken to respond to a stimulus in seconds.

**response_accuracy**:
Whether the correct response within that trial was given or not.

### **Step 3:** Create the BIDSTaskEvents in Code

Now that we have identified all the events to log in Step 2, we can start adding the BIDSTaskEvents for each event in the code.

BIDSTaskEvents takes the input for an event, i.e. one line in the events.tsv file, and formats it. The minimum required input is the "onset" in seconds (integer or float) and the "duration". As previously stated in Step 2, additional information about an event is necessary. To provide this information, customized columns can be created. Note that custom columns can be named freely but we recommend following [BIDS guidelines](https://bids-specification.readthedocs.io/en/stable/common-principles.html#tabular-files) and use snake case.

We will go through our events in chronological order:

#### 1. **Instruction**

```py linenums="101"
# STEP 3.1: Add the Bids Event Instruction
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=v_reactionTime,
            event_role = "instruction",
            word= "instruction_text",
            color="black",
            pressed_key="space",
            response_time=v_reactionTime
            )
events.append(bids_event)
```

*Note*:  If custom columns do not apply to a specific event, they may be omitted. Psychopy-bids will automatically fill these columns with "n/a".

#### 2. **Response to the Instruction**

```py linenums="113"
# STEP 3.2: Add the Bids Event Response
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"]+v_reactionTime,
            duration = "n/a", # we do not measure the length of the keypress
            event_role = "response",
            pressed_key="space",
            response_time=v_reactionTime
            )
events.append(bids_event)
```

#### 3. **Fixation Cross**

```py linenums="140"
# STEP 3.3: Add the Bids Event Fixation Cross
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=0.5,
            event_role = "fixation",
            word=v_item["Word"],
            color=v_item["Color"]
            )
events.append(bids_event)
```

#### 4. ***Stimulus***
   
```py linenums="194"
# STEP 3.4: Add the Bids Event Stimulus
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=stim_duration,
            trial_type=v_item["Trial"],
            trial_number=v_item["ItemNr"],
            event_role = "stimulus",
            word=v_item["Word"],
            color=v_item["Color"],
            pressed_key=v_keyPress[0],
            response_time=v_reactionTime,
            response_accuracy=v_correct
            )
events.append(bids_event)
```

#### 5. **Response to Stimulus**

If there was a key press.

```py linenums="213"
# STEP 3.5: Add the Bids Event Response
if not v_reactionTime == "n/a":
    bids_event = BIDSTaskEvent(
                onset= onset_dict["onset"] + v_reactionTime,
                duration="n/a", # We don't measure the length of the keypress
                trial_type=v_item["Trial"],
                trial_number=v_item["ItemNr"],
                event_role = "response",
                word=v_item["Word"],
                color=v_item["Color"],
                pressed_key=v_keyPress[0],
                response_time=v_reactionTime,
                response_accuracy=v_correct
                )
    events.append(bids_event)
```

#### 6. **Feedback to Response**

```py linenums="240"
# STEP 3.6: Add the Bids Event Feedback
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=1.0,
            trial_type=v_item["Trial"],
            trial_number=v_item["ItemNr"],
            event_role="feedback",
            word=feedback_text,
            color=feedback_color
            )
events.append(bids_event)
```

#### 7. **Instruction at the End**

```py linenums="269"
# STEP 3.7: Add Bids Event Instruction for the End Screen
bids_event = BIDSTaskEvent(
        onset=onset_dict["onset"],
        duration=onset_dict["onset"]+v_reactionTime,
        event_role = "instruction",
        word="end_text",
        color="black",
        pressed_key="space",
        response_time=v_reactionTime
        )
events.append(bids_event)
```

#### 8. **Response to Instruction**

```py linenums="281"
# STEP 3.8: Add Bids Event Response for the Final Key Press
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"]+v_reactionTime,
            duration = "n/a", #we do not measure the length of the keypress
            event_role = "response",
            pressed_key="space",
            response_time=v_reactionTime
            )
events.append(bids_event)
```

*Note*: To demonstrate the difference in method and output, we retained the csv file of the initial base code to log the events. It is crucial to ensure that the input order for all columns is accurate when using the csv file method. The code lines responsible for generating entries in the csv file could have been removed after the BIDS events were inserted.

### **Step 4:** Add a json sidecar

The events.tsv file should be accompanied by an events.json sidecar that explains the columns in the .tsv file (see [BIDS](https://bids-specification.readthedocs.io/en/stable/common-principles.html#tabular-files)).

We have created a template for the standard input for this experiment, which is then used by psychopy-bids to produce the individual files. The template can be found at the top level of our stroop directory, along with the code.

In our case, the events_template.json file looks like the this:

```json
{
    "onset": {
        "LongName": "",
        "Description": "Onset of the event.",
        "Units": "Seconds"
    },
    "duration": {
        "LongName": "",
        "Description": "Duration of the presented event.",
        "Units": "Seconds"
    },
    "event_role": {
        "LongName": "",
        "Description": "The role of the event in the experiment."
    },
    "word": {
        "LongName": "",
        "Description": "Text of the presented event."
    },
    "color": {
        "LongName": "",
        "Description": "Color of the presented event."
    },
    "pressed_key": {
        "LongName": "",
        "Description": "The pressed response key."
    },
    "trial_type":{
        "LongName": "",
        "Description": "Type of experimental trial for the experimental condition",
        "Levels": {
            "congruent": "Word and color match",
            "incongruent": "Word and color do not match"
        }
    },
    "response_time": {
        "LongName": "",
        "Description": "The response time until a key was pressed after the stimulus onset.",
        "Units": "Seconds"
    },
    "trial_number": {
        "LongName": "",
        "Description": "Number of the trial",
        "Units": "Integers"
    },
    "response_accuracy": {
        "LongName": "",
        "Description": "Whether the correct response to a stimulus was given or not",
        "Levels": {
            "correct": "The correct response was given",
            "wrong": "The wrong response was given",
            "missing": "No response was given"
        }
    }
}
```

To use the template, we set it as an existing file for the BIDSHandler:

```py linenums="297"
#%% STEP 4: Use events_template.json
# Set path to an existing sidecar JSON file (if one exists)
existing_file = "events_template.json"
```

### **Step 5:** Write BIDS events

At the very end of our experiment code (or if we exit the experiment earlier), we pass the participant information and our list of events to the BIDSHandler. This adds the events.tsv file and the participant file entry. We also create the events.json sidecar file with the template of step 4.

```py linenums="301"
#%% STEP 5: Save the Event File and Close
bids_example.addEvent(events)
bids_example.writeEvents(participant_info)
```

### **Step 6:** Check final Stroop task with added BIDS events, run experiment and check output

After implementing all the steps discussed in the base code, the final code should resemble this:

```py linenums="1"
import os
import psychopy
from psychopy import visual, core, logging, event, gui, data
from psychopy_bids.bids import BIDSHandler, BIDSTaskEvent

# Simple true/false Stroop Task based on Code by Dennis Wambacher

# In a Stroop Task, color names are presented in different colors.
# The participant must decide whether the color name and the color in which it is displayed match
# by pressing the left (mismatch) and right (match) arrow keys.

#%% Set up paths

# Change Working Directory to Current File
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a Folder Named Data to Save the log File in
if not os.path.isdir("data"):
    os.makedirs("data")

#%% Create Events
# Item Inventory / Item Dictionary with Nr., Word, Color, Correct Answer, and Trial Type.
v_itemDict = [
    {"ItemNr": 1, "Word": "Red", "Color": "green", "CorrAnsw": "left", "Trial": "incongruent"},
    {"ItemNr": 2, "Word": "Blue", "Color": "blue", "CorrAnsw": "right", "Trial": "congruent"},
    {"ItemNr": 3, "Word": "Red", "Color": "red", "CorrAnsw": "right", "Trial": "congruent"},
    {"ItemNr": 4, "Word": "Green", "Color": "blue", "CorrAnsw": "left", "Trial": "incongruent"},
    {"ItemNr": 5, "Word": "Red", "Color": "red", "CorrAnsw": "right", "Trial": "congruent"},
    {"ItemNr": 6, "Word": "Blue", "Color": "red", "CorrAnsw": "left", "Trial": "incongruent"},
    {"ItemNr": 7, "Word": "Green", "Color": "red", "CorrAnsw": "left", "Trial": "incongruent"},
    {"ItemNr": 8, "Word": "Green", "Color": "green", "CorrAnsw": "right", "Trial": "congruent"},
    {"ItemNr": 9, "Word": "Blue", "Color": "blue", "CorrAnsw": "right", "Trial": "congruent"},
]

# Variables for Instruction Text and End Text
v_instrText = "Press the left arrow key if the word and color don't match."
v_instrText += "\n\nPress the right arrow key if the word and color match."
v_instrText += "\n\n\nPress space to start the experiment"

v_finishText = "Thank you for your participation.\n\n\n"
v_finishText += "Press space to end the experiment and close the program"

#%% Get Your Participant Information

# Creating a Dialog Object for Participant Info and Check for Ok
personal_info = {"Participant Code": "", "Session": "", "Age": "", "Sex": ["", "f", "m", "d"]}
v_dialogObj = gui.DlgFromDict(personal_info, title = "StroopBids: Personal Info", order = ["Participant Code", "Session", "Age", "Sex"])   

# Create csv File as log File
if v_dialogObj.OK:
    v_logFileName = "data/%s_%s.csv" % (v_dialogObj.data[0],v_dialogObj.data[1]) 
    v_logFileObj = logging.LogFile(f=v_logFileName, filemode="w")
    # Write the column labels into the log file
    v_logFileObj.write("onset;duration;event_role;word;color;pressed_key;trial_type;response_time;trial_number;response_accuracy\n")
else:
    core.quit()

#%% STEP 1: Create Bids Dataset
# Retrieve the Participant Information
participant_info = {"participant_id": v_dialogObj.data[0], "age": v_dialogObj.data[2], "sex": v_dialogObj.data[3]} 

# Create Dataset = Directory structure
bids_example = BIDSHandler(
                dataset="StroopBids",
                subject=v_dialogObj.data[0],
                session=v_dialogObj.data[1],
                task="stroopbids",
                data_type="beh" # defines the dataset directory structure, could also be "func"
                )
bids_example.createDataset()

# Create Event List for the BIDSHandler
events=[]

#%% Create Objects for Experiment Presentation
# Create a Window for the Text
v_winObj = visual.Window(size=[2560, 1080], color="white", fullscr=True)
v_textObj = visual.TextStim(v_winObj, text="", color="black")

# Create Onset Dictionary for Getting Exact Timings
onset_dict =dict.fromkeys(["onset", "event_onset"])

# Create a Clock for the Response Times
v_reactionClock = core.Clock()

# Create a Cursor(Mouse)-Object to Turn it Invisible During the Experiment
v_mouseObj = event.Mouse(v_winObj)
v_mouseObj.setVisible(False)

#%% Start Experiment Presentation
# Show Instructions until Key Press
v_textObj.setText(v_instrText)
v_textObj.setHeight(0.06)
v_textObj.draw()
v_winObj.timeOnFlip(onset_dict, "onset") # get exact time of presentation
v_winObj.flip()
v_reactionClock.reset() # reset reaction clock to get the time difference between stimulus and response
event.waitKeys(keyList=["space"])
v_reactionTime = v_reactionClock.getTime()

# STEP 3.1: Add the Bids Event Instruction
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=v_reactionTime,
            event_role = "instruction",
            word= "instruction_text",
            color="black",
            pressed_key="space",
            response_time=v_reactionTime,
            )
events.append(bids_event)

# STEP 3.2: Add the Bids Event Response
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"]+v_reactionTime,
            duration = "n/a", # we do not measure the length of the keypress
            event_role = "response",
            pressed_key="space",
            response_time=v_reactionTime,
            )
events.append(bids_event)

# Write the Instruction into the csv File
v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                   %(onset_dict["onset"],v_reactionTime,"instruction","instruction_text","black","space","n/a",v_reactionTime,"n/a","n/a"))
# Write the Response into the csv File
v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                   %(onset_dict["onset"]+v_reactionTime,"n/a","response","n/a","n/a","space","n/a",v_reactionTime,"n/a","n/a"))

#%% The experiment loop
for v_item in v_itemDict:
    # A Fixation Cross for 0.5 Seconds
    v_textObj.setText("+")
    v_textObj.setColor("black")
    v_textObj.setHeight(0.3)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    core.wait(0.5)
    # STEP 3.3: Add the Bids Event Fixation Cross
    bids_event = BIDSTaskEvent(
                onset=onset_dict["onset"],
                duration=0.5,
                event_role = "fixation",
                word=v_item["Word"],
                color=v_item["Color"],
                )
    events.append(bids_event)

    # Write the Fixation into the csv File
    v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                    %(onset_dict["onset"],0.5,"fixation","n/a","n/a","n/a","n/a","n/a","n/a","n/a"))

    # Present the Stimulus Word
    v_textObj.setText(v_item["Word"])
    v_textObj.setColor(v_item["Color"])
    v_textObj.setHeight(0.2)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    v_reactionClock.reset()

    # Wait 1 Seconds for a Key Press
    v_keyPress = event.waitKeys(maxWait=1.0, keyList=["left", "right", "escape"])
    v_reactionTime = v_reactionClock.getTime()

    # Get the Key and its Correctness
    if v_keyPress:
        stim_duration = v_reactionTime
        if v_keyPress[0] == "escape":
            v_winObj.close()
            # Store the Event File before Quitting
            bids_example.addEvent(events)
            bids_example.writeEvents(participant_info)
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

    # STEP 3.4: Add the Bids Event Stimulus
    bids_event = BIDSTaskEvent(
                onset=onset_dict["onset"],
                duration=stim_duration,
                trial_type=v_item["Trial"],
                trial_number=v_item["ItemNr"],
                event_role = "stimulus",
                word=v_item["Word"],
                color=v_item["Color"],
                pressed_key=v_keyPress[0],
                response_time=v_reactionTime,
                response_accuracy=v_correct
                )
    events.append(bids_event)

    # Write the Stimulus into the csv File
    v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                    %(onset_dict["onset"],stim_duration,"stimulus",v_item["Word"],v_item["Color"],v_keyPress[0],v_item["Trial"],v_reactionTime,v_item["ItemNr"],v_correct))

    # STEP 3.5: Add the Bids Event Response
    if not v_reactionTime == "n/a":
        bids_event = BIDSTaskEvent(
                    onset= onset_dict["onset"] + v_reactionTime,
                    duration="n/a", # We don't measure the length of the keypress
                    trial_type=v_item["Trial"],
                    trial_number=v_item["ItemNr"],
                    event_role = "response",
                    word=v_item["Word"],
                    color=v_item["Color"],
                    pressed_key=v_keyPress[0],
                    response_time=v_reactionTime,
                    response_accuracy=v_correct
                    )
        events.append(bids_event)
        # Write the Response into the csv File
        v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                        %(onset_dict["onset"]+v_reactionTime,"n/a","response",v_item["Word"],v_item["Color"],v_keyPress[0],v_item["Trial"],v_reactionTime,v_item["ItemNr"],v_correct))

    # Display the Feedback for 1 Second
    v_textObj.setText(feedback_text)
    v_textObj.setColor(feedback_color)
    v_textObj.draw()
    v_winObj.timeOnFlip(onset_dict, "onset")
    v_winObj.flip()
    core.wait(1.0)

    # STEP 3.6: Add the Bids Event Feedback
    bids_event = BIDSTaskEvent(
                onset=onset_dict["onset"],
                duration=1.0,
                trial_type=v_item["Trial"],
                trial_number=v_item["ItemNr"],
                event_role="feedback",
                word=feedback_text,
                color=feedback_color
                )
    events.append(bids_event)
    # Write the Feedback into the csv File
    v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                    %(onset_dict["onset"],1.0,"feedback",feedback_text,feedback_color,"n/a",v_item["Trial"],"n/a",v_item["ItemNr"],"n/a"))

#%% End the Experiment
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

# STEP 3.7: Add Bids Event Instruction for the End Screen
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"],
            duration=onset_dict["onset"]+v_reactionTime,
            event_role = "instruction",
            word="end_text",
            color="black",
            pressed_key="space",
            response_time=v_reactionTime,
            )
events.append(bids_event)

# STEP 3.8: Add Bids Event Response for the Final Key Press
bids_event = BIDSTaskEvent(
            onset=onset_dict["onset"]+v_reactionTime,
            duration = "n/a", #we do not measure the length of the keypress
            event_role = "response",
            pressed_key="space",
            response_time=v_reactionTime,
            )
events.append(bids_event)
# Write the Instruction into the csv File
v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                   %(onset_dict["onset"],v_reactionTime,"instruction","end_text","black","space","n/a",v_reactionTime,"n/a","n/a"))
# Write the Response into the csv File
v_logFileObj.write("%f;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                   %(onset_dict["onset"]+v_reactionTime,"n/a","response","n/a","n/a","space","n/a",v_reactionTime,"n/a","n/a"))

#%% STEP 4: Use events_template.json
# Set path to an existing sidecar JSON file (if one exists)
existing_file = "events_template.json"

#%% STEP 5: Save the Event File and Close
bids_example.addEvent(events)

bids_example.writeEvents(participant_info, execute_sidecar=existing_file)

# You can write a requirements.txt
bids_example.addEnvironment()

core.quit()
```

Once the experiment has been run for the first time, the folder structure and events file should resemble the following:

```plaintext
stroop/
├── stroop.py
├── events_template.json
├── data/
│   └── 1_1.csv
└── StroopBids/
    │   └── sub-1/
    │       └── ses-1/
    │           └── beh/
    │               └── sub-1_ses-1_task-stroopbids_run-1_events.tsv
    ├── participants.tsv
    ├── participants.json
    ├── dataset_description.json
    ├── task-stroopbids_events.json
    ├── README
    ├── LICENCE
    ├── CHANGES
    ├── requirements.txt
    └── .bidsignore
```

| onset | duration | event_role | word | color | pressed_key | trial_type | response_time | trial_number | response_accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 15.2876 | 1.2295 | instruction | instruction_text | black | space | n/a | 1.2295 | n/a | n/a |
| 16.5171 | n/a | response | n/a | n/a | space | n/a | 1.2295 | n/a | n/a |
| 16.538 | 0.5 | fixation | +  | black | n/a | n/a | n/a | n/a | n/a |
| 17.0593 | 0.8105 | stimulus | Red | green | left | incongruent | 0.8105 | 1.0 | correct |
| 17.8698 | n/a | response | Red | green | left | incongruent | 0.8105 | 1.0 | correct |
| 17.8972 | 1.0 | feedback | Correct! | green | n/a | incongruent | n/a | 1.0 | n/a |
| 18.9272  | 0.5 | fixation | + | black | n/a | n/a | n/a | n/a | n/a |

The tutorial code and a sample dataset for illustrative purposes are available for download [here](files/stroop_coder.zip).
