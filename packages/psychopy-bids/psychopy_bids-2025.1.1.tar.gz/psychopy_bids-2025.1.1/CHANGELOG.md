## 2025.1.0 (2025-01-30)

### Fixed

- [Ensure `addEnvironment()` correctly handles duplicate packages with different versions](https://gitlab.com/psygraz/psychopy-bids/-/commit/eeb8d3b53e5139d92ae13d3ea729baa3169b6eec).  
- Fixed Windows version parsing: Updated the underlying function to correctly detect and parse Windows 11, Linux and MacOS versions  

### Changed

- [Replaced `writeBehEvents` and `writeTaskEvents` with a unified `writeEvents`](https://gitlab.com/psygraz/psychopy-bids/-/commit/4f18c28ba5e8e0c2bd99daebf08a91a6fa106d6b) ([merge request](https://gitlab.com/psygraz/psychopy-bids/-/merge_requests/74)).  
  - See the updated [writeEvents documentation](https://psychopy-bids.readthedocs.io/en/stable/bidshandler/#psychopy_bids.bids.BIDSHandler.writeEvents).  
- Removed `addJSONSidecar` and `addStimuliFolder` in favor of `_addJSONSidecar` and `_addStimuliFolder`, which are now used via `writeEvents`.   
- Moved `BIDSError` class into a separate file (`bidserror.py`).  
- Added `HEDtools` as a dependency to use `TabularSummary`.  
- Improved docstrings for better clarity and maintainability.  
- Removed `__del__` (may be reintroduced via **builder hooks**).  
- Removed incompatible data types from `data_type`.  
- `addEvent` now accepts either a single event or a list of events.  
- Refactored multiple methods to use private helper functions for better modularity.  
- Removed `psychopy` as a dependency from `pyproject.toml`.  
- Migrated test framework from `unittest` to `pytest` for improved testing.   

### Builder Changes

- Improved tooltips for better usability.  
- Renamed `hed` to `HED` (`"HED Tags (Sidecar Preferred)"`) in **BidsEvent** to ensure HED tags comply with **BIDS standards**.  
  - ⚠️ This change will invalidate all existing hed tags in the builder.  
  - **Expected impact**: Users should use the `.json` sidecar in **BidsExport**, as strongly recommended.  
- Added **Events/Beh Sidecar path** option in **BidsExport** for more flexible data handling.  

## 2024.2.2 (2025-01-09)

### fixed (1 change)

- [Generate requirements.txt using Pythonic package discovery instead of pip freeze and subprocess](https://gitlab.com/psygraz/psychopy-bids/-/commit/751cb70cf967003a38c1447064227f135396fa6e) ([merge request](https://gitlab.com/psygraz/psychopy-bids/-/merge_requests/76))


## v2024.2.0

### Added
- addEnvironment function to create `requirements.txt` in BIDS dataset.
- addTaskCode function for adding task code to BIDS dataset.
- BIDS compliance for `psychopy-bids` output, integrated `bids-validator` into the testing stage.
- Enhanced `addStimuliFolder` to accept paths starting with `stimuli/`.
- Added markdown codeblocks support to `pytest`.

### Changed
- Dynamic release versions now based on tags.
- Removed duplicate code lines when logging events in builder.

### Deprecated
- BidsBehEventComponent and BidsTaskEventComponent are deprecated in favor of BidsEventComponent

### Fixed
- Resolved warnings in `pytest`.
- Duplicate events.tsv and .json files on one run with `Add Runs to event filename` checked

### Documentation
- Many sections of the Builder documentation have been marked as deprecated but are still retained for reference purposes. These sections require updates to ensure accuracy and alignment with the latest features and practices.


### v2024.1.4

- Restored support for Python 3.8 and 3.9
- Minimum Python version requirement is now Python 3.8
- Expanded testing to include Python 3.8 and 3.9
- Improved bidshandler.__del__ error handling

### v2024.1.3

- Updated documentation to reflect the current state of the project.

## v2024.1.2 (2024/11/15)

### Added

### Changed

- Switching the package development from poetry to setuptools to be able to address the PsychoPy plugin system.
- BIDSHandler also creates the folder structure in the event of an interrupt.
- Renamed pypi package to psychopy-bids
- Improved CI/CD pipeline

### Deprecated

### Removed

- The function addBuilderElements() was removed due to the successful integration into the PsychoPy plugin system.

### Fixed

- Changed the default values for the event components from None to ''.
- Changed the file LICENCE to LICENSE.
- Fixed the naming problem by renaming the events object to bids_event.
- Removed all unnecessary folders and files from the package.
- Fixed the broken API reference.
- Fixed Builder GUI not displaying BIDS on linux-based-systems

### Security

### Documentation

- Updated the CHANGELOG.
- Updated the "Installation" section.
- Added a short "Getting Started" to the Builder tutorial.

### Miscellaneous

## v2023.2.0 (2023/12/05)

### Added

- Addition of the class `BIDSBehEvent` for the possibility of a more general event class.
- Addition of the class `BIDSBehEventComponent` to make BIDSBehEvents available as a component in PsychoPy Builder.
- Introduced the function addBehEvents() in class `BIDSHandler`.
- Introduced the function addChanges() in class `BIDSHandler`.
- Introduced the function addReadme() in class `BIDSHandler`.
- Introduced the function addLicense() in class `BIDSHandler`.
- Introduced the function addDatasetDescription() in class `BIDSHandler`.

### Changed

- Added column description to the function addJSONSidecar().
- Added a list of licenses to the `BidsExportRoutine`.
- Added the parameter force to createDataset().

### Deprecated

- The function addBuilderElements() will be removed as soon as the integration into the plugin system works.

### Fixed

- Fixed the collapse of `BidsExportRoutine` due to an incorrect indentation level.
- Fixed warning in addTaskEvent() by using pandas.concat.

## v2023.1.1 (2023/03/09/)

### Fixed

- Fixed the incorrect copy path for shutil in function addStimuliFolder().

## v2023.1.0 (2023/02/28)

### Added

- Added the usage of custom columns in the BIDSTaskEvent class.
- Added the usage of custom columns in the BIDSTaskEvent Builder component.

### Changed

- Updated unit tests for BIDSTaskEvent & BIDSHandler.

### Fixed

- Updated to basename for stim_file path in function addStimuliFolder().
- Added parameter path in function addStimuliFolder().
- Fixed the issue with overwriting the StimulusPresentation section in function addJSONSidecar().
- Fixed the issue with an empty dataset name in function createDataset().
- Fixed the issue  with saving the wrong value in class `BIDSTaskEvent`.

## v0.1.4 (2022/10/07)

### Added

- Added exception handling to bidstaskevent.py.

### Fixed

- Fixed KeyError if no `BIDSTaskEvents` are present for `BIDSHandler`.
- Fixed Error if properties of a `BIDSTaskEvent` are not correct.

## v0.1.3 (2022/09/21)

### Fixed

- Fixed the class `BidsExportRoutine` for the PsychoPy Builder.

## v0.1.2 (2022/09/20)

### Fixed

- Fixed the broken addBuilderElements() function.

## v0.1.1 (2022/09/20)

### Added

- Added function addBuilderElements() to get `BidsEventComponent` and `BidsExportRoutine` into PsychoPy Builder.

### Changed

- Updated the  CI/CD configuration file .gitlab-ci.yml.

### Fixed

- Fixed a few linting issues.

### Documentation

- Updated the documentations requirements.

## v0.1.0 (2022/09/06)

### Added

- Class `BIDSHandler` in the module `bids` to handle the BIDSTaskEvents saved in the PsychoPy ExperimentHandler.
- Class `BIDSTaskEvent` in the module `bids` to save TaskEvents in the BIDS data structure.
- Class `BidsEventComponent` in the module `bids_event` to make BIDSTaskEvents available as a component in PsychoPy Builder.
- Class `BidsExportRoutine` in the module `bids_settings` to enable the creation of valid BIDS datasets in PsychoPy Builder.

### Documentation

- A first small sphinx-based introduction.

### Miscellaneous

- First release of `psychopy_bids`.
