from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import logging
from .api_utils import APIClient, ENDPOINTS

logger = logging.getLogger("PostoSDK")

@dataclass
class NetworkSettings:
    """Handles network-specific settings and capabilities"""
    
    def __init__(self, network_type: str, settings_data: Dict[str, Any]):
        self.network_type = network_type
        self.settings_data = settings_data
        self.available_settings = self._parse_available_settings()
        
    def _parse_available_settings(self) -> Dict[str, Any]:
        """Parse available settings from the backend data"""
        if not self.settings_data:
            return {}
            
        # Handle simple key-value format from API
        settings = {}
        for key, value in self.settings_data.items():
            settings[key] = {
                'type': type(value).__name__,
                'default': value,
                'required': False,  # API doesn't specify this, assume optional
                'current_value': value
            }
        return settings
    
    def get_available_settings(self) -> Dict[str, Any]:
        """Get all available settings for this network"""
        return {
            key: info['current_value'] 
            for key, info in self.available_settings.items()
        }
    
    def validate_settings(self, settings: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate settings against network requirements"""
        errors = []
        
        for key, value in settings.items():
            if key not in self.available_settings:
                continue  # Allow extra settings
                
            setting_info = self.available_settings[key]
            
            # Validate type
            expected_type = setting_info['type']
            if expected_type and not isinstance(value, eval(expected_type)):
                errors.append(f"Setting '{key}' should be of type {expected_type}")
        
        return len(errors) == 0, errors
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default values for all settings"""
        return {
            key: info['default']
            for key, info in self.available_settings.items()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary for API requests"""
        return self.get_available_settings()

@dataclass
class NetworkCapabilities:
    """Network capabilities from the API"""
    supports_media: bool = True
    supports_scheduling: bool = True
    max_media_items: Optional[int] = None
    supported_media_types: Optional[List[str]] = None
    max_text_length: Optional[int] = None
    supports_link_attachment: bool = True

class NetworkSettingsManager(APIClient):
    """Manages network settings and capabilities"""
    
    def __init__(self, base_url: str, auth_token: str):
        """Initialize the settings manager
        
        Args:
            base_url: Base URL of the WordPress instance
            auth_token: Authentication token
        """
        super().__init__(base_url, auth_token)
        self._settings_cache: Dict[str, NetworkSettings] = {}
        self._capabilities_cache: Dict[str, NetworkCapabilities] = {}
        self._profiles: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
    def validate_network_settings(self, network: str, settings: Dict[str, Any]) -> None:
        """Validate network settings
        
        Args:
            network: Network identifier
            settings: Settings to validate
            
        Raises:
            ValueError: If settings are invalid
        """
        if not isinstance(settings, dict):
            raise ValueError("Settings must be a dictionary")
            
        # Get network capabilities
        capabilities = self.get_network_capabilities(network)
        
        # Validate against capabilities
        if 'post_text' in settings and capabilities.max_text_length:
            if len(settings['post_text']) > capabilities.max_text_length:
                raise ValueError(f"Post text exceeds maximum length of {capabilities.max_text_length}")
                
        if settings.get('upload_media') and not capabilities.supports_media:
            raise ValueError("Network does not support media uploads")
            
        # Set defaults for missing required fields
        if 'post_text' not in settings:
            settings['post_text'] = "{post_title}"
        
    def get_available_networks(self) -> List[Dict[str, Any]]:
        """Get list of available social networks
        
        Returns:
            List of dictionaries containing network information
        """
        data = self._make_request('GET', ENDPOINTS['channels'])
        networks = []
        
        # Extract unique networks from channels
        seen = set()
        for channel in data.get('channels', []):
            network = channel.get('social_network')
            if network and network not in seen:
                networks.append({
                    "slug": network,
                    "name": channel.get('network_name', network.title()),
                    "icon": channel.get('network_icon', ''),
                    "enabled": True
                })
                seen.add(network)
                
        return networks
        
    def get_network_settings(self, network: str) -> NetworkSettings:
        """Get settings for a specific network
        
        Args:
            network: Network identifier
            
        Returns:
            NetworkSettings object
        """
        if network in self._settings_cache:
            return self._settings_cache[network]
            
        data = self._make_request('GET', ENDPOINTS['network_settings'](network))
        settings = NetworkSettings(network, data)
        self._settings_cache[network] = settings
        
        return settings
        
    def save_network_settings(self, network: str, settings: Dict[str, Any]) -> None:
        """Save settings for a specific network
        
        Args:
            network: Network identifier
            settings: Settings to save
        """
        # Convert NetworkSettings object to dict if needed
        if isinstance(settings, NetworkSettings):
            settings = settings.to_dict()
            
        # Validate settings before saving
        self.validate_network_settings(network, settings)
        
        self._make_request('POST', ENDPOINTS['network_settings'](network), json=settings)
        
        # Update cache if successful
        if network in self._settings_cache:
            self._settings_cache[network] = NetworkSettings(network, settings)
    
    def get_network_capabilities(self, network: str) -> NetworkCapabilities:
        """Get capabilities for a specific network
        
        Args:
            network: Network identifier
            
        Returns:
            NetworkCapabilities object
        """
        if network in self._capabilities_cache:
            return self._capabilities_cache[network]
            
        # For now, return default capabilities
        # In the future, this could fetch from API
        capabilities = NetworkCapabilities()
        self._capabilities_cache[network] = capabilities
        
        return capabilities
    
    def save_settings_profile(self, name: str, settings: Dict[str, Dict[str, Any]]) -> None:
        """Save a network settings profile
        
        Args:
            name: Profile name
            settings: Settings for each network
        """
        # Validate settings for each network
        for network, network_settings in settings.items():
            self.validate_network_settings(network, network_settings)
        
        self._profiles[name] = settings
    
    def get_settings_profile(self, name: str) -> Dict[str, Dict[str, Any]]:
        """Get a saved settings profile
        
        Args:
            name: Profile name
            
        Returns:
            Settings for each network
        """
        return self._profiles.get(name, {})
    
    def list_settings_profiles(self) -> List[str]:
        """Get names of all saved settings profiles
        
        Returns:
            List of profile names
        """
        return list(self._profiles.keys())
    
    def clear_cache(self, network: Optional[str] = None) -> None:
        """Clear the settings and capabilities cache
        
        Args:
            network: Optional network to clear cache for
        """
        if network:
            self._settings_cache.pop(network, None)
            self._capabilities_cache.pop(network, None)
        else:
            self._settings_cache.clear()
            self._capabilities_cache.clear() 