"""This module provides the class BIDSHandler"""

import importlib.metadata
import json
import os
import platform
import re
import shutil
import sys
import warnings
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from typing import List, Union

import pandas as pd
import requests
from hed.tools.analysis.tabular_summary import TabularSummary
from packaging.version import Version

from psychopy_bids.bids.bidsbehevent import BIDSBehEvent
from psychopy_bids.bids.bidstaskevent import BIDSTaskEvent


class BIDSHandler:
    """A class to handle the creation of a BIDS-compliant dataset.

    This class provides methods for creating and managing BIDS datasets and their modality agnostic
    files plus modality specific files.

    Examples
    --------
    >>> from psychopy_bids import bids
    >>> handler = bids.BIDSHandler(dataset="example_dataset")
    """

    def __init__(
        self,
        dataset: str,
        subject: Union[str, None] = None,
        task: Union[str, None] = None,
        session: Union[str, None] = None,
        data_type: str = "beh",
        acq: Union[str, None] = None,
        runs: bool = True,
    ) -> None:
        """Initialize a BIDSHandler object.

        Parameters
        ----------
        dataset : str
            A set of neuroimaging and behavioral data acquired for a purpose of a particular study.
        subject : str, optional
            A person or animal participating in the study.
        task : str, optional
            A set of structured activities performed by the participant.
        session : str, optional
            A logical grouping of neuroimaging and behavioral data consistent across subjects.
        data_type : str, optional
            A functional group of different types of data.
        acq : str, optional
            Custom label to distinguish different conditions present during multiple runs of the
            same task.
        runs : bool, optional
            If True, run will be added to filename.
        """
        self.dataset = dataset
        self.subject = subject
        self.task = task
        self.session = session
        self.data_type = data_type
        self.acq = acq
        self.runs = runs
        self.__events = []

    @property
    def dataset(self) -> str:
        """A set of neuroimaging and behavioral data acquired for a purpose of a particular study."""
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset: str) -> None:
        self.__dataset = str(dataset)

    @property
    def subject(self) -> Union[str, None]:
        """A participant identifier of the form sub-<label>, matching a participant entity in the dataset."""
        return self.__subject

    @subject.setter
    def subject(self, subject: Union[str, None]) -> None:
        match = re.match(r"^sub-[0-9a-zA-Z]+$", str(subject))
        if match:
            self.__subject = subject
        else:
            sanitized = re.sub(r"[^A-Za-z0-9]+", "", str(subject))
            self.__subject = f"sub-{sanitized}"

    @property
    def task(self) -> Union[str, None]:
        """A set of structured activities performed by the participant."""
        return self.__task

    @task.setter
    def task(self, task: Union[str, None]) -> None:
        pattern = re.compile(r"^task-[0-9a-zA-Z]+$", re.I)
        match = pattern.match(str(task))
        if match:
            self.__task = task
        else:
            sanitized = re.sub(r"[^A-Za-z0-9]+", "", str(task))
            self.__task = f"task-{sanitized}"

    @property
    def session(self) -> Union[str, None]:
        """A logical grouping of neuroimaging and behavioral data consistent across subjects."""
        return self.__session

    @session.setter
    def session(self, session: Union[str, None]) -> None:
        if session:
            pattern = re.compile(r"^ses-[0-9a-zA-Z]+$", re.I)
            match = pattern.match(str(session))
            if match:
                self.__session = session
            else:
                sanitized = re.sub(r"[^A-Za-z0-9]+", "", str(session))
                self.__session = f"ses-{sanitized}"
        else:
            self.__session = None

    @property
    def data_type(self) -> str:
        """A functional group of different types of data."""
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type: str) -> None:
        types = [
            "beh",
            "eeg",
            "func",
            "ieeg",
            "nirs",
            "meg",
            "motion",
            "mrs",
            "pet",
        ]
        if str(data_type) in types:
            self.__data_type = str(data_type)
        else:
            msg = f"<data_type> MUST be one of the following: {types}"
            sys.exit(msg)

    @property
    def acq(self) -> Union[str, None]:
        """A label to distinguish a different set of parameters used for acquiring the same modality."""
        return self.__acq

    @acq.setter
    def acq(self, acq: Union[str, None]) -> None:
        if acq:
            pattern = re.compile(r"^acq-[0-9a-zA-Z]+$", re.I)
            match = pattern.match(str(acq))
            if match:
                self.__acq = acq
            else:
                sanitized = re.sub(r"[^A-Za-z0-9]+", "", str(acq))
                self.__acq = f"acq-{sanitized}"
        else:
            self.__acq = None

    @property
    def events(self) -> List[Union[BIDSBehEvent, BIDSTaskEvent]]:
        """Get the list of events."""
        return self.__events

    def addEvent(
        self,
        event: Union[
            BIDSBehEvent, BIDSTaskEvent, List[Union[BIDSBehEvent, BIDSTaskEvent]]
        ],
    ) -> None:
        """Add an event or list of events.

        Parameters
        ----------
        event : Any or list
            The event or list of events to be added to the list.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset")
        >>> handler.addEvent(bids.BIDSBehEvent(trial=1))
        >>> handler.addEvent([bids.BIDSBehEvent(trial=2), bids.BIDSBehEvent(trial=3)])
        """
        if isinstance(event, list):
            self.__events.extend(event)
        else:
            self.__events.append(event)

    def addChanges(
        self, changes: list, version: str = "PATCH", force: bool = False
    ) -> None:
        """Update the version history of the dataset.

        This method updates the CPAN changelog-like file `CHANGES` by adding a new version entry
        with the specified changes and incrementing the version number accordingly.

        Parameters
        ----------
        changes : list
            List of changes or bullet points for the new version.
        version : str, optional
            The version part to increment. Must be one of "MAJOR", "MINOR", or "PATCH".
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject=None, task=None)
        >>> handler.createDataset()
        >>> handler.addChanges(["Added new data files"], "MAJOR")

        Notes
        -----
        Version history of the dataset (describing changes, updates and corrections) MAY be provided
        in the form of a CHANGES text file. This file MUST follow the CPAN Changelog convention.
        The CHANGES file MUST be either in ASCII or UTF-8 encoding. For more details on the CHANGES
        file, see:
        https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#changes
        """
        changelog_dest = Path(self.dataset) / "CHANGES"
        if not force and changelog_dest.exists():
            print(
                "File 'CHANGES' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
            return

        new_version = self._incrementVersion(changelog_dest, version)
        entry = self._createChangeLogEntry(new_version, changes, changelog_dest)

        with open(changelog_dest, mode="w", encoding="utf-8") as file:
            file.write(entry + "\n\n")

    def addDatasetDescription(
        self, file_path: Union[str, None] = None, force: bool = False
    ) -> None:
        """Add a description to the dataset by creating `dataset_description.json`.

        This method adds the required `dataset_description.json` file to the dataset.

        Parameters
        ----------
        file_path : str or None, optional
            Path to a custom `dataset_description.json` file. If None, the default template is used.
        force : bool, optional
            Specifies whether existing files should be overwritten.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.createDataset()
        >>> handler.addDatasetDescription()

        Notes
        -----
        The file `dataset_description.json` is a JSON file describing the dataset. Every dataset
        MUST include this file. For more details, see:
        https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#dataset-description
        """
        dataset_desc = Path(self.dataset) / "dataset_description.json"
        if not force and dataset_desc.exists():
            print(
                "File 'dataset_description.json' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
            return

        ds_info = self._loadDatasetDescriptionTemplate(file_path)
        ds_info.update(
            {
                "Name": self.dataset,
                "BIDSVersion": self._getLatestBidsVersion(),
                "HEDVersion": self._getLatestHedVersion(),
                "DatasetType": "raw",
                "GeneratedBy": [
                    {
                        "Name": "psychopy-bids",
                        "Version": self._getPackageVersion("psychopy-bids"),
                        "Description": "A PsychoPy plugin for working with the Brain Imaging Data Structure (BIDS).",
                        "CodeURL": "https://gitlab.com/psygraz/psychopy-bids",
                    }
                ],
            }
        )

        with open(dataset_desc, "w", encoding="utf-8") as write_file:
            json.dump(ds_info, write_file, indent=4)

    def addLicense(self, identifier: str, force: bool = False) -> None:
        """Add a license file to the dataset.

        This method downloads a license with the given identifier from the SPDX license list and
        copies the content into the file `LICENSE`.

        Parameters
        ----------
        identifier : str
            Identifier of the license.
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.createDataset()
        >>> handler.addLicense("CC-BY-NC-4.0")

        Notes
        -----
        A LICENSE file MAY be provided in addition to the short specification of the used license
        in the dataset_description.json "License" field. The "License" field and LICENSE file MUST
        correspond. The LICENSE file MUST be either in ASCII or UTF-8 encoding. For more details, see:
        https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#license
        """
        dataset_desc = Path(self.dataset) / "dataset_description.json"
        if not dataset_desc.exists():
            self.addDatasetDescription()

        with dataset_desc.open("r", encoding="utf-8") as file:
            ds_info = json.load(file)
        ds_info["License"] = identifier
        with dataset_desc.open("w", encoding="utf-8") as write_file:
            json.dump(ds_info, write_file)

        license_dest = Path(self.dataset) / "LICENSE"
        if not force and license_dest.exists():
            print(
                "File 'LICENSE' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
        else:
            self._downloadLicense(identifier, license_dest)

    def addReadme(self, force: bool = False) -> None:
        """Add a text file explaining the dataset in detail.

        This method adds a `README` template file to the dataset, which contains the main sections
        needed to describe the dataset in more detail.

        Parameters
        ----------
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.createDataset()
        >>> handler.addReadme()

        Notes
        -----
        A REQUIRED text file, README, SHOULD describe the dataset in more detail. A BIDS dataset
        MUST NOT contain more than one README file (with or without extension) at its root
        directory. For more details, see:
        https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#readme
        """
        readme_dest = Path(self.dataset) / "README"
        if not force and readme_dest.exists():
            print(
                "File 'README' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
        else:
            bidsdir = Path(sys.modules["psychopy_bids.bids"].__path__[0])
            readme_src = bidsdir / "template" / "README"
            shutil.copyfile(readme_src, readme_dest)

    def addTaskCode(self, path: Union[str, None] = None, force: bool = False) -> None:
        """Add psychopy script or specified code directory to the BIDS /code directory.

        This method copies the psychopy script or a specified folder into the `/code` directory
        of the dataset. If a path is provided, the function handles files and folders
        appropriately. If the path starts with "code/", this prefix is stripped only for the
        destination placement.

        Parameters
        ----------
        path : str, optional
            Path to the file or folder to copy. If None, the main script is used.
        force : bool, optional
            If True, existing files are overwritten. Default is False.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.addTaskCode(path="tests/bids_validator/experiment_lastrun.py", force=True)

        Notes
        -----
        The method ensures no files are overwritten unless the `force` parameter is set to True.
        If the path starts with "code/", the prefix is stripped only from the destination.
        If a file or directory already exists in `/code`, a warning is issued unless `force=True`.
        """
        code_path, psyexp_path = self._determineCodePath(path)
        code_dir = Path(self.dataset) / "code"
        code_dir.mkdir(parents=True, exist_ok=True)

        self._copyItem(code_path, code_dir, force)
        if psyexp_path and psyexp_path.exists():
            self._copyItem(psyexp_path, code_dir, force)

    def addEnvironment(self) -> None:
        """Generate a deduplicated requirements.txt and update .bidsignore.

        This method scans the current Python environment for installed packages,
        consolidates them into a `requirements.txt` file, and writes it to the dataset.
        If multiple versions of the same package are found, the higher version is used,
        and a warning is printed. The `requirements.txt` file is also added to `.bidsignore`
        to ensure it is ignored during BIDS validation.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.createDataset()
        >>> handler.addEnvironment()
        """
        bidsignore_path = Path(self.dataset) / ".bidsignore"
        req_path = Path(self.dataset) / "requirements.txt"

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        packages = {}
        for dist in importlib.metadata.distributions():
            name = dist.metadata["Name"].lower()
            version = dist.version
            old_version = packages.get(name)

            if old_version and old_version != version:
                print(
                    f"Warning: Multiple versions of '{name}' ({old_version}, {version}) found "
                    "while generating requirements.txt. Using the higher version."
                )
                packages[name] = str(max(Version(old_version), Version(version)))
            else:
                packages[name] = version

        with open(req_path, "w", encoding="utf-8") as f:
            f.write(f"# Python version: {python_version}\n")
            for pkg_name in sorted(packages):
                f.write(f"{pkg_name}=={packages[pkg_name]}\n")

        self._updateBidsIgnore(bidsignore_path, "requirements.txt")

    def createDataset(
        self,
        readme: bool = True,
        chg: bool = True,
        lic: bool = True,
        force: bool = False,
    ) -> None:
        """Create the rudimentary body of a new dataset.

        Parameters
        ----------
        readme : bool, optional
            Specifies whether a README file should be created.
        chg : bool, optional
            Specifies whether a CHANGES file should be created.
        lic : bool, optional
            Specifies whether a LICENSE file should be created.
        force : bool, optional
            Specifies whether existing files should be overwritten.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> handler.createDataset()
        """
        dataset_path = Path(self.dataset)
        if not force and dataset_path.exists():
            print(
                f"The folder {self.dataset} already exists! Use the parameter force if you want to recreate a dataset in an existing, non-empty directory",
                file=sys.stderr,
            )
            return

        dataset_path.mkdir(exist_ok=True)
        (dataset_path / "participants.tsv").touch()

        self.addDatasetDescription()
        if readme:
            self.addReadme(force=force)
        if chg:
            self.addChanges(changes=["Initialize the dataset"], force=force)
        if lic:
            self.addLicense(identifier="CC-BY-NC-4.0", force=force)

    def writeEvents(
        self,
        participant_info: dict,
        execute_sidecar: Union[bool, str] = True,
        generate_hed_metadata: bool = True,
        add_stimuli: bool = True,
        event_type: str = "both",
    ):
        """Writes all existing events in `self.events` to the dataset.

        Parameters
        ----------
        participant_info : dict
            Key-value pairs describing participant info (e.g. age, sex, group) to be inserted
            into participants.tsv. A 'participant_id' key will automatically be added/updated
            with `self.subject`.
        execute_sidecar : Union[bool, str], optional
            If True, creates or updates a JSON sidecar file for the events file with metadata.
            If a string, uses the provided path to update the sidecar file.
        generate_hed_metadata : bool, optional
            If True, automatically generates HED metadata based on the event file.
            Only applies if execute_sidecar is not False.
        add_stimuli : bool, optional
            If True, copies any referenced stimuli in the event file to a `/stimuli` folder.
        event_type : str, optional
            One of {'both', 'beh', 'task'}:
            - 'both': Writes both behavioral and task events.
            - 'beh': Only writes behavioral events (`*_beh.tsv`).
            - 'task': Only writes task events (`*_events.tsv`).

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset")
        >>> handler.addEvent(bids.BIDSBehEvent(trial=1))
        >>> handler.addEvent(bids.BIDSTaskEvent(onset=1.0, duration=0.5))
        >>> handler.writeEvents(participant_info={'participant_id': handler.subject}, execute_sidecar=False)
        """
        self._updateParticipantsFile(participant_info)

        bids_beh_events = [e for e in self.events if type(e) is BIDSBehEvent]
        bids_task_events = [e for e in self.events if type(e) is BIDSTaskEvent]

        if event_type == "beh":
            bids_task_events = []
        elif event_type == "task":
            bids_beh_events = []

        written_events = []
        if bids_beh_events:
            written_events.extend(
                self._writeSingleEventFile(
                    bids_beh_events,
                    "beh",
                    execute_sidecar,
                    generate_hed_metadata,
                    add_stimuli,
                )
            )
        if bids_task_events:
            written_events.extend(
                self._writeSingleEventFile(
                    bids_task_events,
                    "events",
                    execute_sidecar,
                    generate_hed_metadata,
                    add_stimuli,
                )
            )

        self.__events = [e for e in self.events if e not in written_events]

    def _updateParticipantsFile(self, participant_info: dict) -> None:
        """
        Update or create the participants.tsv file with the given participant information.

        Parameters
        ----------
        participant_info : dict
            Dictionary containing participant metadata (e.g., {'age': 25, 'sex': 'M'}).
            The key 'participant_id' will be updated with `self.subject`.
        """
        participants_file = Path(self.dataset) / "participants.tsv"
        participant_info["participant_id"] = self.subject

        if participants_file.stat().st_size == 0:
            df_participants = pd.DataFrame([participant_info])
            participant_cols = ["participant_id"] + [
                col for col in df_participants.columns if col != "participant_id"
            ]
            df_participants = df_participants[participant_cols]
            df_participants = df_participants.fillna("n/a")
            participants_metadata = {
                field: {
                    "Description": "RECOMMENDED. Free-form natural language description."
                }
                for field in participant_info
            }
            with open(
                f"{self.dataset}/participants.json", mode="w", encoding="utf-8"
            ) as f:
                json.dump(participants_metadata, f)

            df_participants.to_csv(participants_file, sep="\t", index=False)
        else:
            df_participants = pd.read_csv(participants_file, sep="\t")
            if self.subject not in df_participants["participant_id"].tolist():
                df_participants = pd.concat(
                    [df_participants, pd.DataFrame([participant_info])],
                    ignore_index=True,
                )
                participant_cols = ["participant_id"] + [
                    col for col in df_participants.columns if col != "participant_id"
                ]
                df_participants = df_participants[participant_cols]
                df_participants = df_participants.fillna("n/a")
                df_participants.to_csv(participants_file, sep="\t", index=False)

    def _writeSingleEventFile(
        self,
        events: list,
        event_type: str,
        execute_sidecar: Union[bool, str],
        generate_hed_metadata: bool,
        add_stimuli: bool,
    ) -> list:
        """
        Write a single type of events to the dataset (behavioral or task).

        Optionally creates a JSON sidecar file and copies stimuli if requested.

        Parameters
        ----------
        events : list
            List of event dictionaries (BIDSBehEvent or BIDSTaskEvent instances, as dicts).
        event_type : str
            The suffix in the event filename (e.g., 'beh' or 'events').
        execute_sidecar : Union[bool, str]
            If True, calls `_addJsonSidecar` to create/update sidecar metadata.
            If a string, uses the provided path to update the sidecar file.
        generate_hed_metadata : bool
            If True, automatically generates HED metadata based on the event file.
            Only applies if execute_sidecar is not False.
        add_stimuli : bool
            If True, calls `_addStimuliFolder` to copy referenced stimuli.

        Returns
        -------
        list
            The same list of events that were written, for reference (used to update `self.__events`).
        """
        df_events = pd.DataFrame(events)
        df_events.dropna(how="all", axis=1, inplace=True)
        df_events = df_events.fillna("n/a").infer_objects(copy=False)

        if "stim_file" in df_events.columns:
            df_events["stim_file"] = df_events["stim_file"].apply(
                lambda stim: (
                    Path(*Path(stim).parts[1:]).as_posix()
                    if stim.startswith("stimuli/")
                    else stim.replace("\\", "/")
                )
            )

        if "onset" in df_events.columns and "duration" in df_events.columns:
            col_order = ["onset", "duration"] + [
                c for c in df_events.columns if c not in ["onset", "duration"]
            ]
            df_events = df_events[col_order]

        filepath = self._generateEventFilePath(event_type)
        df_events.to_csv(filepath, sep="\t", index=False)

        if execute_sidecar:
            self._addJsonSidecar(
                filepath, event_type, execute_sidecar, generate_hed_metadata
            )
        if add_stimuli:
            self._addStimuliFolder(filepath)

        return events

    def _generateEventFilePath(self, event_type: str) -> Path:
        """
        Generate the file path for the event file based on its type and the current
        dataset, subject, session, and data_type.

        Parameters
        ----------
        event_type : str
            The suffix to use in the filename (e.g., 'beh' or 'events').

        Returns
        -------
        pathlib.Path
            The full path (including filename) to the event file to be created.
        """
        event_dir_parts = [self.dataset, self.subject]
        if self.session:
            event_dir_parts.append(self.session)
        event_dir_parts.append(self.data_type)
        event_dir = Path(*event_dir_parts)
        event_dir.mkdir(parents=True, exist_ok=True)

        filename_parts = [self.subject, self.task]
        if self.session:
            filename_parts.insert(1, self.session)
        if self.acq:
            filename_parts.append(self.acq)
        base_filename = "_".join(filename_parts)

        existing_files = list(event_dir.glob(f"{base_filename}*_{event_type}.tsv"))
        if self.runs:
            file_name = (
                f"{base_filename}_run-{len(existing_files) + 1}_{event_type}.tsv"
            )
        else:
            file_name = f"{base_filename}_{event_type}.tsv"

        full_event_path = event_dir / file_name

        if event_type == "beh" and self.data_type != "beh":
            warnings.warn(
                f"You are writing a 'beh' event file in a dataset with data_type='{self.data_type}', "
                "which is not BIDS valid. "
                "If you intend to store behavioral event data, please set 'data_type=beh'. "
                "Otherwise, use Task events instead. "
                f"\nThis invalid file has been saved to: {full_event_path}"
            )
        return full_event_path

    def _addJsonSidecar(
        self,
        event_filepath: Path,
        event_type: str,
        sidecar_path: Union[bool, str],
        generate_hed_metadata: bool,
    ) -> None:
        """
        Create or update the JSON sidecar file for the events file.

        Parameters
        ----------
        event_filepath : pathlib.Path
            The path to the written event TSV file.
        event_type : str
            Indicates whether this is a 'beh' or 'events' file for the sidecar naming.
        sidecar_path : Union[bool, str]
            If a string, uses the provided path to update the sidecar file.
        generate_hed_metadata : bool
            If True, automatically generates HED metadata based on the event file.
        """
        if isinstance(sidecar_path, str):
            template_path = Path(sidecar_path)
            if template_path.exists():
                sidecar = self._loadSidecarTemplate(template_path)
            else:
                warnings.warn(
                    f"Provided sidecar template does not exist at: {template_path}. Falling back to an empty template."
                )
                sidecar = {}
        else:
            sidecar = {}

        json_path = (
            Path(self.dataset)
            / f"{self.task}_{self.acq + '_' if self.acq else ''}{event_type}.json"
        )

        existing_sidecar = {}
        if json_path.exists():
            try:
                with open(json_path, mode="r", encoding="utf-8") as json_reader:
                    existing_sidecar = json.load(json_reader)
                print(
                    f"Info: Found an existing sidecar file at {json_path}. It will be updated with new metadata and any missing fields."
                )
            except (TypeError, json.JSONDecodeError):
                warnings.warn(
                    f"Failed to load the existing sidecar file at {json_path}. The file might be corrupted or "
                    "contain invalid JSON format. Proceeding with the creation of a new sidecar."
                )

        if event_type == "beh":
            task_metadata = {
                "TaskName": self.task.replace("task-", ""),
                "TaskDescription": "RECOMMENDED. Detailed description of the task.",
                "Instructions": "RECOMMENDED. Text of the instructions given to participants.",
                "CogAtlasID": "RECOMMENDED. URL of the corresponding Cognitive Atlas term.",
                "CogPOID": "RECOMMENDED. URL of the corresponding CogPO term.",
                "InstitutionName": "RECOMMENDED. The institution responsible for the equipment.",
                "InstitutionAddress": "RECOMMENDED. The address of the institution.",
                "InstitutionalDepartmentName": "RECOMMENDED. The department within the institution.",
            }
            sidecar = {**task_metadata, **sidecar}

        event_data = pd.read_csv(event_filepath, sep="\t")

        if "HED" not in event_data.columns and generate_hed_metadata:
            skip_columns = {"onset", "duration", "trial_type"}
            skip_columns.update(existing_sidecar.keys())
            skip_columns.update(sidecar.keys())
            value_columns = ["response_time"]
            value_columns = [col for col in value_columns if col not in skip_columns]
            value_summary = TabularSummary(
                value_cols=value_columns, skip_cols=skip_columns
            )
            value_summary.update([str(event_filepath)])
            hed_metadata = value_summary.extract_sidecar_template()
        else:
            print(
                "Info: HED metadata generation disabled or HED column found in the event file. Skipping HED metadata generation."
            )
            hed_metadata = {}

        column_metadata_template = {
            "Description": "RECOMMENDED. Free-form natural language description.",
        }

        for column_name in event_data.columns:
            if column_name not in sidecar and column_name != "HED":
                sidecar[column_name] = column_metadata_template.copy()
                print(
                    f"Info: Adding column '{column_name}' to the sidecar metadata. This column was found in the event file but not in the provided/default template. "
                )

            if column_name in hed_metadata:
                for key, value in hed_metadata[column_name].items():
                    if key not in sidecar[column_name]:
                        sidecar[column_name][key] = value
                    elif isinstance(value, dict):
                        sidecar[column_name][key] = {
                            **sidecar[column_name].get(key, {}),
                            **value,
                        }

        for sidecar_column in sidecar.keys():
            if (
                sidecar_column not in event_data.columns
                and sidecar_column not in task_metadata
            ):
                warnings.warn(
                    f"The column '{sidecar_column}' is present in the sidecar but does not appear in the event file '{event_filepath}'."
                )

        for key, value in existing_sidecar.items():
            if key not in sidecar:
                sidecar[key] = value

        sidecar["StimulusPresentation"] = {
            "OperatingSystem": self._getOsInfo(),
            "SoftwareName": "PsychoPy",
            "SoftwareRRID": "RRID:SCR_006571",
            "SoftwareVersion": self._getPackageVersion("psychopy"),
        }

        with open(json_path, mode="w", encoding="utf-8") as json_file:
            json.dump(sidecar, json_file, indent=4)

    def _addStimuliFolder(self, event_filepath) -> None:
        """
        Copies files referenced in the 'stim_file' column of the event TSV into a
        'stimuli' directory under the dataset root, preserving folder structure.

        Parameters
        ----------
        event_filepath : str or pathlib.Path
            Path to the TSV event file from which to extract 'stim_file' references.
        """
        dest_path = Path(self.dataset) / "stimuli"
        data_frame = pd.read_csv(event_filepath, sep="\t")

        if "stim_file" in data_frame.columns:
            for stim in data_frame["stim_file"].dropna().unique():
                stim_path = Path(stim)
                src = stim_path if stim_path.is_file() else Path("stimuli") / stim_path
                dest_file = dest_path / stim_path

                if src.is_file():
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dest_file)
                else:
                    print(f"File '{stim}' not found at '{src}'!", file=sys.stderr)

    @staticmethod
    def parseLog(file, level="BIDS", regex=None) -> list:
        """Extract events from a log file.

        This method parses a given log file based on the specified log level and, optionally, a
        regex pattern. It then processes and structures these events into a list each adhering to
        the BIDSTaskEvent event format.

        Parameters
        ----------
        file : str
            The file path of the log file.
        level : str
            The level name of the bids task events.
        regex : str, optional
            A regular expression to parse the message string.

        Return
        ------
        events : list
            A list of events like presented stimuli or participant responses.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="example_dataset", subject="sub-01", task="simple")
        >>> log_events = handler.parseLog("simple1.log", "BIDS")
        """
        events = []
        try:
            with open(file, mode="r", encoding="utf-8") as log_file:
                for line in log_file:
                    event = re.split(r" \t|[ ]+", line, maxsplit=2)
                    if level in event:
                        entry = BIDSHandler._parseLogEntry(event, regex)
                        events.append(entry)
        except FileNotFoundError:
            warnings.warn(f"file {file} NOT FOUND!")
        return events

    @staticmethod
    def _parseLogEntry(event, regex):
        """Parse a single log entry."""
        if regex:
            match = re.search(regex, event[2])
            entry = match.groupdict() if match else {}
        else:
            entry = {k: v for k, v in literal_eval(event[2]).items() if v is not None}
        entry.setdefault("onset", float(event[0]))
        entry.setdefault("duration", "n/a")
        return entry

    @staticmethod
    def _incrementVersion(changelog_dest, version):
        """Increment the version number based on the specified version part.

        Parameters
        ----------
        changelog_dest : pathlib.Path
            Path to the changelog file
        version : str
            Version part to increment ("MAJOR", "MINOR", or "PATCH")

        Returns
        -------
        str
            The new version number
        """
        if changelog_dest.exists():
            with open(changelog_dest, "r", encoding="utf-8") as file:
                content = file.read()
            matches = re.findall(r"(\d+\.\d+\.\d+)\s+-", content, re.MULTILINE)
            if matches:
                curr_version = [
                    int(num) for num in sorted(matches, reverse=True)[0].split(".")
                ]
                new_version_list = curr_version[:]
                if version == "MAJOR":
                    new_version_list[0] += 1
                elif version == "MINOR":
                    new_version_list[1] += 1
                else:
                    new_version_list[2] += 1
                return ".".join(str(num) for num in new_version_list)
        return "1.0.0"

    @staticmethod
    def _createChangeLogEntry(new_version, changes, changelog_dest):
        """Create a new changelog entry with version, date and changes.

        Parameters
        ----------
        new_version : str
            Version number for the new entry
        changes : list
            List of changes to include
        changelog_dest : pathlib.Path
            Path to the changelog file

        Returns
        -------
        str
            Formatted changelog entry
        """
        entry = f"{new_version} - {datetime.now().strftime('%Y-%m-%d')}\n" + "\n".join(
            [f" - {change}" for change in changes]
        )
        if changelog_dest.exists():
            with open(changelog_dest, "r", encoding="utf-8") as file:
                content = file.read()
            entry += "\n\n" + content
        return entry

    @staticmethod
    def _loadDatasetDescriptionTemplate(file_path):
        """Load the dataset description JSON template.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path, None]
            Path to custom template file, if None uses default

        Returns
        -------
        dict
            Template data as dictionary
        """
        if file_path and Path(file_path).exists():
            with open(file_path, mode="r", encoding="utf-8") as read_file:
                return json.load(read_file)
        bidsdir = Path(sys.modules["psychopy_bids.bids"].__path__[0])
        ds_desc = bidsdir / "template" / "dataset_description.json"
        with open(ds_desc, mode="r", encoding="utf-8") as read_file:
            return json.load(read_file)

    @staticmethod
    def _getPackageVersion(package_name):
        """Get the version of a Python package.

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        str
            Version string or "unknown"
        """
        try:
            version = importlib.metadata.version(package_name)
            if not version:
                warnings.warn(
                    f"The version of '{package_name}' could not be determined and will be set to 'unknown' in BIDS metadata files."
                )
                return "unknown"
            return version
        except importlib.metadata.PackageNotFoundError:
            warnings.warn(
                f"The version of '{package_name}' could not be determined and will be set to 'unknown' in BIDS metadata files."
            )
            return "unknown"

    @staticmethod
    def _downloadLicense(identifier, license_dest):
        """Download a license file from SPDX.

        Parameters
        ----------
        identifier : str
            SPDX license identifier
        license_dest : pathlib.Path
            Destination path for license file
        """
        try:
            response = requests.get(
                f"https://spdx.org/licenses/{identifier}.txt", timeout=2
            )
            if response.status_code == 200:
                with open(license_dest, "w", encoding="utf-8") as file:
                    file.write(response.text)
            else:
                print(
                    f"License '{identifier}' not found or could not be downloaded.",
                    file=sys.stderr,
                )
        except requests.exceptions.Timeout:
            print(f"Request to download {identifier} timed out.", file=sys.stderr)
        except requests.exceptions.RequestException as exc:
            print(f"Request error: {exc}", file=sys.stderr)

    @staticmethod
    def _determineCodePath(path):
        """Determine code and psyexp paths from input path.

        Parameters
        ----------
        path : Union[str, None]
            Input path to analyze

        Returns
        -------
        tuple
            Tuple of (code_path, psyexp_path)
        """
        if path:
            code_path = Path(path)
            psyexp_path = None
        else:
            main_script = Path(os.path.basename(sys.argv[0]))
            code_path = main_script
            if "_lastrun" in main_script.stem:
                psyexp_path = main_script.with_name(
                    main_script.stem.replace("_lastrun", "") + ".psyexp"
                )
            else:
                psyexp_path = None
        return code_path, psyexp_path

    @staticmethod
    def _copyItem(src, dst_dir, force):
        """Copy file or directory to destination, with overwrite protection.

        Parameters
        ----------
        src : pathlib.Path
            Source file or directory to copy
        dst_dir : pathlib.Path
            Destination directory to copy into
        force : bool
            If True, overwrite existing files
        """
        dst = dst_dir / src.name
        if not src.is_dir():
            dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and not force:
            warnings.warn(
                f"'{dst}' already exists. Use force=True to overwrite.", UserWarning
            )
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=force)
        else:
            shutil.copy2(src, dst)

    @staticmethod
    def _updateBidsIgnore(bidsignore_path, entry):
        """Update the .bidsignore file by adding a new entry if it doesn't exist.

        Parameters
        ----------
        bidsignore_path : pathlib.Path
            Path to the .bidsignore file
        entry : str
            Entry to add to the ignore file
        """
        entries = []
        if bidsignore_path.exists():
            with open(bidsignore_path, "r", encoding="utf-8") as f:
                entries = f.read().splitlines()
        if entry not in entries:
            entries.append(entry)
            with open(bidsignore_path, "w", encoding="utf-8") as f:
                f.write("\n".join(entries) + "\n")

    @staticmethod
    def _loadSidecarTemplate(template_path: Path) -> dict:
        """
        Load the sidecar template from a specified file path.

        Parameters
        ----------
        template_path : pathlib.Path
            Path to the template file.

        Returns
        -------
        dict
            Loaded sidecar template as a dictionary.
        """
        try:
            if template_path.suffix == ".json":
                with open(template_path, mode="r", encoding="utf-8") as f:
                    return json.load(f)
            elif template_path.suffix in [".csv", ".tsv", ".xlsx"]:
                df = (
                    pd.read_excel(template_path)
                    if template_path.suffix == ".xlsx"
                    else pd.read_csv(
                        template_path,
                        sep="\t" if template_path.suffix == ".tsv" else ",",
                    )
                )

                sidecar = {}
                for _, row in df.iterrows():
                    try:
                        column_name = (
                            str(row["column_name"])
                            .replace("\u00a0", " ")
                            .replace("\n", " ")
                            .strip()
                        )
                        column_value = (
                            str(row["column_value"])
                            .replace("\u00a0", " ")
                            .replace("\n", " ")
                            .strip()
                        )
                        description = (
                            str(row["description"])
                            .replace("\u00a0", " ")
                            .replace("\n", " ")
                            .strip()
                        )
                        hed = (
                            str(row.get("HED", ""))
                            .replace("\u00a0", " ")
                            .replace("\n", " ")
                            .strip()
                        )

                        sidecar.setdefault(column_name, {})[column_value] = {
                            "Description": description,
                            "HED": hed,
                        }
                    except KeyError:
                        warnings.warn(
                            f"Missing expected keys (e.g., 'column_name', 'column_value', 'description') in the sidecar template file {template_path.name}. "
                            "Skipping the row. Verify the template file structure for completeness."
                        )
                return sidecar
            else:
                raise ValueError(f"Unsupported file format: {template_path.suffix}")
        except FileNotFoundError:
            warnings.warn(
                f"File not found: {template_path}. Using an empty template. Ensure the file path is correct."
            )
        except json.JSONDecodeError as e:
            warnings.warn(
                f"Invalid JSON format in the file {template_path}. The error details are: {e}. "
                "The file might be malformed or not intended to be a JSON sidecar. Using an empty template instead."
            )
        except pd.errors.ParserError as e:
            warnings.warn(
                f"Failed to parse the file {template_path} as a CSV/TSV. Error details: {e}. Ensure the file conforms to the expected format. "
                "Using an empty template as a fallback."
            )
        except ValueError as e:
            warnings.warn(
                f"Value error encountered while processing the sidecar template file at {template_path}: {e}. "
                "This may indicate an unsupported format or unexpected data. Proceeding with an empty template."
            )
        return {}

    @staticmethod
    def _getLatestBidsVersion() -> str:
        """Fetch the latest BIDS specification version from GitHub.

        Returns
        -------
        str
            Version string or fallback version
        """
        try:
            response = requests.get(
                "https://api.github.com/repos/bids-standard/bids-specification/releases/latest",
                timeout=2,
            )
            if response.status_code == 200:
                return response.json().get("tag_name", "").lstrip("v")
        except (requests.RequestException, KeyError):
            pass
        return "1.8.0"

    @staticmethod
    def _getLatestHedVersion() -> str:
        """Fetch the latest HED schema version from GitHub.

        Returns
        -------
        str
            Version string or fallback version
        """
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/hed-standard/hed-schemas/main/standard_schema/hedxml/HEDLatest.xml",
                timeout=2,
            )
            if response.status_code == 200:
                content = response.text
                hed_tag_start = content.find("<HED ")
                if hed_tag_start != -1:
                    version_start = content.find('version="', hed_tag_start) + len(
                        'version="'
                    )
                    version_end = content.find('"', version_start)
                    if version_start != -1 and version_end != -1:
                        return content[version_start:version_end]
        except requests.RequestException:
            pass
        return "8.3.0"

    @staticmethod
    def _getOsInfo():
        try:
            system_name = platform.system()

            if system_name == "Windows" and hasattr(sys, "getwindowsversion"):
                win_build = sys.getwindowsversion().build  # pylint: disable=no-member
                return (
                    "Windows 11"
                    if win_build >= 22000
                    else f"Windows {platform.release()}"
                )

            if system_name == "Linux":
                with open("/etc/os-release", encoding="utf-8") as release_file:
                    os_info = {
                        k: v.strip().strip('"')
                        for k, v in (
                            line.split("=", 1) for line in release_file if "=" in line
                        )
                    }
                return os_info.get("PRETTY_NAME", f"Linux {platform.release()}")

            if system_name == "Darwin":
                return f"macOS {platform.mac_ver()[0]}"

            return f"{system_name} {platform.release()}"

        except (OSError, ValueError, SystemError):
            return "unknown"
