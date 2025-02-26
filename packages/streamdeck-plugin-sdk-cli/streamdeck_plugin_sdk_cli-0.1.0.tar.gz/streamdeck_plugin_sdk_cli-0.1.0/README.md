# Python StreamDeck Plugin SDK CLI

A command-line interface (CLI) tool for packaging Elgato Stream Deck plugins. This tool helps automate the process of creating plugin packages using the [Python plugin SDK](https://github.com/strohganoff/python-streamdeck-plugin-sdk) library.

## Features

- Create a fresh Python plugin project with scaffolding provided by a template.
- Validate a plugin's structure.
- Pack Stream Deck plugins into distributable .streamDeckPlugin files
- Support for `.packignore` file to exclude unwanted files/directories
- Automatic plugin UUID directory structure creation

## Installation

To install the required dependencies, run:
```bash
pip install streamdeck-plugin-sdk-cli
```

## Usage

### Create a New Plugin
To create a new Stream Deck plugin project, run:
```bash
streamdeck-cli create
```

This will create a new project at the current directory from the template at https://github.com/strohganoff/python-streamdeck-plugin-template.git.


### Validate a Plugin
To validate the plugin manifest and directory structure, run:
```bash
streamdeck-cli validate /path/to/plugin
```

Note that the manifest.json file must be updated and saved as a proper json file (no comments) to pass validation.

### Pack a Plugin
To pack the plugin into a .streamDeckPlugin file, run:
```bash
streamdeck-cli pack /path/to/plugin --output /path/to/output
```

If you don't pass in a version argument, the script will automatically look up the plugin version in the manifest.json file to place the release package into a directory named for that version under the specified output directory.

If there is already a release directory with that version, the script will handle giving a subversion (or incrementing the subversion) to apply to the directory name.
So if a version '0.0.1' has already been packed, a new release directory will be saved to named '0.0.1-1', but the version in the manifest.json file will be unchanged.
If a release was already saved to directory '0.0.1-1', then a new release directory will be saved to named '0.0.1-2'.

#### Next Step
Simply double-click the .streamDeckPlugin file, which will load up the plugin in the Stream Deck application.

#### Pack for debug mode
To pack the plugin in debug mode, which enables remote debugging capabilities, use the `--debug` flag:

```bash
streamdeck-cli pack /path/to/plugin --debug --debug-port 5679
```

This will create a flag file named `.debug` in the packed plugin containing the specified port.

When this file is included, the plugin will wait for a debugger to attach at that port before starting. You can use tools like VS Code's Python debugger or PyCharm's remote debugger to connect to it.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

