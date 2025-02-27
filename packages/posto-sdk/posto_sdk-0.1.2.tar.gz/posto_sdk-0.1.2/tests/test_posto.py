from posto_sdk import PostoSDK, PostoError
from datetime import datetime, timedelta
import logging

def test_posto_sdk():
    # Initialize with WordPress credentials and debug mode
    posto = PostoSDK.from_credentials(
        username="demo3",
        password="51Az 1PCV 4VZe ubzS Fb7C RRy0",
        debug=True  # Enable detailed logging
    )
    
    try:
        # 1. Show available social networks
        print("\nAvailable social networks:")
        networks = posto.get_networks()
        print(networks)
        
        # 2. Show all available channels
        print("\nAll available channels:")
        channels = posto.get_available_channels()
        if channels:
            for channel in channels:
                print(f"- Network: {channel.get('type', 'unknown')}, "
                      f"Name: {channel.get('name', 'unnamed')}, "
                      f"ID: {channel.get('id', 'no-id')}")
        else:
            print("No channels found")
        
        # 3. Test different posting scenarios
        if channels:
            # Get a Twitter channel for testing
            twitter_channels = [c for c in channels if c['type'] == 'twitter']
            if twitter_channels:
                channel = twitter_channels[0]
                channel_id = channel['id']
                print(f"\nTesting with Twitter channel: {channel['name']} (ID: {channel_id})")
                
                # Test 1: Simple text post
                print("\n1. Testing simple text post...")
                result = posto.schedule_post(
                    message="🌟 Testing simple text post via PostoSDK!",
                    channels=channel_id,
                    when="1h"  # Added 1 hour delay
                )
                print(f"Result: {result}")
                
                # Test 2: Post with multiple media URLs
                print("\n2. Testing post with multiple media URLs...")
                result = posto.schedule_post(
                    message="🌟 Testing multiple media URLs via PostoSDK!",
                    channels=channel_id,
                    media=[
                        "https://picsum.photos/200/300",
                        "https://picsum.photos/300/400"
                    ],
                    when="2h"  # Added 2 hour delay
                )
                print(f"Result: {result}")
                
                # Test 3: Scheduled post with media
                print("\n3. Testing scheduled post with media...")
                result = posto.schedule_post(
                    message="🌟 This is a scheduled post with media via PostoSDK!",
                    channels=channel_id,
                    media="https://picsum.photos/400/500",  # Single media URL
                    when="1h"  # Schedule 1 hour from now
                )
                print(f"Result: {result}")
                
                # Test 4: Post to multiple channels
                print("\n4. Testing post to multiple channels...")
                result = posto.post(
                    message="🌟 Testing multi-channel post via PostoSDK!",
                    to=["POD Diva", "Trump Flash"],  # Post to channels by name
                    media="https://picsum.photos/600/700",
                    when="2h"  # Schedule 2 hours from now
                )
                print(f"Result: {result}")
                
                # Test 5: Post to all Twitter accounts
                print("\n5. Testing post to all Twitter accounts...")
                result = posto.post(
                    message="🌟 Hello to all Twitter followers!",
                    network="twitter",
                    when="3h"  # Changed from "now" to 3 hour delay
                )
                print(f"Result: {result}")
                
    except PostoError as e:
        print(f"PostoSDK Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_posto_sdk() 