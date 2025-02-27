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

class SocialPoster:
    def __init__(self, auth_token: str, base_url: str = BASE_URL, debug: bool = False):
        """
        Initialize the SocialPoster
        
        Args:
            auth_token: Authentication token
            base_url: Base URL for the API
            debug: Enable debug logging
        """
        if not auth_token:
            raise ValueError("auth_token is required")
        
        self.base_url = base_url
        self.fs_poster_url = f"{base_url}/wp-json/fs-poster/v1/composer"
        self.media_url = f"{base_url}/wp-json/wp/v2/media"
        self.channels_url = f"{base_url}/wp-json/fs-poster/v1/channels"
        self.headers = {
            "Authorization": f"Basic {auth_token}",
            "Content-Type": "application/json"
        }
        
        if debug:
            logger.setLevel(logging.DEBUG)
    
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
        """
        Upload one or more media files to WordPress. Supports both local files and URLs.
        Automatically handles different media types (images, videos).
        
        Args:
            media_path_or_url: Path(s) or URL(s) to media files. Can be:
                - Local file path: "path/to/image.jpg"
                - URL: "https://example.com/image.jpg"
                - List of paths/URLs: ["image1.jpg", "https://example.com/image2.jpg"]
            
        Returns:
            List of media IDs that were successfully uploaded
            
        Raises:
            MediaUploadError: If any media upload fails
        """
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
                    try:
                        response = requests.post(
                            self.media_url,
                            headers=headers,
                            data=media_file
                        )
                        
                        if response.ok:
                            media_id = response.json()['id']
                            media_ids.append(media_id)
                            logger.debug(f"Media uploaded successfully. ID: {media_id}")
                        else:
                            errors.append(f"Failed to upload {media_path}: {response.text}")
                    except requests.exceptions.RequestException as e:
                        errors.append(f"Error uploading {media_path}: {str(e)}")
            
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
    
    def post(self, message: str, channel_ids: Union[str, List[int]], media: Optional[Union[str, List[str]]] = None, 
             when: Optional[Union[datetime, str, int]] = None) -> PostResult:
        """
        Post content with optional media to social networks
        
        Args:
            message: The text content to post
            channel_ids: Channel ID(s) - can be an integer, list of integers, or comma-separated string
            media: Optional - Path(s) or URL(s) to media file(s). Supports:
                - Local files: "path/to/image.jpg"
                - URLs: "https://example.com/image.jpg"
                - Multiple files: ["image1.jpg", "https://example.com/image2.jpg"]
            when: Optional - When to post. Can be:
                - None (post immediately)
                - datetime object
                - "1h" (1 hour from now)
                - "2d" (2 days from now)
                - Unix timestamp
        
        Returns:
            PostResult object containing the result of the operation
        
        Raises:
            PostingError: If the post creation fails
            MediaUploadError: If media upload fails
            ChannelError: If channel validation fails
        """
        try:
            # Convert channel_ids to list
            if isinstance(channel_ids, str):
                channel_ids = [int(cid.strip()) for cid in channel_ids.split(',')]
            elif isinstance(channel_ids, int):
                channel_ids = [channel_ids]
            
            # Validate channels
            if not channel_ids:
                raise ChannelError("No channel IDs provided")
            
            # Process scheduling
            schedule_time = None
            if when is not None:
                if isinstance(when, datetime):
                    schedule_time = int(when.timestamp())
                elif isinstance(when, str):
                    # Parse time strings like "1h", "2d"
                    unit = when[-1].lower()
                    try:
                        value = int(when[:-1])
                    except ValueError:
                        raise ValueError("Time string must be in format '1h' or '2d'")
                    
                    if unit == 'h':
                        schedule_time = int(time.time() + value * 3600)
                    elif unit == 'd':
                        schedule_time = int(time.time() + value * 86400)
                    else:
                        raise ValueError("Time string must end with 'h' (hours) or 'd' (days)")
                elif isinstance(when, int):
                    schedule_time = when
            
            # Upload media if provided
            media_ids = []
            if media:
                try:
                    media_ids = self.upload_media(media)
                except MediaUploadError as e:
                    logger.error(f"Media upload failed: {str(e)}")
                    raise
            
            # Create schedules for all channels
            schedules = []
            for channel_id in channel_ids:
                schedule = {
                    "channel_id": channel_id,
                    "custom_post_data": {
                        "post_content": message,
                    }
                }
                
                # Add media configuration if we have uploaded media
                if media_ids:
                    schedule["custom_post_data"].update({
                        "upload_media": True,
                        "upload_media_type": "custom",  # Always use custom type for simplicity
                        "media_list_to_upload": media_ids
                    })
                
                schedules.append(schedule)
            
            data = {
                "schedules": schedules,
                "share_at": schedule_time
            }
            
            logger.debug(f"Sending post request to: {self.fs_poster_url}")
            logger.debug(f"Post data: {data}")
            
            response = requests.post(self.fs_poster_url, headers=self.headers, json=data)
            
            if response.ok:
                result = response.json()
                logger.debug(f"Post created successfully: {result}")
                return PostResult.from_response(result)
            else:
                error_msg = f"Post creation failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return PostResult(success=False, error_message=error_msg)
        
        except Exception as e:
            error_msg = f"Error creating post: {str(e)}"
            logger.error(error_msg)
            return PostResult(success=False, error_message=error_msg)
    
    def get_channels(self):
        """Get all available social media channels
        
        Returns:
            List of dictionaries containing channel information:
            [
                {
                    "id": channel_id,
                    "name": channel_name,
                    "type": social_network type (e.g., "twitter", "instagram"),
                    "link": channel_link,
                    "picture": profile_picture_url,
                    "channel_type": type of channel (e.g., "account", "account_story"),
                    "status": whether channel is active
                },
                ...
            ]
        """
        try:
            response = requests.get(self.channels_url, headers=self.headers)
            
            if response.ok:
                data = response.json()
                channels = []
                for channel in data.get('channels', []):
                    channels.append({
                        "id": channel.get('id'),
                        "name": channel.get('name'),
                        "type": channel.get('social_network'),
                        "link": channel.get('channel_link'),
                        "picture": channel.get('picture'),
                        "channel_type": channel.get('channel_type'),
                        "status": channel.get('status', False)
                    })
                return channels
            else:
                print(f"Error getting channels: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting channels: {e}")
            return None

