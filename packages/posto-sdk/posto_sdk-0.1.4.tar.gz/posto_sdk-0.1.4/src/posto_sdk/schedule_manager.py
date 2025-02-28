from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("PostoSDK")

class ScheduleManager:
    """Manages all schedule-related operations"""
    
    def __init__(self, api_client):
        self._api = api_client
        
    def list(self, 
             status: Optional[Union[str, List[str]]] = None,
             network: Optional[Union[str, List[str]]] = None,
             page: int = 1,
             per_page: int = 10,
             schedule_id: Optional[int] = None,
             group_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a list of schedules with optional filtering.
        
        Args:
            status: Filter by status ('error', 'not_sent', 'sending', 'success', 'draft')
            network: Filter by social network(s)
            page: Page number for pagination
            per_page: Number of items per page
            schedule_id: Filter by specific schedule ID
            group_id: Filter by schedule group ID
        """
        params = {
            'page': page,
            'rows_count': per_page
        }
        
        if status:
            if isinstance(status, str):
                status = [status]
            params['statuses'] = ','.join(status)
            
        if network:
            if isinstance(network, str):
                network = [network]
            params['social_networks'] = ','.join(network)
            
        if schedule_id:
            params['schedule_id'] = schedule_id
            
        if group_id:
            params['schedule_group_id'] = group_id
            
        return self._api._make_request('GET', '/wp-json/fs-poster/v1/schedules', params=params)
    
    def retry(self, schedules: Union[int, List[int]]) -> Dict[str, Any]:
        """Retry failed schedules.
        
        Args:
            schedules: Single schedule ID or list of schedule IDs to retry
        """
        if isinstance(schedules, int):
            schedules = [schedules]
            
        data = {'log_ids[]': schedules}
        return self._api._make_request('POST', '/wp-json/fs-poster/v1/schedules/retry', data=data)
    
    def delete(self,
              schedule_ids: Optional[List[int]] = None,
              exclude_ids: Optional[List[int]] = None,
              status: Optional[Union[str, List[str]]] = None,
              older_than: Optional[str] = None,
              all: bool = False) -> bool:
        """Delete schedules matching the given criteria.
        
        Args:
            schedule_ids: List of specific schedule IDs to delete
            exclude_ids: List of schedule IDs to exclude from deletion
            status: Delete schedules with this status
            older_than: Delete schedules older than this (e.g. '7d', '24h', '30m')
            all: If True, delete all schedules matching other criteria
        """
        if not all and not schedule_ids and not status and not older_than:
            raise ValueError("Must specify what to delete: provide schedule_ids, status, older_than, or set all=True")
            
        data = {
            "include_all": all,
            "include_ids": schedule_ids or [],
            "exclude_ids": exclude_ids or [],
            "filters": {}
        }
        
        if status:
            if isinstance(status, str):
                status = [status]
            data['filters']['status'] = status
            
        if older_than:
            # Parse time strings like "7d", "24h", "30m"
            unit = older_than[-1].lower()
            try:
                value = int(older_than[:-1])
                if unit == 'd':
                    delta = timedelta(days=value)
                elif unit == 'h':
                    delta = timedelta(hours=value)
                elif unit == 'm':
                    delta = timedelta(minutes=value)
                else:
                    raise ValueError("Time unit must be 'd' (days), 'h' (hours), or 'm' (minutes)")
                    
                data['filters']['created_before'] = (datetime.now() - delta).strftime('%Y-%m-%d')
            except ValueError as e:
                raise ValueError(f"Invalid older_than format. Example: '7d', '24h', '30m'. Error: {str(e)}")
        
        try:
            self._api._make_request('DELETE', '/wp-json/fs-poster/v1/schedules', json=data)
            return True
        except Exception as e:
            logger.error(f"Failed to delete schedules: {str(e)}")
            return False 