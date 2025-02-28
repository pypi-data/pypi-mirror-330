"""
This package provides a PsychoPy Builder component that represents an event of a behavioural
experiment.
"""

from pathlib import Path

from psychopy.experiment.components import BaseComponent, Param, _translate

# only use _localized values for label values, nothing functional:
_localized = {"name": _translate("Name")}

_localized.update(
    {
        "custom": _translate("Custom columns"),
        "add_log": _translate("Add to log file"),
    }
)


class BidsBehEventComponent(BaseComponent):
    """
    This class is used for events that do not include the mandatory onset and duration columns.
    Events are, for example, stimuli presented to the participant or participant responses.
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
        name="bidsBehEvent",
        custom="",
        add_log=False,
    ):
        self.type = "BIDSBehEvent"
        self.exp = exp
        self.parentName = parentName
        self.params = {}
        self.depends = []
        super().__init__(exp, parentName, name=name)

        self.exp.requireImport(
            importName="BIDSBehEvent", importFrom="psychopy_bids.bids"
        )

        self.exp.requireImport(importName="BIDSError", importFrom="psychopy_bids.bids")

        _allow3 = ["constant"]

        # Basic params
        self.order += ["custom"]

        hnt = _translate("Add columns as a dictionary")
        self.params["custom"] = Param(
            custom,
            valType="extendedCode",
            inputType="multi",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["custom"],
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
        code = "bids_event = BIDSBehEvent()\n"
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
            code = "logging.log(level=24, msg=dict(bids_event))\n"
            buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(original_indent_level)
