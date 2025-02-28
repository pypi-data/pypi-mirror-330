from typing import List, Optional, Union, Dict, Any
from datetime import datetime, timedelta
from .posto_sdk import PostoSDK
import logging
import base64

logger = logging.getLogger("PostoSDK")

class SocialMediaManager(PostoSDK):
    """
    Enhanced PostoSDK with additional features for social media management.
    Inherits all base PostoSDK functionality while adding convenience methods
    for social media managers.
    """
    
    def __init__(self, username: str, password: str):
        """Initialize with WordPress credentials"""
        logger.debug(f"Initializing SocialMediaManager with username: {username}")
        
        # Use PostoSDK's from_credentials class method
        try:
            sdk = PostoSDK.from_credentials(username=username, password=password)
            logger.debug("Successfully created PostoSDK instance")
            logger.debug(f"SDK base_url: {sdk.base_url}")
            
            # Get the auth token directly from the SDK instance
            auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
            
            super().__init__(auth_token=auth_token, base_url=sdk.base_url)
            logger.debug("Successfully initialized parent PostoSDK class")
            
            self._default_settings = {}  # Store default settings per network/channel
            logger.debug("SocialMediaManager initialization complete")
            
        except Exception as e:
            logger.error(f"Error during SocialMediaManager initialization: {str(e)}")
            raise
        
    def set_network_defaults(self, network: str, settings: Dict[str, Any]) -> None:
        """
        Set default settings for a specific network (applies to all channels of that network)
        
        Example:
            # Set defaults for all TikTok posts
            manager.set_network_defaults("tiktok", {
                "post_text": "✨ {post_title} #fyp",
                "upload_media": True,
                "cut_post_text": True
            })
        """
        if not network in self._default_settings:
            self._default_settings[network] = {}
        self._default_settings[network]['network'] = settings
        
    def set_channel_defaults(self, channel_id: Union[int, str], settings: Dict[str, Any]) -> None:
        """
        Set default settings for a specific channel
        
        Example:
            # Set defaults for a specific Instagram account
            manager.set_channel_defaults("my_business_instagram", {
                "post_text": "{post_title}\n.\n.\n.\n#business #updates",
                "upload_media": True
            })
        """
        # If channel_id is a name, find the actual ID
        if isinstance(channel_id, str):
            channels = self.get_channels_by_type(channel_id)
            if channels:
                channel_id = channels[0]['id']
            else:
                raise ValueError(f"Channel not found: {channel_id}")
                
        network = self._get_channel_network(channel_id)
        if network:
            if not network in self._default_settings:
                self._default_settings[network] = {}
            self._default_settings[network][str(channel_id)] = settings
            
    def _get_channel_network(self, channel_id: int) -> Optional[str]:
        """Get the network type for a channel"""
        for channel in self.channels:
            if channel['id'] == channel_id:
                return channel['social_network']
        return None
        
    def _merge_settings(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two settings dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        return result
        
    def _get_final_settings(self, network: str, channel_id: Optional[int] = None,
                          style: Optional[str] = None, 
                          custom_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get final settings combining defaults, style, and custom settings"""
        final = {}
        
        # 1. Start with network defaults if any
        if network in self._default_settings and 'network' in self._default_settings[network]:
            final = self._merge_settings(final, self._default_settings[network]['network'])
            
        # 2. Add channel defaults if any
        if channel_id and network in self._default_settings and str(channel_id) in self._default_settings[network]:
            final = self._merge_settings(final, self._default_settings[network][str(channel_id)])
            
        # 3. Add style settings if any
        if style:
            style_settings = self._get_style_settings(style).get(network, {})
            final = self._merge_settings(final, style_settings)
            
        # 4. Add custom settings if any
        if custom_settings:
            final = self._merge_settings(final, custom_settings)
            
        return final

    def quick_post(self, message: str, image: Optional[str] = None, style: Optional[str] = None,
                  settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Post a message to all your active channels right now
        """
        # Get all active channels
        channels = self.get_active_channels()
        if not channels:
            return False
            
        # Prepare settings for each channel
        channel_settings = {}
        for channel in channels:
            network = self._get_channel_network(channel['id'])
            if network:
                final_settings = self._get_final_settings(
                    network=network,
                    channel_id=channel['id'],
                    style=style,
                    custom_settings=settings.get(network) if settings else None
                )
                channel_settings[network] = final_settings
            
        # Make the post
        result = self.post(
            message,
            to=[ch['id'] for ch in channels],
            media=image,
            settings=channel_settings
        )
        return result.success
    
    def _get_style_settings(self, style: str) -> Dict[str, Any]:
        """Get predefined settings for common post styles"""
        styles = {
            "announcement": {
                "twitter": {"post_text": "🚨 {post_title} 🚨", "cut_post_text": True},
                "facebook": {"post_text": "🎉 ANNOUNCEMENT 🎉\n\n{post_title}", "attach_link": True},
                "instagram": {"post_text": "📢 {post_title}\n.\n.\n.", "upload_media": True}
            },
            "blog": {
                "twitter": {"post_text": "New blog post: {post_title}\n\nRead more 👇", "attach_link": True},
                "facebook": {"post_text": "📝 {post_title}\n\n{post_excerpt}", "attach_link": True},
                "linkedin": {"post_text": "New Article 📝\n\n{post_title}\n\n{post_excerpt}", "attach_link": True}
            },
            "product": {
                "twitter": {"post_text": "🆕 {post_title}\n\nLearn more ➡️", "upload_media": True},
                "facebook": {"post_text": "🎉 New Product Alert!\n\n{post_title}", "upload_media": True},
                "instagram": {"post_text": "Introducing... ✨\n{post_title}", "upload_media": True}
            }
        }
        return styles.get(style, {})
        
    def post_to(self, platforms: Union[str, List[str]], message: str, 
                image: Optional[str] = None, when: Optional[str] = None,
                style: Optional[str] = None, settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Post to specific platforms with improved settings handling
        
        Examples:
            # Simple post to Twitter
            manager.post_to("twitter", "Hello Twitter!")
            
            # Post with style and network-specific settings
            manager.post_to(
                ["facebook", "instagram"], 
                "Big announcement!", 
                image="photo.jpg",
                style="announcement",
                settings={
                    "post_content": "BIG NEWS! 🎉\n{post_title}",
                    "upload_media": True,
                    "cut_post_text": True,
                    "attach_link": True
                }
            )
        """
        if isinstance(platforms, str):
            platforms = [platforms]
            
        # Get all channels for the specified platforms
        channels = []
        for platform in platforms:
            platform_channels = self.get_channels_by_type(platform.lower())
            channels.extend(channel['id'] for channel in platform_channels)
            
        if not channels:
            logger.warning(f"No channels found for platforms: {platforms}")
            return False
            
        # Handle scheduling
        schedule_time = self._parse_schedule_time(when)
        
        # Prepare base settings
        base_settings = settings or {}
        if style:
            style_settings = self._get_style_settings(style)
            base_settings = self._merge_settings(style_settings, base_settings)
        
        # Add required fields
        base_settings.update({
            "post_content": message,
            "upload_media": bool(image),
            "media_type_to_upload": "custom" if image else "featured_image"
        })
        
        # Use the same settings for all channels since the backend expects flat settings
        result = self.post(
            message,
            to=channels,
            media=image,
            when=schedule_time,
            settings=base_settings  # Pass flat settings directly
        )
        
        if not result.success:
            logger.error(f"Failed to post: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}")
        
        return result.success
    
    def _parse_schedule_time(self, when: Optional[str]) -> Optional[datetime]:
        """Convert friendly time strings to datetime"""
        if not when:
            return None
            
        now = datetime.now()
        
        if when == "tomorrow":
            return now + timedelta(days=1)
        elif when == "tonight":
            tonight = now.replace(hour=20, minute=0)
            if now >= tonight:
                tonight = tonight + timedelta(days=1)
            return tonight
        
        # Parse time strings like "30m", "1h", "2d", "5h"
        if isinstance(when, str) and len(when) >= 2:
            unit = when[-1].lower()
            try:
                value = int(when[:-1])
                if unit == 'm':
                    return now + timedelta(minutes=value)
                elif unit == 'h':
                    return now + timedelta(hours=value)
                elif unit == 'd':
                    return now + timedelta(days=value)
            except ValueError:
                pass
                
        return None
        
    def schedule_post(self, message: str, when: str, 
                     image: Optional[str] = None, 
                     platforms: Optional[List[str]] = None,
                     style: Optional[str] = None,
                     settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Schedule a post for later
        
        Examples:
            # Schedule everywhere with a style
            manager.schedule_post("Hello world!", "tomorrow", style="announcement")
            
            # Schedule with custom settings
            manager.schedule_post(
                "Evening update", "tonight",
                platforms=["facebook", "twitter"],
                settings={
                    "facebook": {"post_text": "Evening News 🌙\n{post_title}"},
                    "twitter": {"post_text": "🌙 {post_title}"}
                }
            )
        """
        return self.post_to(
            platforms or self.get_networks(),
            message,
            image=image,
            when=when,
            style=style,
            settings=settings
        )
        
    def create_campaign(self, messages: List[str], 
                       platforms: Optional[List[str]] = None,
                       images: Optional[List[str]] = None,
                       start_time: Optional[str] = None,
                       hours_between_posts: int = 24,
                       style: Optional[str] = None,
                       settings: Optional[Dict[str, Any]] = None) -> List[bool]:
        """
        Create a campaign with multiple posts scheduled over time
        """
        if not platforms:
            # Get all available networks
            networks = self.get_available_networks()
            platforms = [net['slug'] for net in networks]
            
        # Get channel IDs for selected platforms
        channel_ids = []
        for platform in platforms:
            platform_channels = self.get_channels_by_type(platform)
            channel_ids.extend([ch['id'] for ch in platform_channels])
            
        if not channel_ids:
            return [False] * len(messages)
            
        # Prepare settings for each platform
        platform_settings = {}
        for platform in platforms:
            final_settings = self._get_final_settings(
                network=platform,
                style=style,
                custom_settings=settings.get(platform) if settings else None
            )
            platform_settings[platform] = final_settings
            
        results = []
        start = datetime.now()
        
        if start_time == "tomorrow":
            start = start + timedelta(days=1)
        elif start_time == "tonight":
            start = start.replace(hour=20, minute=0)
            if datetime.now() >= start:
                start = start + timedelta(days=1)
                
        for i, message in enumerate(messages):
            post_time = start + timedelta(hours=i * hours_between_posts)
            image = images[i] if images and i < len(images) else None
            
            result = self.post(
                message,
                to=channel_ids,
                media=image,
                when=post_time,
                settings=platform_settings
            )
            results.append(result.success)
            
        return results
        
    def save_style(self, name: str, settings: Dict[str, Dict[str, Any]]) -> None:
        """
        Save custom post settings for reuse
        
        Example:
            manager.save_style("my_announcement", {
                "twitter": {
                    "post_text": "🎯 {post_title}",
                    "cut_post_text": True
                },
                "facebook": {
                    "post_text": "📢 Important Update:\n\n{post_title}",
                    "attach_link": True
                }
            })
        """
        self.save_settings_profile(name, settings)
        
    def get_style(self, name: str) -> Dict[str, Dict[str, Any]]:
        """Get a saved post style"""
        return self.get_settings_profile(name)
        
    def list_styles(self) -> List[str]:
        """Get names of all saved post styles"""
        return self.list_settings_profiles()
        
    def get_channels(self, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get your social media channels
        
        Examples:
            # Get all channels
            channels = manager.get_channels()
            
            # Get just Twitter channels
            twitter_channels = manager.get_channels("twitter")
        """
        if platform:
            return self.get_channels_by_type(platform.lower())
        return self.channels

    def get_network_defaults(self, network: str) -> Dict[str, Any]:
        """
        Get current default settings for a network
        
        Example:
            tiktok_settings = manager.get_network_defaults("tiktok")
        """
        return self._default_settings.get(network, {}).get('network', {})
        
    def get_channel_defaults(self, channel_id: Union[int, str]) -> Dict[str, Any]:
        """
        Get current default settings for a channel
        
        Example:
            instagram_settings = manager.get_channel_defaults("my_instagram")
        """
        if isinstance(channel_id, str):
            channels = self.find_channel(channel_id)
            if channels:
                channel_id = channels[0]['id']
            else:
                return {}
                
        network = self._get_channel_network(channel_id)
        if network:
            return self._default_settings.get(network, {}).get(str(channel_id), {})
        return {}
        
    def clear_defaults(self, network: Optional[str] = None, channel_id: Optional[Union[int, str]] = None) -> None:
        """
        Clear default settings
        
        Examples:
            # Clear all defaults
            manager.clear_defaults()
            
            # Clear defaults for a network
            manager.clear_defaults(network="twitter")
            
            # Clear defaults for a channel
            manager.clear_defaults(channel_id="my_instagram")
        """
        if network and channel_id:
            if isinstance(channel_id, str):
                channels = self.find_channel(channel_id)
                if channels:
                    channel_id = channels[0]['id']
            if network in self._default_settings:
                self._default_settings[network].pop(str(channel_id), None)
        elif network:
            self._default_settings.pop(network, None)
        else:
            self._default_settings.clear()

    def delete_all_schedules(self, exclude_ids: List[int] = None, 
                            platforms: List[str] = None, 
                            statuses: List[str] = None) -> bool:
        """
        Delete all scheduled posts with optional filters
        
        Args:
            exclude_ids: List of schedule IDs to exclude from deletion
            platforms: List of platforms to filter by (e.g. ['twitter', 'facebook'])
            statuses: List of statuses to filter by ('not_sent', 'success', 'error', 'draft')
            
        Example:
            # Delete all pending schedules for Twitter
            manager.delete_all_schedules(
                platforms=['twitter'],
                statuses=['not_sent']
            )
        """
        filters = {}
        if platforms:
            filters['social_networks'] = platforms
        if statuses:
            filters['statuses'] = statuses
        
        return self.delete_schedules(
            include_all=True,
            exclude_ids=exclude_ids,
            filters=filters
        )
        
    def delete_schedules(self, schedule_ids: List[int]) -> bool:
        """
        Delete specific scheduled posts by their IDs
        
        Args:
            schedule_ids: List of schedule IDs to delete
            
        Example:
            manager.delete_schedules([123, 456, 789])
        """
        return self.delete_schedules(
            include_all=False,
            include_ids=schedule_ids
        )

    def create_quick_campaign(self, messages: List[str], interval: str = "1d", 
                            start_time: Optional[str] = None) -> bool:
        """
        Quickly create a campaign with sensible defaults
        
        Args:
            messages: List of messages to post
            interval: Time between posts (e.g. "1h", "1d")
            start_time: When to start (e.g. "tomorrow", "1h")
            
        Returns:
            bool: True if campaign was created successfully
            
        Example:
            # Create a daily campaign starting tomorrow
            messages = [
                "Day 1: Launch announcement! 🚀",
                "Day 2: Feature spotlight ✨",
                "Day 3: Customer testimonials 💬"
            ]
            manager.create_quick_campaign(
                messages=messages,
                interval="1d",
                start_time="tomorrow"
            )
        """
        # Get all active channels
        channels = self.get_active_channels()
        if not channels:
            logger.warning("No active channels found for campaign")
            return False
        
        # Prepare settings for each platform
        platform_settings = {}
        for channel in channels:
            network = channel['social_network']
            if network:
                # Get network-specific settings using existing method
                final_settings = self._get_final_settings(
                    network=network,
                    channel_id=channel['id']
                )
                platform_settings[network] = final_settings
            
        # Convert interval to hours
        if interval.endswith('d'):
            hours = int(interval[:-1]) * 24
        elif interval.endswith('h'):
            hours = int(interval[:-1])
        else:
            hours = 24  # Default to daily
            
        # Create campaign using existing method
        results = self.create_campaign(
            messages=messages,
            start_time=start_time or "1h",
            hours_between_posts=hours,
            settings=platform_settings
        )
        
        # Return True only if all posts were scheduled successfully
        return all(results) if isinstance(results, list) else bool(results) 