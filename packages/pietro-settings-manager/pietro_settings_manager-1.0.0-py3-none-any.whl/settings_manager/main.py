from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Literal


class SettingsManager:
	"""
	A class to handle configuration settings using an INI file.
	Provides methods to load, save, get, and set configuration values.
	"""
	
	file_path: Path  # Path to the configuration file
	parser = ConfigParser()  # INI file parser
	_defaults: Dict[str, Dict[str, Any]]  # Default configuration values
	
	def __init__(self, file_name: str = "settings.ini", defaults: Dict[str, Dict[str, Any]] = None):
		"""
		Initialize the Settings Manager.

		:param file_name: Name of the configuration file.
		:param defaults: Default configuration values structured as a nested dictionary.
		"""
		self._defaults = defaults
		self.file_path = Path(file_name)
	
	def _apply_defaults(self) -> None:
		"""
		Apply default settings to the configuration if the file does not exist.
		"""
		for section, options in self._defaults.items():
			if not self.parser.has_section(section):
				self.parser.add_section(section)
			for key, value in options.items():
				if not self.parser.has_option(section, key):
					self.set(section, key, value)
	
	def load(self) -> None:
		"""
		Load the configuration from the settings file.
		If the file does not exist, apply the default settings and save them.
		"""
		if self.file_path.exists():
			self.parser.read(self.file_path)
		else:
			self._apply_defaults()
			self.save()
	
	def save(self) -> None:
		"""
		Save the current configuration settings to the file.
		"""
		with self.file_path.open("w") as config_file:
			self.parser.write(config_file)
	
	def get(
		self,
		section: str,
		option: str,
		_as: Literal["bool", "int", "float", "list", "dict"] = None
	) -> Any:
		"""
		Retrieve a configuration value and convert it to the desired type if specified.

		:param section: The section in the configuration file.
		:param option: The key within the section.
		:param _as: Optional type conversion (bool, int, float, list, dict).
		:return: The retrieved value, converted if necessary.
		"""
		self.load()
		try:
			match _as:
				case "bool":
					return self.parser.getboolean(section, option)
				case "int":
					return self.parser.getint(section, option)
				case "float":
					return self.parser.getfloat(section, option)
				case _:  # Default to string
					return self.parser.get(section, option)
		except Exception as e:
			raise ValueError(f"Error reading '{option}' in section '{section}': {e}.")
	
	def set(self, section: str, key: str, value: Any) -> None:
		"""
		Set a configuration value, ensuring the section exists before setting the key-value pair.

		:param section: The section in which to store the key-value pair.
		:param key: The configuration key.
		:param value: The value to be stored, which will be converted to a string.
		"""
		if not self.parser.has_section(section):
			self.parser.add_section(section)
		
		if isinstance(value, bool):
			self.parser.set(section, key, "yes" if value else "no")
		else:
			self.parser.set(section, key, str(value))  # Store all values as strings
		
		self.save()