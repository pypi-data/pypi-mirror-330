#!/usr/bin/env python3
from posto_sdk import PostoSDK
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_schedule_management():
    """Test schedule management features using the simplified SDK interface"""
    
    # Initialize SDK
    sdk = PostoSDK.from_credentials("demo3", "kl3PX86Rq5bLipNq5iPIVdk0", debug=True)
    
    try:
        # Get all schedules
        all_schedules = sdk.schedules.list()
        logger.info(f"Found {len(all_schedules['schedules'])} schedules")
        
        # Get failed schedules
        failed_schedules = sdk.schedules.list(status='error')
        logger.info(f"Found {len(failed_schedules['schedules'])} failed schedules")
        
        # Retry failed schedules if any exist
        if failed_schedules['schedules']:
            failed_ids = [s['id'] for s in failed_schedules['schedules']]
            retry_result = sdk.schedules.retry(failed_ids)
            logger.info(f"Retry result: {retry_result}")
        else:
            logger.info("No failed schedules to retry")
        
        # Delete old failed schedules
        delete_result = sdk.schedules.delete(status='error', older_than='7d')
        logger.info(f"Delete result: {delete_result}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_schedule_management() 