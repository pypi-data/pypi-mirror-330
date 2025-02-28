# SettingsManager

A simple Python class for managing configuration settings using an INI file. The class provides methods to load, save, get, and set configuration values, with support for default settings and type conversion.

## Features

- Load and save settings from/to an INI file.
- Apply default settings if the configuration file does not exist.
- Get configuration values with optional type conversion (`bool`, `int`, `float`).
- Set configuration values, ensuring the section exists before setting the key-value pair.
- Uses Python's `configparser` module for parsing INI files.

## Usage

```py
# Define default configuration values
default_config = {
	"general": {
		"theme": "light",  # Default theme
		"language": "en",  # Default language
		"notifications_enabled": True  # Enable notifications by default
	},
	"user": {
		"username": "default_user",  # Default username
		"email": "user@example.com"  # Default email address
	}
}

# Create an instance of SettingsManager with a specific config file and default values
settings_manager = SettingsManager(file_name="my_config.ini", defaults=default_config)

# Load configuration from the file (if it exists) or apply the default values
settings_manager.load()

# Retrieve configuration values using the 'get' method
theme = settings_manager.get("general", "theme")  # Get the theme value
language = settings_manager.get("general", "language")  # Get the language value
notifications_enabled = settings_manager.get("general", "notifications_enabled", "bool")  # Get notifications status as a boolean

# Print the retrieved configuration values
print(f"Theme: {theme}")
print(f"Language: {language}")
print(f"Notifications enabled: {notifications_enabled}")

# Change some configuration values
settings_manager.set("general", "theme", "dark")  # Change theme to dark
settings_manager.set("user", "username", "new_user")  # Change username

# Save the changes to the configuration file
settings_manager.save()
```