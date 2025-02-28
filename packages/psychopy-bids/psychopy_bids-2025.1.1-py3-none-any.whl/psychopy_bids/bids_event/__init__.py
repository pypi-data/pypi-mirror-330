"""
This package provides a PsychoPy Builder component that represents a BIDS event of an
experiment.
"""

from pathlib import Path
from sys import path as sys_path

from psychopy.experiment.components import BaseComponent, Param, _translate

# Add the plugin directory to path
plugin_dir = Path(__file__).parent
if str(plugin_dir) not in sys_path:
    sys_path.insert(0, str(plugin_dir))

# Define localized labels for UI components
_localized = {
    "name": _translate("Name"),
    "bids_event_type": _translate("BIDS Event Type"),
    "trial_type": _translate("Trial Type"),
    "link_component": _translate("Link Component"),
    "linked_attributes": _translate("Linked Attbributes"),
    "onset": _translate("Onset"),
    "bids_duration": _translate("Duration"),
    "event_type": _translate("Event Type"),
    "sample": _translate("Sample Point"),
    "response_time": _translate("Response Time"),
    "value": _translate("Event Value"),
    "HED": _translate("HED Tags (Sidecar Preferred)"),
    "stim_file": _translate("Stimulus File"),
    "identifier": _translate("Database ID"),
    "database": _translate("Database Reference"),
    "custom": _translate("Custom Columns"),
    "add_log": _translate("Add to log file"),
}


