# Posto SDK

A Python SDK for scheduling and managing social media posts through FS Poster.

## Installation

```bash
pip install posto-sdk
```

## Quick Start

```python
from posto_sdk import PostoSDK

# Initialize with credentials
posto = PostoSDK.from_credentials(
    username="your_username",
    password="your_password"
)

# Quick post to a channel
posto.post("Hello world!", to="My Twitter")

# Post with media and scheduling
posto.schedule_post(
    message="Check out this photo!",
    channels="2,3",
    media="path/to/photo.jpg",
    when="1h"  # Schedule 1 hour from now
)
```

## Features

- Easy authentication with WordPress credentials
- Support for multiple social media platforms
- Media upload capabilities (images and videos)
- Flexible scheduling options
- Channel management and discovery
- Error handling and logging

## Documentation

### Authentication

```python
# Using credentials
posto = PostoSDK.from_credentials(username="user", password="pass")

# Using existing token
posto = PostoSDK.from_token(token="your_base64_token")
```

### Posting Content

```python
# Simple immediate post
posto.post("Hello World!", to=2)

# Post with media
posto.post(
    message="Check this out!",
    to=["Twitter Main", "Instagram"],
    media="photo.jpg"
)

# Scheduled post
posto.schedule_post(
    message="Future post",
    channels=[2, 3],
    media=["image1.jpg", "image2.jpg"],
    when="2h"  # 2 hours from now
)
```

### Channel Management

```python
# Get all channels
channels = posto.get_available_channels()

# Find specific channels
twitter_channels = posto.get_channels_by_type("twitter")
my_channel = posto.find_channel("My Account")

# Get network types
networks = posto.get_networks()
```

## Error Handling

The SDK provides several exception types for proper error handling:

- `PostoError`: Base exception class
- `MediaUploadError`: Media upload failures
- `ChannelError`: Channel-related issues
- `PostingError`: Post creation failures

```python
from posto_sdk import PostoError

try:
    posto.post("Hello!", to="My Channel")
except PostoError as e:
    print(f"Error: {e}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 