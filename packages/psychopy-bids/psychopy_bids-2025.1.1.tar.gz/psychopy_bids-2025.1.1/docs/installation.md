# Installation

## pip install (Linux, macOS & Windows)

This method should work with a number of Python versions, but **we strongly recommend that you use Python 3.10**. Older Python versions are no longer tested and may not work correctly. Newer Python versions may not have wheels for all required dependencies. For Linux the [install script](#install-script-linux) is recommended.

You can install psychopy-bids and its dependencies by:

```console
pip install psychopy-bids
```

For further information on pip visit [pip install - pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/).

## Standalone PsychoPy (macOS & Windows)

For the simplest installation, download and install the standalone package. You can find all versions on [PsychoPy releases on github](https://github.com/psychopy/psychopy/releases). **Use at least version 2024.1.0 or later**.

First, start PsychoPy and select **Plugin/packages manager...** from the Tools menu.

![Tools](image/installation/inst-fig01.png)

There are now three different ways in which you can install psychopy-bids.

![Plugins & Packages](image/installation/inst-fig02.png)

- **Option 1 - Search package (Recommended):** Search for _psychopy-bids_ using the search bar. Then select the package below, decide which version you want to install and click _Install_ to complete the process.
- **Option 2 - Open PIP terminal:** Click _Open PIP terminal_, type `pip install psychopy-bids` into the command prompt and wait for the package to install successfully.

### Older Standalone PsychoPy versions (Windows)

If you are using a standalone PsychoPy version older than 2023.1.0, you need to install psychopy-bids differently. First, open your terminal. To do this

1. Select the Start button.
2. Type "cmd".
3. Select Command Prompt from the list.

To avoid possible problems, it is best to start Command Prompt as administrator.

![Command Prompt](image/installation/inst-fig03.png)

To install **psychopy-bids** use `"<path>\python.exe" -m pip install psychopy-bids`. If you have installed PsychoPy to the standard installation folder, your path is most likely going to be `C:\Program Files\PsychoPy`. In this case, you would run the command `"C:\Program Files\PsychoPy\python.exe" -m pip install psychopy-bids`.

## Install script (Linux)

```bash
 curl -O https://raw.githubusercontent.com/wieluk/psychopy_linux_installer/main/psychopy_linux_installer
 chmod +x psychopy_linux_installer
 ./psychopy_linux_installer --additional-packages==psychopy-bids,seedir
```

[More information on GitHub](https://github.com/wieluk/psychopy_linux_installer)

## Post-Installation Steps

### Use the Components

As shown in the figure below, the **BIDS Event component** and the **BIDS Export routine** are now available and ready for use.

Please note that the **BIDS Beh Event component** and the **BIDS Task Event component** are now deprecated and will be removed from the builder in the future. They remain available temporarily for backward compatibility purposes only.

![PsychoPyBuilder](image/installation/inst-fig05.png)
