# SettingsManager

A simple Python class for managing configuration settings using an INI file. The class provides methods to load, save, get, and set configuration values, with support for default settings and type conversion.

## Features

- Load and save settings from/to an INI file.
- Apply default settings if the configuration file does not exist.
- Get configuration values with optional type conversion (`bool`, `int`, `float`).
- Set configuration values, ensuring the section exists before setting the key-value pair.
- Uses Python's `configparser` module for parsing INI files.

## Installation

You can install the package via pip (once it's published to PyPi):

```bash
pip install settingsmanager
```