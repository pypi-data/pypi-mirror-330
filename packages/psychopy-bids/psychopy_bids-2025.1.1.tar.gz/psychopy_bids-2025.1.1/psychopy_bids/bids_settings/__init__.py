"""
PsychoPy routine to support the creation of valid bids-datasets.
"""

from pathlib import Path
from sys import path as sys_path

from psychopy.experiment import Param
from psychopy.experiment.routines._base import BaseStandaloneRoutine
from psychopy.localization import _translate

plugin_dir = Path(__file__).parent
if str(plugin_dir) not in sys_path:
    sys_path.insert(0, str(plugin_dir))

_localized = {
    "path": _translate("Path"),
    "runs": _translate("Add runs to event file name"),
    "dataset_description": _translate("Dataset Description"),
}


class BidsExportRoutine(BaseStandaloneRoutine):
    """
    This class provides methods for creating and managing BIDS datasets and their modality agnostic
    files plus modality specific files.
    """

    categories = ["BIDS"]
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "BIDS.png"
    tooltip = _translate(
        "BIDS Export: Creates a standardized BIDS directory structure and generates "
        "required metadata files according to BIDS specifications"
    )
    plugin = "psychopy-bids"

    def __init__(self, exp, name="bidsExport"):
        BaseStandaloneRoutine.__init__(self, exp, name=name)

        self.exp.requireImport(
            importName="BIDSHandler", importFrom="psychopy_bids.bids"
        )

        self.type = "BIDSexport"

        self.params["name"].hint = _translate("Name of the Routine.")
        self.params["name"].label = _translate("Routine Name")

        hnt = _translate(
            "Root name of the dataset (parent folder name) if this task is part of "
            "a larger experiment"
        )
        self.params["dataset_name"] = Param(
            "bids",
            valType="str",
            inputType="single",
            categ="Basic",
            allowedTypes=[],
            canBePath=False,
            hint=hnt,
            label=_translate("Dataset Name"),
        )

        # license
        hnt = _translate("License of the dataset")
        self.params["bids_license"] = Param(
            "",
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "",
                "CC0-1.0",
                "CC-BY-4.0",
                "CC-BY-SA-4.0",
                "CC-BY-ND-4.0",
                "CC-BY-NC-4.0",
                "CC-BY-NC-SA-4.0",
                "CC-BY-NC-ND-4.0",
                "ODC-By-1.0",
                "ODbL-1.0",
                "PDDL-1.0",
            ],
            hint=hnt,
            label=_translate("Dataset License"),
        )

        hnt = _translate("BIDS defined data type")
        self.params["data_type"] = Param(
            "beh",
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "beh",
                "eeg",
                "func",
                "ieeg",
                "nirs",
                "meg",
                "motion",
                "mrs",
                "pet",
            ],
            hint=hnt,
            label=_translate("Data Type"),
        )

        hnt = _translate(
            "Optional label to distinguish between different acquisition parameters "
            "or conditions across multiple runs of the same task"
        )
        self.params["acq"] = Param(
            "",
            valType="str",
            inputType="single",
            categ="Basic",
            allowedVals=[],
            canBePath=False,
            hint=hnt,
            label=_translate("Acquisition Label"),
        )

        # Params for dataset description
        hnt = _translate(
            "Path to a dataset_description.json. If not provided, "
            "a default template will be used. Specifying a file will overwrite any "
            "existing dataset_description.json"
        )
        self.params["dataset_description"] = Param(
            "",
            valType="str",
            inputType="file",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=["constant"],
            hint=hnt,
            label=_translate("Dataset Description"),
        )

        # Params for json_sidecar
        hnt = _translate(
            "Path to the events/beh sidecar file. Accepts a complete .json sidecar or a 4-column spreadsheet "
            "in CSV, TSV, or XLSX format (only for HED tags). "
            "Spreadsheet files must adhere to the BIDS 4-column format. "
            "If not specified, a default template is used. Existing sidecars will be updated during execution."
        )
        self.params["json_sidecar"] = Param(
            "",
            valType="str",
            inputType="file",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=["constant"],
            hint=hnt,
            label=_translate("Events/Beh Sidecar"),
        )

        hnt = _translate(
            "Generate preliminary HED metadata from the events file; may not fully comply with BIDS standards."
        )
        self.params["generate_hed_metadata"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Generate HED Metadata"),
        )

        hnt = _translate(
            "Copy all stimulus files referenced in the events file to the BIDS dataset's /stimuli directory"
        )
        self.params["add_stimuli"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Include Stimuli"),
        )

        hnt = _translate(
            "Include experiment files (lastrun.py and .psyexp) in the BIDS dataset's /code directory"
        )
        self.params["add_code"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Include Source Code"),
        )

        hnt = _translate(
            "Generate and include requirements.txt with Python and package versions in the BIDS dataset"
        )
        self.params["add_environment"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Include Dependencies"),
        )

        # runs params
        hnt = _translate(
            "Include run numbers in event filenames for multi-run experiments"
        )
        self.params["runs"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Add Run Numbers"),
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
        original_indent_level = buff.indentLevel

        # Create the initial folder structure
        code = "if expInfo['session']:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(dataset_name)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " session=expInfo['session'], data_type=%(data_type)s, acq=%(acq)s,\n"
            " runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)

        # Handle case where session is not provided
        code = "else:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(dataset_name)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " data_type=%(data_type)s, acq=%(acq)s, runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)

        # Initialize dataset and add license
        code = "bids_handler.createDataset()\n"
        if self.params["bids_license"] not in ["", None]:
            code += "bids_handler.addLicense(%(bids_license)s, force=True)\n"
        buff.writeIndentedLines(code % self.params)

        # Add task code if enabled
        if self.params["add_code"]:
            code = "bids_handler.addTaskCode(force=True)\n"
            buff.writeIndentedLines(code)

        # Add environment if enabled
        if self.params["add_environment"]:
            code = "bids_handler.addEnvironment()\n"
            buff.writeIndentedLines(code)

        # Add dataset description if provided
        if self.params["dataset_description"].val not in ["", None]:
            code = "bids_handler.addDatasetDescription(%(dataset_description)s, force=True)\n"
            buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(original_indent_level)

    def writeExperimentEndCode(self, buff):
        """Write code at the end of the routine."""
        original_indent_level = buff.indentLevel

        code = "ignore_list = [\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "'participant',\n"
            "'session',\n"
            "'date',\n"
            "'expName',\n"
            "'psychopyVersion',\n"
            "'OS',\n"
            "'frameRate'\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "]\nparticipant_info = {\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "key: thisExp.extraInfo[key]\n"
            "for key in thisExp.extraInfo\n"
            "if key not in ignore_list\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "}\n# write tsv file and update\ntry:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "if bids_handler.events:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        if self.params["json_sidecar"] == "":
            self.params["json_sidecar"] = True
        code = "bids_handler.writeEvents(participant_info, add_stimuli=%(add_stimuli)s, execute_sidecar=%(json_sidecar)s, generate_hed_metadata=%(generate_hed_metadata)s)\n"
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-2, relative=True)
        code = "except Exception as e:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = 'print(f"An error occurred when writing BIDS events: {e}")\n'
        buff.writeIndentedLines(code)
        buff.setIndentLevel(original_indent_level)
