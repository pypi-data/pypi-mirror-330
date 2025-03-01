# OpenDRIVE BSSD Converter

> **IMPORTANT NOTE** This repository is part of the _Behavior-Semantic Scenery Description (BSSD)_ framework. Check out our BSSD documentation and overview repository in your git of choice:
[![GitLab](https://img.shields.io/badge/GitLab-330F63?style=flat&logo=gitlab&logoColor=white)](https://gitlab.com/tuda-fzd/scenery-representations-and-maps/behavior-semantic-scenery-description)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/TUDa-FZD/Behavior-Semantic-Scenery-Description)

Tool for integrating BSSD-data into an existing OpenDRIVE-file (.xodr) with Version 1.4, 1.5, 1.6 or 1.7.

## Requirements

 - Python (Tool has been tested with Python 3.7, 3.8 and 3.9)
 - The following Python-modules are needed:
	 - easygui==0.98.1
	 - lxml==4.6.3
	 - pandas==1.3.4
	 - rich==10.16.2
	 - scipy==1.7.1
	 - tqdm==4.62.3
   - importlib_resources

The tool has been tested with the versions of the modules specified in the list above. It may also work with other module-versions, but the correct functionality can't be guaranteed in this case.

**Hint**: Some parts of the visualiziation of the tool in the terminal are based on the python package [rich](https://rich.readthedocs.io/en/stable/introduction.html). In some terminals on Windows the full visualization of *rich* does not work properly (e.g. *PowerShell*, *cmd*). Nevertheless, everything will be displayed so that the correct functionality is guaranteed.

In Windows for a full visualiziation with *rich*, the use of the  [Windows-Terminal](https://www.microsoft.com/de-de/p/windows-terminal/9n0dx20hk701) is recommended. In macOS (*Terminal*) and Linux (*Terminal*) the full visualization should work properly.


## Installation
### Using pip
```bash
pip install opendrive-bssd-converter
```
This will install the latest version of the OpenDRIVE-BSSD-Converter available in [PyPI](https://pypi.org/project/opendrive-bssd-converter/) to your environment.

### Manual Installation

Clone the source code to a directory of your choice (```path/to/opendrive-bssd-converter-src/```).

If you are using virtual environments, make sure to activate the correct environment to install the library into e.g:

```bash
source /<path-to-my-project>/.venv/bin/activate
```

Install the library:
```bash
pip install -e path/to/opendrive-bssd-converter-src/
```

## Usage
1. Start the tool: Run
   ```bash
   opendrive-bssd-converter
   ```
2. If the tool started successfully, you can choose your OpenDRIVE-file in the window, which opens immediately after executing.
3. You will be able to modify the behaviour of the tool thoughout the process, therefore watch the terminal for prompts and provide your input.
4. After successfully executing the tool, the modified OpenDRIVE-file will be stored in the same folder as the original OpenDRIVE-file with the same name plus the suffix "_BSSD".
