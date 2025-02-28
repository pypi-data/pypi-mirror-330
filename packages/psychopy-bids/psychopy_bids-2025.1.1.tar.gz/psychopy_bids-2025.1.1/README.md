# psychopy-bids

A [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/).


- **[Website](https://psygraz.gitlab.io/psychopy-bids)**  
- **[Documentation](https://psychopy-bids.readthedocs.io/)**  
- **[Source Code](https://gitlab.com/psygraz/psychopy-bids)**  
- **[Report Issues](https://gitlab.com/psygraz/psychopy-bids/issues)**  
- **[Contributing Guidelines](https://gitlab.com/psygraz/psychopy-bids/-/blob/main/CONTRIBUTING.md)**  
- **[Code of Conduct](https://gitlab.com/psygraz/psychopy-bids/-/blob/main/CONDUCT.md)**  
- **[PyPI Package](https://pypi.org/project/psychopy-bids/)**  

---

## ⚠️ **Breaking Changes in v2025** ⚠️  

This release introduces breaking changes that may affect your existing workflows. It is highly recommended to always use the same version of `psychopy-bids` for experiments that have already been written. If an experiment was created with a specific version of `psychopy-bids` (e.g., `vX.X.X`), you should continue using that version to ensure compatibility and reproducibility. Only upgrade to a newer version for new experiments.

Please review the following resources for detailed information:

- **[Changelog](https://gitlab.com/psygraz/psychopy-bids/-/blob/main/CHANGELOG.md)**

---

## Installation

We recommend installation in a virtual environment.

```console
pip install psychopy-bids
```

---

## Usage

The psychopy bids plugin can be used to create valid BIDS valid datasets by creating [behavioral](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/behavioral-experiments.html#example-_behtsv) or [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in Psychopy. This can be done directly in python code or using the psychopy builder.

In code, the *BIDSHandler* can create or extend an existing BIDS dataset, including directory structure and necessary metadata files. Individual BIDS events can be added during the experiment and are passed to the *BIDSHandler* to write event `.tsv` files and accompanying `.json` files.

```py
from psychopy_bids import bids

handler = bids.BIDSHandler(dataset="example_dataset", subject="01", task="A")
handler.createDataset()

events = [
    bids.BIDSTaskEvent(onset=1.0, duration=0.5, event_type="stimulus", response="correct"),
    bids.BIDSTaskEvent(onset=1.0, duration=0, trial_type="trigger")
]

handler.addEvent(events)

participant_info = {"participant_id": handler.subject, "age": 18}

handler.writeEvents(participant_info=participant_info)
handler.addEnvironment()
```

---

## Contributing

Interested in contributing? Check out the [contributing guidelines](https://gitlab.com/psygraz/psychopy-bids/-/blob/main/CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](https://gitlab.com/psygraz/psychopy-bids/-/blob/main/CONDUCT.md). By contributing to this project, you agree to abide by its terms.

---

## License

`psychopy-bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.

---

## Credits

`psychopy-bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
