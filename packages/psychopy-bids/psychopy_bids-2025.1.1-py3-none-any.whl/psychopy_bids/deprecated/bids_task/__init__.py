"""
This package provides a PsychoPy Builder component that represents a task event of an
experiment.
"""

from pathlib import Path

from psychopy.experiment.components import BaseComponent, Param, _translate

# only use _localized values for label values, nothing functional:
_localized = {"name": _translate("Name")}

_localized.update(
    {
        "onset": _translate("Onset"),
        "bids_duration": _translate("Duration"),
        "trial_type": _translate("Trial type"),
        "sample": _translate("Sample"),
        "response_time": _translate("Response time"),
        "value": _translate("Value"),
        "hed": _translate("HED"),
        "stim_file": _translate("Stimulus file"),
        "identifier": _translate("Identifier"),
        "database": _translate("Database"),
        "custom": _translate("Custom columns"),
        "add_log": _translate("Add to log file"),
    }
)


class BidsTaskEventComponent(BaseComponent):
    """
    This class describes timing and other properties of events recorded during a run. Events are,
    for example, stimuli presented to the participant or participant responses.
    """

    categories = ["BIDS"]
    targets = ["PsychoPy"]
    hidden = True
    plugin = "psychopy-bids"
    iconFile = Path(__file__).parent / "BIDS.png"

    def __init__(
        self,
        exp,
        parentName,
        name="bidsEvent",
        onset=0,
        bids_duration=1,
        trial_type=None,
        sample=None,
        response_time=None,
        value=None,
        hed=None,
        stim_file=None,
        identifier=None,
        database=None,
        custom="",
        add_log=False,
    ):
        self.type = "BIDSTaskEvent"
        self.exp = exp
        self.parentName = parentName
        self.params = {}
        self.depends = []
        super().__init__(exp, parentName, name=name)

        self.exp.requireImport(
            importName="BIDSBehEvent", importFrom="psychopy_bids.bids"
        )
        self.exp.requireImport(
            importName="BIDSTaskEvent", importFrom="psychopy_bids.bids"
        )

        self.exp.requireImport(importName="BIDSError", importFrom="psychopy_bids.bids")

        self.exp.requireImport(importName="literal_eval", importFrom="ast")

        _allow3 = ["constant"]

        # Basic params
        self.order += ["onset", "bids_duration", "trial_type", "response_time"]

        hnt = _translate(
            "Onset (in seconds) of the event, measured from the beginning of the acquisition of"
            " the first data point stored in the corresponding task data file."
        )
        self.params["onset"] = Param(
            onset,
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized["onset"],
        )
        hnt = _translate(
            "Duration of the event (measured from onset) in seconds. Must always be either zero or"
            " positive (or n/a if unavailable)."
        )
        self.params["bids_duration"] = Param(
            bids_duration,
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized["bids_duration"],
        )
        hnt = _translate(
            "Primary categorisation of each trial to identify them as instances of the"
            " experimental conditions."
        )
        self.params["trial_type"] = Param(
            trial_type,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["trial_type"],
        )
        hnt = _translate("Response time measured in seconds.")
        self.params["response_time"] = Param(
            response_time,
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized["response_time"],
        )

        # Data params
        hnt = _translate("Should the event be saved in the log file too?")
        self.params["add_log"] = Param(
            add_log,
            valType="bool",
            inputType="bool",
            categ="Data",
            hint=hnt,
            label=_translate("Add event to log"),
        )

        # Stim params
        self.order += ["stim_file", "identifier", "database"]

        hnt = _translate(
            "Indicates the location of the stimulus file. The values represent a path relative to"
            " the /stimuli directory. Paths that include the stimuli/ prefix will also be correctly"
            " interpreted by removing the redundant prefix, ensuring proper placement within"
            " the /stimuli directory."
        )
        self.params["stim_file"] = Param(
            stim_file,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            updates="constant",
            allowedUpdates=_allow3[:],
            hint=hnt,
            label=_localized["stim_file"],
        )
        hnt = _translate("References within a database")
        self.params["identifier"] = Param(
            identifier,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["identifier"],
        )
        hnt = _translate("References to a database")
        self.params["database"] = Param(
            database,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="Stim",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["database"],
        )

        # more params
        self.order += ["sample", "value", "hed", "custom"]

        hnt = _translate(
            "Onset of the event according to the sampling scheme of the recorded modality (that"
            " is, referring to the raw data file that the events.tsv file accompanies)."
        )
        self.params["sample"] = Param(
            sample,
            valType="num",
            inputType="single",
            allowedTypes=[],
            categ="More",
            updates="constant",
            allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized["sample"],
        )
        hnt = _translate(
            "Marker value associated with the event (for example, the value of a TTL trigger that"
            " was recorded at the onset of the event)."
        )
        self.params["value"] = Param(
            value,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="More",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["value"],
        )
        hnt = _translate("Hierarchical Event Descriptor (HED) Tag")
        self.params["hed"] = Param(
            hed,
            valType="str",
            inputType="single",
            allowedTypes=[],
            categ="More",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["hed"],
        )
        hnt = _translate("Add additional columns as a dictionary")
        self.params["custom"] = Param(
            custom,
            valType="extendedCode",
            inputType="multi",
            allowedTypes=[],
            categ="More",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["custom"],
        )

        # these inherited params are harmless but might as well trim:
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
        """Write code at the beginning of the experiment."""
        code = "bidsLogLevel = 24\nlogging.addLevel('BIDS', 24)\n"
        if self.params["add_log"]:
            buff.writeIndentedLines(code)

    def writeRoutineEndCode(self, buff):
        """Write code at the end of the routine."""
        original_indent_level = buff.indentLevel
        inits = self.params

        params = [
            "trial_type",
            "sample",
            "response_time",
            "value",
            "hed",
            "stim_file",
            "identifier",
            "database",
        ]
        if len(self.exp.flow._loopList):
            curr_loop = self.exp.flow._loopList[-1]
        else:
            curr_loop = self.exp._expHandler

        if "Stair" in curr_loop.type:
            add_data_func = "addOtherData"
        else:
            add_data_func = "addData"

        loop = curr_loop.params["name"]
        name = self.params["name"]
        code = "try:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "bids_event = BIDSTaskEvent(\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "onset=%(onset)s,\n"
        for parameter in params:
            if inits[parameter] != "None":
                code += parameter + "=%(" + parameter + ")s,\n"
        code += "duration=%(bids_duration)s"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = ")\n"
        buff.writeIndentedLines(code % inits)
        custom = self.params["custom"]

        if custom:
            code = "bids_event.update(%(custom)s)\n"
            buff.writeIndentedLines(code % inits)
        code = "if bids_handler:"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "bids_handler.addEvent(bids_event)"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "else:"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = f"{loop}.{add_data_func}('{name}.event', bids_event)\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-2, relative=True)
        code = "except BIDSError:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "pass\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        if self.params["add_log"]:
            code = (
                "logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})"
                "\n"
            )
            buff.writeIndentedLines(code % inits)

        buff.setIndentLevel(original_indent_level)