class BidsEventComponent(BaseComponent):
    """
    This class describes timing and other properties of events recorded during a run. Events are,
    for example, stimuli presented to the participant or participant responses.
    """

    categories = ["BIDS"]
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "BIDS.png"
    tooltip = _translate("BIDS Event: Records experiment events in BIDS-valid format")
    plugin = "psychopy-bids"
    log_level_added = False

    def __init__(
        self,
        exp,
        parentName,
        name="bidsEvent",
    ):
        self.type = "BIDSEvent"
        self.exp = exp
        self.parentName = parentName
        self.params = {}
        self.depends = []
        super().__init__(exp, parentName, name=name)

        # Required imports for BIDS events
        required_imports = [
            ("BIDSBehEvent", "psychopy_bids.bids"),
            ("BIDSTaskEvent", "psychopy_bids.bids"),
            ("BIDSError", "psychopy_bids.bids"),
        ]
        for import_name, import_from in required_imports:
            self.exp.requireImport(importName=import_name, importFrom=import_from)

        # Parameter for selecting the type of BIDS event
        hnt = _translate(
            "Choose whether this is a Task-related event (requires onset/duration) or a Behavioral event (timing optional)"
        )
        self.params["bids_event_type"] = Param(
            "TaskEvent",
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=["TaskEvent", "BehEvent"],
            hint=hnt,
            label=_localized["bids_event_type"],
        )

        # Parameter for trial type categorization
        hnt = _translate(
            "Categorical label identifying the experimental condition or trial type. Used to group similar events for analysis."
        )
        self.params["trial_type"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Basic",
            canBePath=False,
            hint=hnt,
            label=_localized["trial_type"],
        )

        # Additional parameters for linking components
        hnt = _translate(
            "Select a PsychoPy component to automatically extract timing and property information"
        )
        self.params["link_component"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Link Component",
            canBePath=False,
            hint=hnt,
            label=_localized["link_component"],
        )

        hnt = _translate(
            "Select which attributes to automatically extract from the linked component"
        )
        self.params["linked_attributes"] = Param(
            [],
            valType="list",
            inputType="multiChoice",
            categ="Link Component",
            updates="constant",
            allowedVals=[
                _localized["onset"],
                _localized["bids_duration"],
                _localized["response_time"],
                _localized["event_type"],
            ],
            hint=hnt,
            label=_localized["linked_attributes"],
        )
        self.depends.append(
            {
                "dependsOn": "link_component",
                "condition": "!=''",
                "param": "linked_attributes",
                "true": "enable",
                "false": "disable",
            }
        )

        # Parameter for overwriting linked values
        hnt = _translate(
            "When enabled, manually entered values will take precedence over automatically extracted values"
        )
        self.params["overwrite_linked"] = Param(
            False,
            valType="bool",
            inputType="bool",
            categ="Link Component",
            hint=hnt,
            label=_translate("Manually set values"),
        )

        # Parameters for event timing
        hnt = _translate(
            "Time in seconds when the event started, measured from the beginning of the recording"
        )
        self.params["onset"] = Param(
            "",
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Link Component",
            hint=hnt,
            label=_localized["onset"],
        )

        hnt = _translate(
            "Length of the event in seconds. Must be zero or positive. Use 'n/a' if duration is unknown."
        )
        self.params["bids_duration"] = Param(
            "",
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Link Component",
            hint=hnt,
            label=_localized["bids_duration"],
        )

        hnt = _translate(
            "Time in seconds between stimulus presentation and participant's response"
        )
        self.params["response_time"] = Param(
            "",
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Link Component",
            hint=hnt,
            label=_localized["response_time"],
        )

        hnt = _translate(
            "Category of stimulus or response (e.g., TextStim, ImageStim, KeyResponse)"
        )
        self.params["event_type"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Link Component",
            canBePath=False,
            hint=hnt,
            label=_localized["event_type"],
        )

        # List of dependent parameters for enabling/disabling based on overwrite_linked
        dependent_params = ["onset", "bids_duration", "response_time", "event_type"]
        for param_name in dependent_params:
            self.depends.append(
                {
                    "dependsOn": "overwrite_linked",
                    "condition": "==True",
                    "param": param_name,
                    "true": "enable",
                    "false": "disable",
                }
            )

        # Stimulus parameters
        hnt = _translate(
            "Path to stimulus file relative to experiment root; recorded in events.tsv and necessary tocopied to BIDS/stimuli folder"
        )
        self.params["stim_file"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            hint=hnt,
            label=_localized["stim_file"],
        )
        hnt = _translate("References within a database")
        self.params["identifier"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            canBePath=False,
            hint=hnt,
            label=_localized["identifier"],
        )
        hnt = _translate("References to a database")
        self.params["database"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            canBePath=False,
            hint=hnt,
            label=_localized["database"],
        )

        # More parameters for additional event details
        hnt = _translate(
            "Onset of the event according to the sampling scheme of the recorded modality (that"
            " is, referring to the raw data file that the events.tsv file accompanies)."
        )
        self.params["sample"] = Param(
            "",
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="More",
            hint=hnt,
            label=_localized["sample"],
        )

        hnt = _translate(
            "Marker value associated with the event (for example, the value of a TTL trigger that"
            " was recorded at the onset of the event)."
        )
        self.params["value"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="More",
            canBePath=False,
            hint=hnt,
            label=_localized["value"],
        )

        hnt = _translate(
            "Define additional columns for the events.tsv file as a Python dictionary: {'column_name': 'value'}"
        )
        self.params["custom"] = Param(
            "",
            valType="extendedCode",
            inputType="multi",
            allowedTypes=[],
            categ="More",
            canBePath=False,
            hint=hnt,
            label=_localized["custom"],
        )

        hnt = _translate(
            "It is strongly advised to use the .json sidecar in the BidsExport instead. "
            "Using HED tags here will disable automated HED tag generation via the sidecar."
        )
        self.params["HED"] = Param(
            "",
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="More",
            canBePath=False,
            hint=hnt,
            label=_localized["HED"],
        )

        # Data params
        hnt = _translate("Include this event's data in the experiment's log file")
        self.params["add_log"] = Param(
            False,
            valType="bool",
            inputType="bool",
            categ="Data",
            hint=hnt,
            label=_translate("Add event to log"),
        )

        # Remove unnecessary inherited parameters
        for parameter in (
            "startType",
            "startVal",
            "startEstim",
            "stopVal",
            "stopType",
            "durationEstim",
            "saveStartStop",
            "syncScreenRefresh",
        ):
            if parameter in self.params:
                del self.params[parameter]

    def writeStartCode(self, buff):
        self.validateBIDSEventParams()
        if self.params["add_log"] and not BidsEventComponent.log_level_added:
            code = "bidsLogLevel = 24\nlogging.addLevel('BIDS', 24)\n"
            buff.writeIndentedLines(code)
            BidsEventComponent.log_level_added = True

    def validateBIDSEventParams(self):
        """
        Validates that required parameters are set and checks if a routine with type 'BIDSexport' exists
        and is included in the experiment flow. Also verifies that if this component is a 'BehEvent',
        the BIDS export routine has its data_type set to 'beh'.
        """
        # 1) Check if a routine with type "BIDSexport" exists in `self.exp.routines`
        bids_export_routine_name = None
        bids_export_routine = None

        for routine_name, routine in self.exp.routines.items():
            if getattr(routine, "type", None) == "BIDSexport":
                bids_export_routine_name = routine_name
                bids_export_routine = routine
                break

        if not bids_export_routine_name:
            raise ValueError(
                f"Component '{self.name}': A routine with type 'BIDSexport' is required. "
                "Please ensure a routine of this type is added to the project."
            )

        # 2) Check if the routine is included in the experiment flow
        routine_in_flow = any(
            getattr(element, "name", None) == bids_export_routine_name
            for element in self.exp.flow
        )
        if not routine_in_flow:
            raise ValueError(
                f"Component '{self.name}': The routine '{bids_export_routine_name}' exists but is not included in the flow. "
                "Please ensure the routine is added to the experiment timeline."
            )

        # 3) If this event is BehEvent, ensure data_type='beh' in BIDSexport
        if self.params["bids_event_type"].val == "BehEvent":
            # Grab the data_type param from the BIDSexport routine
            if "data_type" not in bids_export_routine.params:
                raise ValueError(
                    f"Component '{self.name}': Could not find 'data_type' in the BIDSexport routine '{bids_export_routine_name}'. "
                    "Please make sure it is defined."
                )

            export_data_type = bids_export_routine.params["data_type"].val
            if export_data_type != "beh":
                raise ValueError(
                    f"Component '{self.name}': BIDS event is set to 'BehEvent' but the BIDSexport routine "
                    f"'{bids_export_routine_name}' has data_type='{export_data_type}'. "
                    "This is not valid in BIDS. Please set data_type='beh' on the BIDSexport routine, "
                    "or change the event to a 'TaskEvent'."
                )

        # 4) Check if linked component exists (unchanged from your code)
        linked_component_name = self.params["link_component"].val
        if (
            linked_component_name
            and linked_component_name not in ["", None]
            and self.params["linked_attributes"].val
        ):
            component = self.exp.getComponentFromName(linked_component_name)
            if not hasattr(component, "parentName"):
                raise AttributeError(
                    f"Component '{self.name}': The linked component '{linked_component_name}' "
                    "specified in the link textbox is invalid or does not exist. "
                    "Please ensure the linked component name is correct and refers "
                    "to a valid component in the project."
                )

        # 5) Check if duration and onset is set if taskevent (unchanged from your code)
        if self.params["bids_event_type"].val == "TaskEvent":
            if not self.params["overwrite_linked"]:
                onset_set = False
                duration_set = False
            else:
                onset_set = bool(self.params["onset"].val.strip())
                duration_set = bool(self.params["bids_duration"].val.strip())

            linked_attributes = self.params["linked_attributes"].val
            linked_onset = (
                (_localized["onset"] in linked_attributes)
                if linked_attributes
                else False
            )
            linked_duration = (
                (_localized["bids_duration"] in linked_attributes)
                if linked_attributes
                else False
            )

            # Validate if either manual or linked attributes are set
            if not (onset_set or linked_onset) or not (duration_set or linked_duration):
                raise ValueError(
                    f"Component '{self.name}': When {_localized['bids_event_type']} is set to 'TaskEvent', "
                    f"both {_localized['onset']} and {_localized['bids_duration']} must be provided. "
                    "These values can either be entered manually or linked by ensuring the appropriate "
                    "checkboxes are checked. Please verify your inputs and linked attribute settings."
                )

    def writeRoutineEndCode(self, buff):
        """Write code at the end of the routine."""
        original_indent_level = buff.indentLevel
        params = [
            "trial_type",
            "sample",
            "value",
            "HED",
            "stim_file",
            "identifier",
            "database",
        ]
        if len(self.exp.flow._loopList):
            curr_loop = self.exp.flow._loopList[-1]
        else:
            curr_loop = self.exp._expHandler

        # Determine the function to add data based on loop type
        if "Stair" in curr_loop.type:
            add_data_func = "addOtherData"
        else:
            add_data_func = "addData"

        loop = curr_loop.params["name"]
        name = self.params["name"]

        # Start try block
        code = "try:\n"
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(1, relative=True)

        # Calculate duration if using linked component
        linked_component_name = self.params["link_component"].val
        if (
            linked_component_name
            and linked_component_name not in ["", None]
            and self.params["linked_attributes"].val
        ):
            routine_name = self.exp.getComponentFromName(
                linked_component_name
            ).parentName

            linked_attributes = self.params["linked_attributes"].val
            if _localized["bids_duration"] in linked_attributes:
                code = f"if {linked_component_name}.tStopRefresh is not None:\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(1, relative=True)
                code = f"duration_val = {linked_component_name}.tStopRefresh - {linked_component_name}.tStartRefresh\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(-1, relative=True)
                code = "else:\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(1, relative=True)
                code = f"duration_val = thisExp.thisEntry['{routine_name}.stopped'] - {linked_component_name}.tStartRefresh\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(-1, relative=True)

            if _localized["response_time"] in linked_attributes and self.params[
                "response_time"
            ].val in ["", None]:
                code = f"if hasattr({linked_component_name}, 'rt'):\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(1, relative=True)
                code = f"rt_val = {linked_component_name}.rt\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(-1, relative=True)
                code = "else:\n"
                buff.writeIndentedLines(code)
                buff.setIndentLevel(1, relative=True)
                code = "rt_val = None\n"
                buff.writeIndentedLines(code)
                code = (
                    "logging.warning("
                    f'\'The linked component "{linked_component_name}" does not have a reaction time(.rt) attribute. '
                    "Unable to link BIDS response_time to this component. Please verify the component settings.')\n"
                )
                buff.writeIndentedLines(code)
                buff.setIndentLevel(-1, relative=True)

            # Create BIDS event based on event type
            code = f"bids_event = BIDS{self.params['bids_event_type'].val}(\n"
            buff.writeIndentedLines(code)
            buff.setIndentLevel(1, relative=True)

            code = ""
            if (
                self.params["onset"].val not in ["", None]
                and self.params["overwrite_linked"]
            ):
                code += "onset=%(onset)s,\n"
            elif _localized["onset"] in linked_attributes:
                code += f"onset={linked_component_name}.tStartRefresh,\n"

            if (
                self.params["bids_duration"].val not in ["", None]
                and self.params["overwrite_linked"]
            ):
                code += "duration=%(bids_duration)s,\n"
            elif _localized["bids_duration"] in linked_attributes:
                code += "duration=duration_val,\n"

            if (
                self.params["response_time"].val not in ["", None]
                and self.params["overwrite_linked"]
            ):
                code += "response_time=%(response_time)s,\n"
            elif _localized["response_time"] in linked_attributes:
                code += "response_time=rt_val,\n"

            if (
                self.params["event_type"].val not in ["", None]
                and self.params["overwrite_linked"]
            ):
                code += "event_type=%(event_type)s,\n"
            elif _localized["event_type"] in linked_attributes:
                code += f"event_type=type({linked_component_name}).__name__,\n"
        else:
            # Create BIDS event without linked component
            code = f"bids_event = BIDS{self.params['bids_event_type'].val}(\n"
            buff.writeIndentedLines(code)
            buff.setIndentLevel(1, relative=True)
            code = "onset=%(onset)s,\n"
            code += "duration=%(bids_duration)s,\n"
            code += "response_time=%(response_time)s,\n"
            code += "event_type=%(event_type)s,\n"

        # Add remaining parameters
        for parameter in params:
            if parameter != "bids_event_type" and self.params[parameter] not in [
                "",
                None,
                "None",
            ]:
                code += parameter + "=%(" + parameter + ")s,\n"

        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)
        code = ")\n"
        buff.writeIndentedLines(code)

        # Handle custom parameters
        if custom := self.params["custom"]:
            code = "bids_event.update(%(custom)s)\n"
            buff.writeIndentedLines(code % self.params)

        # Add the event to the handler
        code = "if bids_handler:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "bids_handler.addEvent(bids_event)\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "else:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = f"{loop}.{add_data_func}('{name}.event', bids_event)\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-2, relative=True)

        # Exception handling
        code = "except BIDSError as e:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = 'print(f"An error occurred when creating BIDS event: {e}")\n'
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)

        # add Log
        if self.params["add_log"]:
            code = (
                "logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})"
                "\n"
            )
            buff.writeIndentedLines(code)
        buff.setIndentLevel(original_indent_level)
