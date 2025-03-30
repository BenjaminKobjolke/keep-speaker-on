"""
Settings handler for the application.
"""
import configparser
import os
import logging
from typing import Dict, Any


class Settings:
    """
    Class to handle application settings from settings.ini file.
    """
    def __init__(self, config_file: str = "settings.ini"):
        """
        Initialize Settings with the given config file.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        # Default settings
        self.defaults = {
            'Settings': {
                'interval_minutes': '5'
            },
            'Logging': {
                'log_level': 'INFO',
                'log_file': 'app.log'
            }
        }
        
        self.load_config()
    
    def load_config(self) -> None:
        """
        Load configuration from the config file.
        If settings.ini doesn't exist but settings_example.ini does, copy from example.
        If neither exists, create settings.ini with default values.
        """
        example_config = "settings_example.ini"
        
        if not os.path.exists(self.config_file):
            if os.path.exists(example_config):
                logging.info(f"Creating {self.config_file} from {example_config}")
                # Copy from example
                example = configparser.ConfigParser()
                example.read(example_config)
                
                # Create new config with example values
                self.config = example
                
                # Save to settings.ini
                with open(self.config_file, 'w') as f:
                    self.config.write(f)
            else:
                # No example found, create with defaults
                self._create_default_config()
        
        try:
            self.config.read(self.config_file)
        except configparser.Error as e:
            logging.error(f"Error reading config file: {e}")
            self._set_defaults()
    
    def _create_default_config(self) -> None:
        """Create a default configuration file."""
        self._set_defaults()
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def _set_defaults(self) -> None:
        """Set default values for configuration."""
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            for option, value in options.items():
                self.config.set(section, option, value)
    
    def get(self, section: str, option: str, fallback: Any = None) -> str:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            option: Option name
            fallback: Fallback value if option is not found
            
        Returns:
            The configuration value as a string
        """
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            
            # Try to get from defaults
            try:
                return self.defaults[section][option]
            except KeyError:
                logging.warning(f"Configuration {section}.{option} not found")
                return ""
    
    def get_int(self, section: str, option: str, fallback: int = None) -> int:
        """
        Get a configuration value as an integer.
        
        Args:
            section: Configuration section
            option: Option name
            fallback: Fallback value if option is not found or not an integer
            
        Returns:
            The configuration value as an integer
        """
        try:
            return self.config.getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            if fallback is not None:
                return fallback
            
            # Try to get from defaults
            try:
                return int(self.defaults[section][option])
            except (KeyError, ValueError):
                logging.warning(f"Configuration {section}.{option} not found or not an integer")
                return 0
    
    def get_float(self, section: str, option: str, fallback: float = None) -> float:
        """
        Get a configuration value as a float.
        
        Args:
            section: Configuration section
            option: Option name
            fallback: Fallback value if option is not found or not a float
            
        Returns:
            The configuration value as a float
        """
        try:
            return self.config.getfloat(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            if fallback is not None:
                return fallback
            
            # Try to get from defaults
            try:
                return float(self.defaults[section][option])
            except (KeyError, ValueError):
                logging.warning(f"Configuration {section}.{option} not found or not a float")
                return 0.0
    
    def get_boolean(self, section: str, option: str, fallback: bool = None) -> bool:
        """
        Get a configuration value as a boolean.
        
        Args:
            section: Configuration section
            option: Option name
            fallback: Fallback value if option is not found or not a boolean
            
        Returns:
            The configuration value as a boolean
        """
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            if fallback is not None:
                return fallback
            
            # Try to get from defaults
            try:
                return self.config.getboolean(self.defaults[section][option])
            except (KeyError, ValueError):
                logging.warning(f"Configuration {section}.{option} not found or not a boolean")
                return False
    
    def get_interval_minutes(self) -> int:
        """
        Get the interval in minutes between audio playback.
        
        Returns:
            The interval in minutes as an integer
        """
        return self.get_int('Settings', 'interval_minutes', 5)
    
    def get_log_level(self) -> str:
        """
        Get the log level.
        
        Returns:
            The log level as a string
        """
        return self.get('Logging', 'log_level', 'INFO')
    
    def get_log_file(self) -> str:
        """
        Get the log file path.
        
        Returns:
            The log file path as a string
        """
        return self.get('Logging', 'log_file', 'app.log')
