import requests
import time
import mimetypes
import os
import base64
from typing import Union, List, Optional, Dict, Any
from datetime import datetime, timedelta
import tempfile
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from enum import Enum
from .api_utils import APIClient, ENDPOINTS
from .network_settings import NetworkSettings, NetworkCapabilities, NetworkSettingsManager
from .schedule_manager import ScheduleManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PostoSDK")

class MediaType(Enum):
    """Supported media types for posts"""
    CUSTOM = "custom"
    FEATURED_IMAGE = "featured_image"

@dataclass
class PostResult:
    """Structured response for post operations"""
    success: bool
    schedule_group_id: Optional[str] = None
    error_message: Optional[str] = None
    media_ids: List[int] = None

    @classmethod
    def from_response(cls, response: Optional[Dict[str, Any]]) -> 'PostResult':
        if not response:
            return cls(success=False, error_message="No response received")
        return cls(
            success=True,
            schedule_group_id=response.get('schedule_group_id'),
            media_ids=[]
        )

    def __str__(self) -> str:
        if self.success:
            return f"Success: Schedule Group ID = {self.schedule_group_id}"
        return f"Failed: {self.error_message}"

class PostoError(Exception):
    """Base exception for Posto SDK errors"""
    pass

class MediaUploadError(PostoError):
    """Raised when media upload fails"""
    pass

class ChannelError(PostoError):
    """Raised when there are channel-related issues"""
    pass

class PostingError(PostoError):
    """Raised when post creation fails"""
    pass

# Configuration
BASE_URL = 'https://xmachine.online'
WP_API_BASE = f'{BASE_URL}/wp-json'
FS_POSTER_ENDPOINT = f'{WP_API_BASE}/fs-poster/v1/composer'
MEDIA_ENDPOINT = f'{WP_API_BASE}/wp/v2/media'
MESSAGE = "Hello World!"  # Your message to post
CHANNEL_IDS = "2,3"  # Comma-separated channel IDs
SCHEDULE_TIME = int(time.time()) + 3600  # Set to None for immediate posting, or use Unix timestamp for scheduling
# Example for scheduling 1 hour from now: int(time.time()) + 3600

# Supported media types
SUPPORTED_IMAGE_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 
    'image/tiff', 'image/bmp'
}
SUPPORTED_VIDEO_TYPES = {
    'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo',
    'video/x-ms-wmv', 'video/webm', 'video/3gpp'
}
SUPPORTED_MEDIA_TYPES = SUPPORTED_IMAGE_TYPES | SUPPORTED_VIDEO_TYPES

