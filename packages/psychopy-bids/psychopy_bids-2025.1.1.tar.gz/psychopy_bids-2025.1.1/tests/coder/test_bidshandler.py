import doctest
import os
import shutil
import subprocess
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest
from psychopy_bids import bids

@pytest.fixture
def example_dataset():
    dataset = "example_dataset"
    if os.path.exists(dataset):
        shutil.rmtree(dataset)
    yield dataset
    if os.path.exists(dataset):
        shutil.rmtree(dataset)

@pytest.fixture
def subject():
    return {"participant_id": "01", "sex": "male", "age": 20}

def test_init(example_dataset):
    with pytest.raises(TypeError):
        bids.BIDSHandler()
        bids.BIDSHandler(dataset=example_dataset)
        bids.BIDSHandler(subject="A")
        bids.BIDSHandler(task="A")
        bids.BIDSHandler(dataset=example_dataset, subject="A")
        bids.BIDSHandler(dataset=example_dataset, task="A")
        bids.BIDSHandler(subject="A", task="A")

def test_addChanges(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(force=True)
    handler.addChanges(["Init dataset"], version="MAJOR", force=True)
    handler.addChanges(["Added subject"], version="MINOR", force=True)
    handler.addChanges(["Added session"], version="PATCH", force=True)
    
    changes_path = os.path.join(example_dataset, "CHANGES")
    assert os.path.exists(changes_path), "CHANGES file was not created."
    
    with open(changes_path, "r") as f:
        content = f.read()
    assert "Init dataset" in content, "CHANGES content is incorrect for MAJOR version."
    assert "Added subject" in content, "CHANGES content is incorrect for MINOR version."
    assert "Added session" in content, "CHANGES content is incorrect for PATCH version."

def test_addEvent(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()
    
    event = bids.BIDSTaskEvent(onset=0, duration=1, trial_type="test")
    handler.addEvent(event)
    
    assert len(handler.events) == 1, "Event was not added correctly."
    assert handler.events[0].trial_type == "test", "Event trial_type is incorrect."

def test_addMultipleEvents(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()
    
    events = [
        bids.BIDSTaskEvent(onset=0, duration=1, trial_type="test1"),
        bids.BIDSTaskEvent(onset=1, duration=1, trial_type="test2"),
    ]
    handler.addEvent(events)
    
    assert len(handler.events) == 2, "Events were not added correctly."
    assert handler.events[0].trial_type == "test1", "First event trial_type is incorrect."
    assert handler.events[1].trial_type == "test2", "Second event trial_type is incorrect."

def test_writeEventsWithSidecar(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()
    
    event = bids.BIDSTaskEvent(onset=0, duration=1, trial_type="test")
    handler.addEvent(event)
    handler.writeEvents(participant_info=subject, execute_sidecar=True)
    
    event_file = os.path.join(example_dataset, "sub-01", "beh", "sub-01_task-task1_run-1_events.tsv")
    sidecar_file = os.path.join(example_dataset, "task-task1_events.json")
    
    assert os.path.exists(event_file), "Event file was not created."
    assert os.path.exists(sidecar_file), "Sidecar file was not created."

def test_writeEventsWithoutSidecar(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()
    
    event = bids.BIDSTaskEvent(onset=0, duration=1, trial_type="test")
    handler.addEvent(event)
    handler.writeEvents(participant_info=subject, execute_sidecar=False)
    
    event_file = os.path.join(example_dataset, "sub-01", "beh", "sub-01_task-task1_run-1_events.tsv")
    
    assert os.path.exists(event_file), "Event file was not created."

def test_addDatasetDescription(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()
    handler.addDatasetDescription()
    handler.addDatasetDescription(force=True)
    
    description_path = os.path.join(example_dataset, "dataset_description.json")
    assert os.path.exists(description_path), "dataset_description.json file was not created."
    
    with open(description_path, "r") as f:
        content = f.read()
    assert '"Name": "example_dataset"' in content, "dataset_description.json content is incorrect."

def test_addLicense(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(lic=False, force=True)

    with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
        handler.addLicense(identifier="ABC")
    expected = "License 'ABC' not found or could not be downloaded.\n"
    actual = mock_stderr.getvalue()
    assert expected == actual

    handler.addLicense(identifier="CC0-1.0")
    with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
        handler.addLicense(identifier="CC0-1.0")
    expected = "File 'LICENSE' already exists, use force for overwriting it!\n"
    actual = mock_stderr.getvalue()
    assert expected == actual
    handler.addLicense(identifier="CC0-1.0", force=True)

def test_addReadme(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(force=True)
    with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
        handler.addReadme()
    expected = "File 'README' already exists, use force for overwriting it!\n"
    actual = mock_stderr.getvalue()
    assert expected == actual

def test_addStimuliFolder(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(force=True)

    image = bids.BIDSTaskEvent(
        onset=0,
        duration=0,
        trial_type="start",
        stim_file="images/orig_BIDS.png",
    )
    handler.addEvent(image)

    error = bids.BIDSTaskEvent(
        onset=0, duration=0, trial_type="start", stim_file="orig_BIDS.png"
    )
    handler.addEvent(error)

    handler.writeEvents(participant_info=subject)

    assert "stimuli" in os.listdir(example_dataset)
    assert os.listdir(f"{example_dataset}{os.sep}stimuli{os.sep}images") == ["orig_BIDS.png"]

def test_addTaskCode(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(force=True)

    handler.addTaskCode(path="tests/bids_validator/experiment_lastrun.py")

    code_dir = Path(example_dataset) / "code"
    expected_file = code_dir / "experiment_lastrun.py"

    assert expected_file.exists(), f"File {expected_file} was not found in /code."

def test_addEnvironment(example_dataset, subject):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset(force=True)
    handler.addEnvironment()

    # Verify `requirements.txt` was created
    requirements_path = os.path.join(example_dataset, "requirements.txt")
    assert os.path.exists(requirements_path), "requirements.txt file was not created."

    # Verify `requirements.txt` content
    with open(requirements_path, "r") as f:
        content = f.read().strip()
    assert content, "requirements.txt is empty."
    assert "# Python version:" in content, "Python version is missing in requirements.txt."

    # Dynamically check for any package from `pip freeze` output
    pip_freeze_output = subprocess.run(
        ["pip", "freeze"], stdout=subprocess.PIPE, text=True, check=True
    ).stdout.strip()
    installed_packages = [
        line.split("==")[0] for line in pip_freeze_output.splitlines()
    ]
    requirements_packages = [
        line.split("==")[0] for line in content.splitlines() if "==" in line
    ]

    # Assert that at least one package from the current environment is present in `requirements.txt`
    assert any(
        pkg in requirements_packages for pkg in installed_packages
    ), "No common packages found between pip freeze and requirements.txt"

    # Verify `.bidsignore` was updated
    bidsignore_path = os.path.join(example_dataset, ".bidsignore")
    assert os.path.exists(bidsignore_path), ".bidsignore file was not created."
    with open(bidsignore_path, "r") as f:
        bidsignore_content = f.read()
    assert "requirements.txt" in bidsignore_content, "requirements.txt not added to .bidsignore."

def test_checkDSwithAcq(example_dataset, subject):
    start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
    presentation = bids.BIDSTaskEvent(
        onset=0.5, duration=5, trial_type="presentation"
    )
    stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

    events = [start, presentation, stop]

    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        acq="highres",
        task="task1",
    )
    handler.createDataset()

    handler.addEvent(events)

    handler.writeEvents(participant_info=subject)

    assert set(os.listdir(example_dataset)) == set(
        [
            "CHANGES",
            "dataset_description.json",
            "LICENSE",
            "participants.json",
            "participants.tsv",
            "README",
            "sub-01",
            "task-task1_acq-highres_events.json",
        ]
    )
    assert os.listdir(f"{example_dataset}{os.sep}sub-01") == ["beh"]
    assert os.listdir(f"{example_dataset}{os.sep}sub-01{os.sep}beh")[0] == "sub-01_task-task1_acq-highres_run-1_events.tsv"

def test_checkDSMultipleSessions(example_dataset, subject):
    start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
    presentation = bids.BIDSTaskEvent(
        onset=0.5, duration=5, trial_type="presentation"
    )
    stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

    events = [start, presentation, stop]

    handler1 = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        session="1",
        task="task1",
    )
    handler1.createDataset()
    handler1.addEvent(events)
    handler1.writeEvents(participant_info=subject)
    handler2 = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        session="2",
        task="task1",
    )
    handler2.createDataset(chg=False, readme=False, lic=False, force=False)
    handler2.addEvent(events)
    handler2.writeEvents(participant_info=subject)
    assert set(os.listdir(example_dataset)) == set(
        [
            "CHANGES",
            "dataset_description.json",
            "LICENSE",
            "participants.json",
            "participants.tsv",
            "README",
            "sub-01",
            "task-task1_events.json",
        ]
    )
    assert sorted(os.listdir(f"{example_dataset}{os.sep}sub-01")) == sorted(["ses-1", "ses-2"])
    assert os.listdir(f"{example_dataset}{os.sep}sub-01{os.sep}ses-1{os.sep}beh")[0] == "sub-01_ses-1_task-task1_run-1_events.tsv"
    assert os.listdir(f"{example_dataset}{os.sep}sub-01{os.sep}ses-2{os.sep}beh")[0] == "sub-01_ses-2_task-task1_run-1_events.tsv"

def test_checkDSMultipleSubjects(example_dataset):
    subject1 = {"participant_id": "01", "sex": "male", "age": 20}
    subject2 = {"participant_id": "02", "sex": "female", "age": 22}

    start = bids.BIDSBehEvent(onset=0, duration=0, trial_type="start")
    presentation = bids.BIDSBehEvent(
        onset=0.5, duration=5, trial_type="presentation"
    )
    stop = bids.BIDSBehEvent(onset=10, duration=0, trial_type="stop")

    events = [start, presentation, stop]

    handler1 = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject1["participant_id"],
        task="task1",
        runs=False,
    )
    handler1.createDataset()

    handler1.addEvent(events)

    handler1.writeEvents(participant_info=subject1)

    handler2 = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject2["participant_id"],
        task="task1",
        runs=False,
    )
    handler2.createDataset()

    handler2.addEvent(events)

    handler2.writeEvents(participant_info=subject2)

    assert set(os.listdir(example_dataset)) == set(
        [
            "CHANGES",
            "dataset_description.json",
            "LICENSE",
            "participants.json",
            "participants.tsv",
            "README",
            "sub-01",
            "sub-02",
            "task-task1_beh.json",
        ]
    )
    assert os.listdir(f"{example_dataset}{os.sep}sub-01") == ["beh"]
    assert os.listdir(f"{example_dataset}{os.sep}sub-01{os.sep}beh")[0] == "sub-01_task-task1_beh.tsv"
    assert os.listdir(f"{example_dataset}{os.sep}sub-02") == ["beh"]
    assert os.listdir(f"{example_dataset}{os.sep}sub-02{os.sep}beh")[0] == "sub-02_task-task1_beh.tsv"

def test_parseLog(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject="01",
        task="task1",
    )

    # Define the log file paths
    script_dir = Path(__file__).parent
    simple1_log = f"{script_dir}{os.sep}simple1.log"
    simple2_log = f"{script_dir}{os.sep}simple2.log"
    simple3_log = f"{script_dir}{os.sep}simple3.log"

    # Test with simple1.log
    events = handler.parseLog(simple1_log)
    assert len(events) == 3

    # Test with simple2.log and a regex
    regex = r"duration-(?P<duration>\d{1})_trial-(?P<trial>\d{1})"
    events = handler.parseLog(simple2_log, regex=regex)
    assert len(events) == 3

    # Test with simple3.log expecting a warning
    with pytest.warns(UserWarning):
        events = handler.parseLog(simple3_log)

def test_subject(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="sub-01", task="A"
    )
    assert handler.subject == "sub-01"
    handler = bids.BIDSHandler(dataset=example_dataset, subject="01", task="A")
    assert handler.subject == "sub-01"

def test_task(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="01", task="task-A"
    )
    assert handler.task == "task-A"
    handler = bids.BIDSHandler(dataset=example_dataset, subject="01", task="A")
    assert handler.task == "task-A"

def test_session(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="01", task="A", session="ses-1"
    )
    assert handler.session == "ses-1"
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="01", task="A", session="1"
    )
    assert handler.session == "ses-1"

def test_data_type(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject="01",
        task="A",
        session="1",
        data_type="beh",
    )
    dt = [
        "anat",
        "beh",
        "dwi",
        "eeg",
        "fmap",
        "func",
        "ieeg",
        "meg",
        "micr",
        "perf",
        "pet",
    ]
    assert handler.data_type in dt
    with pytest.raises(SystemExit):
        bids.BIDSHandler(
            dataset=example_dataset,
            subject="01",
            task="A",
            session="1",
            data_type="abc",
        )

def test_acq(example_dataset):
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="01", task="A", acq="acq-1"
    )
    assert handler.acq == "acq-1"
    handler = bids.BIDSHandler(
        dataset=example_dataset, subject="01", task="A", acq="1"
    )
    assert handler.acq == "acq-1"

def test_writeEvents(example_dataset, subject):
    start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
    presentation = bids.BIDSTaskEvent(
        onset=0.5, duration=5, trial_type="presentation"
    )
    stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")
    test = bids.BIDSBehEvent(onset=10, duration=0, trial_type="stop")

    events = [start, presentation, stop, test]

    handler = bids.BIDSHandler(
        dataset=example_dataset,
        subject=subject["participant_id"],
        task="task1",
    )
    handler.createDataset()

    handler.addEvent(events)

    handler.writeEvents(participant_info=subject, event_type="task")
    print(handler._BIDSHandler__events)

def test_doc_strings():
    """
    Test docstrings using doctest and pytest.
    """
    results = doctest.testmod(
        bids.bidshandler,
        globs={
            "bids": bids,
        }
    )

    assert results.failed == 0, f"{results.failed} doctests failed out of {results.attempted}."