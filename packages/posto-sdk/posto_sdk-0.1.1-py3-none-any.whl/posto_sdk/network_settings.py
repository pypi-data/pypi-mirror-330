from typing import Dict, Any, Optional, List
import json
import os
from dataclasses import dataclass
from enum import Enum

@dataclass
class NetworkCapabilities:
    """Network capabilities configuration"""
    supports_media: bool
    supports_scheduling: bool
    supported_media_types: Optional[List[str]] = None
    max_media_items: Optional[int] = None
    supports_stories: bool = False
    supports_first_comment: bool = False
    supports_privacy_levels: bool = False
    max_text_length: Optional[int] = None
    required_media: bool = False

class NetworkSettings:
    """Handles network-specific settings and capabilities"""
    
    def __init__(self, settings_file: Optional[str] = None):
        """Initialize network settings
        
        Args:
            settings_file: Path to network settings JSON file. If None, uses default settings.json from root
        """
        if settings_file is None:
            # Look for settings.json in the root directory (one level up from package directory)
            settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
        self._settings = self._load_settings(settings_file)
        
    def _load_settings(self, settings_file: str) -> Dict:
        """Load settings from JSON file"""
        if not os.path.exists(settings_file):
            raise FileNotFoundError(f"Settings file not found: {settings_file}")
            
        with open(settings_file, 'r') as f:
            return json.load(f)
            
    def get_network_settings(self, network: str) -> Dict[str, Any]:
        """Get settings for a specific network
        
        Args:
            network: Network name (e.g. 'facebook', 'twitter')
            
        Returns:
            Dictionary containing network settings
        """
        network = network.lower()
        if network not in self._settings:
            raise ValueError(f"Network '{network}' not found in settings")
        return self._settings[network]
        
    def get_default_value(self, network: str, setting: str) -> Any:
        """Get default value for a network setting
        
        Args:
            network: Network name
            setting: Setting name
            
        Returns:
            Default value for the setting
        """
        settings = self.get_network_settings(network)
        if 'default_values' not in settings or setting not in settings['default_values']:
            raise ValueError(f"Setting '{setting}' not found for network '{network}'")
        return settings['default_values'][setting]['default']
        
    def get_capabilities(self, network: str) -> NetworkCapabilities:
        """Get capabilities for a specific network
        
        Args:
            network: Network name
            
        Returns:
            NetworkCapabilities object
        """
        settings = self.get_network_settings(network)
        caps = settings.get('capabilities', {})
        
        return NetworkCapabilities(
            supports_media=caps.get('supports_media', False),
            supports_scheduling=caps.get('supports_scheduling', False),
            supported_media_types=caps.get('supported_media_types'),
            max_media_items=caps.get('max_media_items'),
            supports_stories=caps.get('supports_stories', False),
            supports_first_comment=caps.get('supports_first_comment', False),
            supports_privacy_levels=caps.get('supports_privacy_levels', False),
            max_text_length=caps.get('max_text_length'),
            required_media=caps.get('required_media', False)
        )
        
    def get_setting_type(self, network: str, setting: str) -> str:
        """Get the type of a setting for a network
        
        Args:
            network: Network name
            setting: Setting name
            
        Returns:
            Setting type (e.g. 'boolean', 'string', 'enum')
        """
        settings = self.get_network_settings(network)
        if 'setting_types' not in settings or setting not in settings['setting_types']:
            raise ValueError(f"Setting type for '{setting}' not found in network '{network}'")
        return settings['setting_types'][setting]
        
    def get_setting_description(self, network: str, setting: str) -> str:
        """Get description for a network setting
        
        Args:
            network: Network name
            setting: Setting name
            
        Returns:
            Setting description or empty string if not found
        """
        settings = self.get_network_settings(network)
        return settings.get('setting_descriptions', {}).get(setting, "")
        
    def get_enum_values(self, network: str, enum_name: str) -> List[str]:
        """Get possible values for an enum setting
        
        Args:
            network: Network name
            enum_name: Name of the enum
            
        Returns:
            List of possible enum values
        """
        settings = self.get_network_settings(network)
        if 'enums' not in settings or enum_name not in settings['enums']:
            raise ValueError(f"Enum '{enum_name}' not found for network '{network}'")
        return settings['enums'][enum_name]
        
    def validate_setting(self, network: str, setting: str, value: Any) -> bool:
        """Validate a setting value against its type definition
        
        Args:
            network: Network name
            setting: Setting name
            value: Value to validate
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        setting_type = self.get_setting_type(network, setting)
        
        if setting_type == 'boolean' and not isinstance(value, bool):
            raise ValueError(f"Setting '{setting}' must be a boolean")
            
        elif setting_type == 'string' and not isinstance(value, str):
            raise ValueError(f"Setting '{setting}' must be a string")
            
        elif setting_type == 'integer' and not isinstance(value, int):
            raise ValueError(f"Setting '{setting}' must be an integer")
            
        elif setting_type == 'enum':
            # Find the enum name from the setting name
            enum_name = None
            settings = self.get_network_settings(network)
            for e_name, e_values in settings.get('enums', {}).items():
                if setting.endswith(e_name):
                    enum_name = e_name
                    break
                    
            if enum_name and value not in self.get_enum_values(network, enum_name):
                valid_values = self.get_enum_values(network, enum_name)
                raise ValueError(f"Invalid value for '{setting}'. Must be one of: {valid_values}")
                
        return True
        
    def check_setting_dependencies(self, network: str, settings: Dict[str, Any]) -> None:
        """Check if setting dependencies are satisfied
        
        Args:
            network: Network name
            settings: Dictionary of settings to check
            
        Raises:
            ValueError if dependencies are not satisfied
        """
        network_settings = self.get_network_settings(network)
        dependencies = network_settings.get('setting_dependencies', {})
        
        for setting, dependency in dependencies.items():
            if setting in settings:
                depends_on = dependency['depends_on']
                condition = dependency['condition']
                
                if depends_on not in settings:
                    raise ValueError(f"Setting '{setting}' depends on '{depends_on}' which is not provided")
                    
                # Simple condition evaluation (only supports "value == True/False" for now)
                if "value == True" in condition and not settings[depends_on]:
                    raise ValueError(f"Setting '{setting}' requires '{depends_on}' to be True")
                elif "value == False" in condition and settings[depends_on]:
                    raise ValueError(f"Setting '{setting}' requires '{depends_on}' to be False") 