class SocialPoster(APIClient):
    """Low-level social media posting client"""
    
    def _download_file(self, url: str) -> Optional[str]:
        """Download a file from URL and return the local path"""
        try:
            logger.debug(f"Downloading file from {url}")
            response = requests.get(url, stream=True)
            if response.ok:
                # Get the filename from URL or Content-Disposition
                content_disp = response.headers.get('Content-Disposition')
                if content_disp and 'filename=' in content_disp:
                    filename = content_disp.split('filename=')[-1].strip('"')
                else:
                    filename = os.path.basename(urlparse(url).path)
                    if not filename:
                        filename = 'downloaded_file'
                
                # Get extension from Content-Type if available
                content_type = response.headers.get('Content-Type')
                if content_type:
                    ext = mimetypes.guess_extension(content_type)
                    if ext and not filename.endswith(ext):
                        filename = f"{filename}{ext}"
                
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}")
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0
                
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        temp_file.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            progress = (downloaded / total_size) * 100
                            logger.debug(f"Download progress: {progress:.1f}%")
                
                temp_file.close()
                logger.debug(f"File downloaded successfully to {temp_file.name}")
                return temp_file.name
            
            logger.error(f"Failed to download file: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return None
    
    def upload_media(self, media_path_or_url: Union[str, List[str]]) -> List[int]:
        """Upload one or more media files to WordPress"""
        if isinstance(media_path_or_url, str):
            media_path_or_url = [media_path_or_url]
        
        media_ids = []
        errors = []
        
        for media_item in media_path_or_url:
            local_file = None
            try:
                # Check if it's a URL
                if media_item.startswith(('http://', 'https://')):
                    logger.debug(f"Downloading media from URL: {media_item}")
                    local_file = self._download_file(media_item)
                    if not local_file:
                        errors.append(f"Failed to download media from {media_item}")
                        continue
                    media_path = local_file
                else:
                    media_path = media_item
                
                if not os.path.exists(media_path):
                    errors.append(f"Media file not found: {media_path}")
                    continue
                
                # Get the mime type
                mime_type, _ = mimetypes.guess_type(media_path)
                if not mime_type:
                    # Try to guess from file extension
                    ext = os.path.splitext(media_path)[1].lower()
                    if ext in {'.jpg', '.jpeg'}:
                        mime_type = 'image/jpeg'
                    elif ext == '.png':
                        mime_type = 'image/png'
                    elif ext == '.gif':
                        mime_type = 'image/gif'
                    elif ext == '.mp4':
                        mime_type = 'video/mp4'
                    elif ext == '.mov':
                        mime_type = 'video/quicktime'
                
                if not mime_type or mime_type not in SUPPORTED_MEDIA_TYPES:
                    errors.append(f"Unsupported media type for {media_path}")
                    continue
                
                # Prepare headers for file upload
                headers = {
                    "Authorization": self.headers["Authorization"],
                    "Content-Type": mime_type,
                    "Content-Disposition": f'attachment; filename="{os.path.basename(media_path)}"'
                }
                
                # Upload the file
                logger.debug(f"Uploading media file: {media_path}")
                with open(media_path, 'rb') as media_file:
                    data = self._make_request('POST', ENDPOINTS['media'], data=media_file, headers=headers)
                    media_id = data['id']
                    media_ids.append(media_id)
                    logger.debug(f"Media uploaded successfully. ID: {media_id}")
            
            finally:
                # Clean up temporary file if we downloaded one
                if local_file and os.path.exists(local_file):
                    try:
                        os.unlink(local_file)
                        logger.debug(f"Cleaned up temporary file: {local_file}")
                    except:
                        logger.warning(f"Failed to clean up temporary file: {local_file}")
        
        if errors:
            raise MediaUploadError("\n".join(errors))
        
        return media_ids
    
    def post(self, message: str, channel_settings: List[Dict[str, Any]], 
             media: Optional[Union[str, List[str]]] = None,
             when: Optional[Union[datetime, str, int]] = None) -> PostResult:
        """Post content with optional media to social networks"""
        try:
            # Upload media if provided
            media_ids = []
            if media:
                try:
                    media_ids = self.upload_media(media)
                except MediaUploadError as e:
                    logger.error(f"Media upload failed: {str(e)}")
                    raise
            
            # Process scheduling
            schedule_time = None
            if when is not None:
                if isinstance(when, datetime):
                    schedule_time = int(when.timestamp())
                elif isinstance(when, str):
                    # Parse time strings like "30m", "1h", "2d"
                    unit = when[-1].lower()
                    value = int(when[:-1])
                    if unit == 'm':
                        schedule_time = int(time.time() + value * 60)
                    elif unit == 'h':
                        schedule_time = int(time.time() + value * 3600)
                    elif unit == 'd':
                        schedule_time = int(time.time() + value * 86400)
                    else:
                        raise ValueError("Time string must end with 'm' (minutes), 'h' (hours) or 'd' (days)")
                elif isinstance(when, int):
                    schedule_time = when
            
            # Create schedules for all channels
            schedules = []
            for channel in channel_settings:
                schedule = {
                    "channel_id": channel['channel_id'],
                    "custom_post_data": channel['custom_post_data']
                }
                
                # Add media configuration if we have uploaded media
                if media_ids:
                    schedule["custom_post_data"].update({
                        "upload_media": True,
                        "upload_media_type": "custom",
                        "media_list_to_upload": media_ids
                    })
                
                schedules.append(schedule)
            
            data = {
                "schedules": schedules,
                "share_at": schedule_time
            }
            
            logger.debug(f"Sending post request with data: {data}")
            result = self._make_request('POST', ENDPOINTS['composer'], json=data)
            
            logger.debug(f"Post created successfully: {result}")
            return PostResult.from_response(result)
            
        except Exception as e:
            error_msg = f"Error creating post: {str(e)}"
            logger.error(error_msg)
            return PostResult(success=False, error_message=error_msg)

class PostoSDK:
    """An easy-to-use SDK for scheduling social media posts"""
    
    @classmethod
    def from_credentials(cls, username: str, password: str, base_url: str = BASE_URL, debug: bool = False) -> 'PostoSDK':
        """Create SDK instance using WordPress username and password"""
        auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return cls(auth_token=auth_token, base_url=base_url, debug=debug)
    
    @classmethod
    def from_token(cls, token: str, base_url: str = BASE_URL, debug: bool = False) -> 'PostoSDK':
        """Create SDK instance using an existing Base64 encoded token"""
        return cls(auth_token=token, base_url=base_url, debug=debug)
    
    def __init__(self, auth_token: str, base_url: str = BASE_URL, debug: bool = False):
        """Initialize the SDK with authentication"""
        if not auth_token:
            raise ValueError("auth_token is required for authentication")
            
        self.base_url = base_url
        self._poster = SocialPoster(base_url, auth_token)
        self._settings_manager = NetworkSettingsManager(base_url, auth_token)
        self.schedules = ScheduleManager(self._poster)
        
        if debug:
            logger.setLevel(logging.DEBUG)
    
    @property
    def channels(self):
        """Get all available channels"""
        data = self._settings_manager._make_request('GET', ENDPOINTS['channels'])
        return data.get('channels', [])
    
    def get_channel(self, channel_id: int):
        """Get details of a specific channel by ID"""
        for channel in self.channels:
            if channel['id'] == channel_id:
                return channel
        return None
    
    def get_channels_by_type(self, network_type: str):
        """Get all channels of a specific type"""
        return [c for c in self.channels if c['social_network'].lower() == network_type.lower()]
    
    def get_active_channels(self):
        """Get only active channels"""
        return [c for c in self.channels if c['status']]
    
    def get_channel_by_name(self, name: str):
        """Find a channel by its name (case-insensitive partial match)"""
        name = name.lower()
        return [c for c in self.channels if name in c['name'].lower()]
    
    def get_channel_types(self):
        """Get a list of all available social network types"""
        return sorted(list(set(c['social_network'] for c in self.channels)))

    def get_network_settings(self, network: str) -> NetworkSettings:
        """Get settings for a specific network"""
        return self._settings_manager.get_network_settings(network)
        
    def save_network_settings(self, network: str, settings: Dict[str, Any]) -> None:
        """Save settings for a specific network"""
        self._settings_manager.save_network_settings(network, settings)

    def get_available_networks(self) -> List[Dict[str, Any]]:
        """Get list of available social networks and their basic info"""
        return self._settings_manager.get_available_networks()

    def post(self, message: str, **kwargs) -> PostResult:
        """Quick and simple way to make a post"""
        channels = []
        
        # Handle different ways to specify channels
        if 'to' in kwargs:
            target = kwargs['to']
            if isinstance(target, (str, int)):
                target = [target]
            
            for t in target:
                if isinstance(t, int):
                    # Direct channel ID
                    channels.append(t)
                elif isinstance(t, str):
                    # Try to find channel by name
                    found = self.get_channel_by_name(t)
                    if found:
                        channels.extend(c['id'] for c in found)
        
        if not channels:
            raise ValueError("No valid channels specified. Use 'to' parameter.")
        
        # Convert when="now" to None for immediate posting
        when = kwargs.get('when')
        if when == "now":
            when = None
            
        # Process settings for each channel
        channel_settings = []
        
        for channel_id in channels:
            channel = self.get_channel(channel_id)
            if not channel:
                continue
                
            network_type = channel['social_network'].lower()
            
            try:
                # Get network settings from backend
                network_settings = self.get_network_settings(network_type)
                
                # Start with default settings
                channel_specific_settings = network_settings.get_default_settings()
                
                # Update with custom settings if provided
                if 'settings' in kwargs:
                    custom_settings = kwargs['settings']
                    # Validate settings
                    is_valid, errors = network_settings.validate_settings(custom_settings)
                    if not is_valid:
                        logger.warning(f"Some settings for {network_type} were invalid: {errors}")
                    # Update settings, including any extra ones
                    channel_specific_settings.update(custom_settings)
                
                # Ensure required fields are set
                channel_specific_settings['post_content'] = message
                if 'media' in kwargs:
                    channel_specific_settings['upload_media'] = bool(kwargs['media'])
                    channel_specific_settings['media_type_to_upload'] = 'custom' if kwargs['media'] else 'featured_image'
                
                # Add to channel settings list
                channel_settings.append({
                    'channel_id': channel_id,
                    'custom_post_data': channel_specific_settings
                })
                
            except Exception as e:
                logger.warning(f"Failed to get settings for {network_type}, using defaults: {e}")
                # Fallback to basic settings
                channel_settings.append({
                    'channel_id': channel_id,
                    'custom_post_data': {
                        'post_content': message,
                        'upload_media': bool(kwargs.get('media')),
                        'media_type_to_upload': 'custom' if kwargs.get('media') else 'featured_image',
                        'attach_link': True,
                        'cut_post_text': True
                    }
                })
        
        return self._poster.post(
            message=message,
            channel_settings=channel_settings,
            media=kwargs.get('media'),
            when=when
        )

    def get_networks(self) -> List[str]:
        """Get a simple list of available social networks"""
        return self.get_channel_types()

    def find_channel(self, search: str) -> List[dict]:
        """Find channels by name (case-insensitive search)"""
        return self.get_channel_by_name(search)

    def get_network_capabilities(self, network: str) -> NetworkCapabilities:
        """Get capabilities for a specific network"""
        return self._settings_manager.get_network_capabilities(network)
        
    def get_network_defaults(self, network: str) -> Dict[str, Any]:
        """Get default values for a network's settings"""
        settings = self.get_network_settings(network)
        return {k: v['default'] for k, v in settings.get('default_values', {}).items()}
        
    def validate_network_settings(self, network: str, settings: Dict[str, Any]) -> None:
        """Validate network-specific settings"""
        self._settings_manager.validate_network_settings(network, settings)

    def get_supported_media_types(self, network: str) -> Optional[List[str]]:
        """Get supported media types for a network"""
        caps = self.get_network_capabilities(network)
        return caps.supported_media_types if caps.supports_media else None

    def save_settings_profile(self, name: str, settings: Dict[str, Dict[str, Any]]) -> None:
        """Save a network settings profile for reuse"""
        self._settings_manager.save_settings_profile(name, settings)
        
    def get_settings_profile(self, name: str) -> Dict[str, Dict[str, Any]]:
        """Get a saved settings profile"""
        return self._settings_manager.get_settings_profile(name)
        
    def list_settings_profiles(self) -> List[str]:
        """Get names of all saved settings profiles"""
        return self._settings_manager.list_settings_profiles()

# Example usage
if __name__ == "__main__":
    # Initialize SDK
    posto = PostoSDK("ZGVtbzM6a2wzUFg4NlJxNWJMaXBOcTVpUElWZGsw")
    
    # Simple immediate post
    posto.schedule_post("Hello World!", 2)
    
    # Post to multiple channels with an image in 1 hour
    posto.schedule_post(
        message="Check out this cool photo!",
        channels=[2, 3],
        media="path/to/image.jpg",
        when="1h"
    )
    
    # Schedule post for specific datetime
    future_time = datetime.now() + timedelta(days=2)
    posto.schedule_post(
        message="This is a scheduled post",
        channels="2,3",
        media=["image1.jpg", "image2.jpg"],
        when=future_time
    )