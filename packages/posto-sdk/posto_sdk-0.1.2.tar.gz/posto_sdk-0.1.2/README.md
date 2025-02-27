# Posto SDK

A powerful Python SDK for scheduling and managing social media posts across multiple platforms.

## Installation

```bash
pip install posto-sdk
```

## Quick Start

```python
from posto_sdk import PostoSDK

# Initialize with credentials
sdk = PostoSDK.from_credentials('your_username', 'your_password')

# Or initialize with an existing token
sdk = PostoSDK.from_token('your_auth_token')

# Schedule a simple text post
result = sdk.post(
    message="Hello World!",
    channels=[1, 2]  # Channel IDs for your social media accounts
)

# Schedule a post with media
result = sdk.post(
    message="Check out this image!",
    channels=[1, 2],
    media="path/to/image.jpg"  # Can be local path or URL
)

# Schedule a post for later
from datetime import datetime, timedelta
future_time = datetime.now() + timedelta(hours=2)

result = sdk.post(
    message="Scheduled post!",
    channels=[1, 2],
    when=future_time
)
```

## Core Features

- **Multi-Platform Support**: Post to multiple social media platforms simultaneously
- **Media Handling**: Support for images, videos, and multiple media files
- **Flexible Scheduling**: Post immediately or schedule for later
- **Channel Management**: Easy access to available social media channels
- **Error Handling**: Comprehensive error reporting and validation

## API Reference

### Initialization

```python
# With credentials
sdk = PostoSDK.from_credentials(
    username="your_username",
    password="your_password",
    base_url="https://xmachine.online",  # Optional
    debug=False  # Optional
)

# With token
sdk = PostoSDK.from_token(
    token="your_auth_token",
    base_url="https://xmachine.online",  # Optional
    debug=False  # Optional
)
```

### Core Methods

#### Post Content
```python
result = sdk.post(
    message="Your post content",
    channels=["1", "2"],  # Channel IDs as string or list
    media="path/to/media.jpg",  # Optional: path or URL to media
    when=datetime.now()  # Optional: scheduling time
)
```

#### Channel Management
```python
# Get all available channels
channels = sdk.get_available_channels()

# Get channels by type
facebook_channels = sdk.get_channels_by_type("facebook")

# Find specific channels
channels = sdk.find_channel("my channel name")

# Get active channels
active = sdk.get_active_channels()

# Refresh channels list
sdk.refresh_channels()
```

### Response Types

#### PostResult
The `post()` method returns a `PostResult` object with:
- `success`: Boolean indicating success
- `schedule_group_id`: ID for the scheduled post group
- `error_message`: Error details if failed
- `media_ids`: List of uploaded media IDs

### Error Handling

The SDK provides specific exceptions for different error cases:
- `PostoError`: Base exception
- `MediaUploadError`: Media upload failures
- `ChannelError`: Channel-related issues
- `PostingError`: Post creation failures

```python
try:
    result = sdk.post(message="Test post", channels=[1])
except MediaUploadError as e:
    print(f"Media upload failed: {e}")
except ChannelError as e:
    print(f"Channel error: {e}")
except PostingError as e:
    print(f"Posting failed: {e}")
```

## Supported Media Types

### Images
- JPEG/JPG
- PNG
- GIF
- WebP
- TIFF
- BMP

### Videos
- MP4
- MPEG
- QuickTime
- AVI
- WMV
- WebM
- 3GPP

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
2. **Channel Validation**: Verify channel IDs before posting
3. **Media Optimization**: Ensure media files meet platform requirements
4. **Rate Limiting**: Consider implementing delays between multiple posts
5. **Token Management**: Store authentication tokens securely

## Support

For support, please contact: support@xmachine.online

## License

MIT License - See LICENSE file for details 