class PostoSDK:
    """An easy-to-use SDK for scheduling social media posts"""
    
    @classmethod
    def from_credentials(cls, username: str, password: str, base_url: str = BASE_URL, debug: bool = False) -> 'PostoSDK':
        """
        Create SDK instance using WordPress username and password
        
        Args:
            username: WordPress username
            password: WordPress password
            base_url: Optional - Custom WordPress instance URL
            debug: Optional - Enable debug logging
            
        Returns:
            PostoSDK instance
        """
        auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return cls(auth_token=auth_token, base_url=base_url, debug=debug)
    
    @classmethod
    def from_token(cls, token: str, base_url: str = BASE_URL, debug: bool = False) -> 'PostoSDK':
        """
        Create SDK instance using an existing Base64 encoded token
        
        Args:
            token: Base64 encoded authentication token
            base_url: Optional - Custom WordPress instance URL
            debug: Optional - Enable debug logging
            
        Returns:
            PostoSDK instance
        """
        return cls(auth_token=token, base_url=base_url, debug=debug)
    
    def __init__(self, auth_token: str, base_url: str = BASE_URL, debug: bool = False):
        """
        Initialize the SDK with authentication
        Note: It's recommended to use from_credentials() or from_token() instead
        
        Args:
            auth_token: Base64 encoded authentication token for Basic Auth
            base_url: Optional - Custom WordPress instance URL
            debug: Optional - Enable debug logging
        """
        if not auth_token:
            raise ValueError("auth_token is required for authentication")
            
        self._poster = SocialPoster(auth_token, base_url, debug=debug)
        self._channels = None  # Cache for channels
    
    def _fetch_channels(self, force_refresh=False):
        """Internal method to fetch and cache channels"""
        if self._channels is None or force_refresh:
            self._channels = self._poster.get_channels() or []
        return self._channels
    
    @property
    def channels(self):
        """Get all available channels"""
        return self._fetch_channels()
    
    def get_channel(self, channel_id: int):
        """
        Get details of a specific channel by ID
        
        Args:
            channel_id: The ID of the channel to fetch
            
        Returns:
            dict: Channel information or None if not found
        """
        for channel in self._fetch_channels():
            if channel['id'] == channel_id:
                return channel
        return None
    
    def get_channels_by_type(self, network_type: str):
        """
        Get all channels of a specific type (e.g., 'twitter', 'instagram')
        
        Args:
            network_type: The type of social network (e.g., 'twitter', 'instagram', 'threads')
            
        Returns:
            list: List of channels of the specified type
        """
        return [c for c in self._fetch_channels() if c['type'].lower() == network_type.lower()]
    
    def refresh_channels(self):
        """Force refresh the channels cache"""
        return self._fetch_channels(force_refresh=True)
    
    def get_active_channels(self):
        """Get only active channels"""
        return [c for c in self._fetch_channels() if c['status']]
    
    def get_channel_by_name(self, name: str):
        """
        Find a channel by its name (case-insensitive partial match)
        
        Args:
            name: The name to search for
            
        Returns:
            list: List of matching channels
        """
        name = name.lower()
        return [c for c in self._fetch_channels() if name in c['name'].lower()]
    
    def get_channel_types(self):
        """Get a list of all available social network types"""
        return sorted(list(set(c['type'] for c in self._fetch_channels())))
    
    def schedule_post(self,
        message: str,
        channels: Union[str, List[int], int],
        media: Optional[Union[str, List[str]]] = None,
        when: Optional[Union[datetime, str, int]] = None
    ) -> dict:
        """
        Schedule a social media post with super simple interface.
        
        Args:
            message: The text content to post
            channels: Channel ID(s) - can be an integer, list of integers, or comma-separated string
            media: Optional - Path to media file(s) to upload. Can be single path or list of paths
            when: Optional - When to post. Can be:
                - None (post immediately)
                - datetime object
                - "1h" (1 hour from now)
                - "2d" (2 days from now)
                - Unix timestamp
        
        Returns:
            API response dictionary
        """
        global SCHEDULE_TIME
        
        # Process channels parameter
        if isinstance(channels, int):
            channels = str(channels)
        elif isinstance(channels, list):
            channels = ",".join(map(str, channels))
        
        # Process scheduling
        schedule_time = None
        if when is not None:
            if isinstance(when, datetime):
                schedule_time = int(when.timestamp())
            elif isinstance(when, str):
                # Parse time strings like "1h", "2d"
                unit = when[-1].lower()
                value = int(when[:-1])
                if unit == 'h':
                    schedule_time = int(time.time() + value * 3600)
                elif unit == 'd':
                    schedule_time = int(time.time() + value * 86400)
                else:
                    raise ValueError("Time string must end with 'h' (hours) or 'd' (days)")
            elif isinstance(when, int):
                schedule_time = when
        
        # Store original schedule time
        original_schedule_time = SCHEDULE_TIME
        
        try:
            # Temporarily override global schedule time
            SCHEDULE_TIME = schedule_time
            
            # Make the post
            result = self._poster.post(message, channels, media)
            return result
        
        finally:
            # Restore original schedule time
            SCHEDULE_TIME = original_schedule_time
    
    def get_available_channels(self):
        """
        Get a list of all available social media channels
        
        Returns:
            List of dictionaries containing channel information:
            [
                {
                    "id": channel_id,
                    "name": channel_name,
                    "type": platform_type (e.g., "Facebook", "Twitter"),
                    "link": channel_url
                },
                ...
            ]
        """
        return self._poster.get_channels()

    def post(self, message: str, **kwargs) -> PostResult:
        """
        Quick and simple way to make a post. All parameters are optional except message.
        
        Args:
            message: The text content to post
            to: Channel ID(s) or name(s) - can be int, str, list[int], list[str]
            media: Path to media file(s) to upload
            when: When to post - supports:
                - "now" (immediate)
                - "1h" (1 hour from now)
                - "2d" (2 days from now)
                - datetime object
                - Unix timestamp
            network: Post to all channels of a specific type (e.g., "twitter", "instagram")
        
        Examples:
            # Quick post to a channel by name
            sdk.post("Hello world!", to="My Twitter")
            
            # Post to multiple channels with media
            sdk.post("Check this out!", to=["Twitter Main", "Instagram"], media="photo.jpg")
            
            # Post to all Twitter accounts in 1 hour
            sdk.post("Hello Twitter!", network="twitter", when="1h")
        """
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
        
        # Handle posting to all channels of a specific type
        if 'network' in kwargs:
            network_channels = self.get_channels_by_type(kwargs['network'])
            if network_channels:
                channels.extend(c['id'] for c in network_channels)
        
        if not channels:
            raise ValueError("No valid channels specified. Use 'to' or 'network' parameter.")
        
        # Convert when="now" to None for immediate posting
        when = kwargs.get('when')
        if when == "now":
            when = None
        
        return self._poster.post(
            message=message,
            channel_ids=channels,
            media=kwargs.get('media'),
            when=when
        )

    def get_networks(self) -> List[str]:
        """Get a simple list of available social networks"""
        return self.get_channel_types()

    def find_channel(self, search: str) -> List[dict]:
        """
        Find channels by name (case-insensitive search)
        
        Example:
            channels = posto.find_channel("twitter")
        """
        return self.get_channel_by_name(search)

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