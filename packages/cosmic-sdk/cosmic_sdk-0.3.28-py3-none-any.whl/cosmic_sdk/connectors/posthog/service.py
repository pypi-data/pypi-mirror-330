# posthog/service.py
# Purpose: Provides a service layer for the PostHog API. 
# This layer is responsible for interacting with the PostHog API and returning processed data.
from cosmic_sdk.connectors.posthog.client import PostHogClient
from datetime import datetime
import requests


#TODO: Switch to using one function for all events
class PostHogService:
    def __init__(self, credentials: dict):
        self.client = PostHogClient(credentials)


    def fetch_posthog_user_logins(self, start_date, event_name='User logged in'):
        """
        Fetch PostHog user login data showing last login times and URLs accessed.
    
        Args:
            start_date (str): Start date in YYYY-MM-DD format
        
        Returns:
            dict: JSON response containing user login data and URLs
            None: If there was an error with the request
        """
        url = f"{self.client.base_url}/api/projects/{self.client.project_id}/query"
        headers = {
            "Authorization": f"Bearer {self.client. api_key}",
            "Content-Type": "application/json"
        }
        if not start_date:
            return {
                "status": "error",
                "message": "Start date is required",
                "data": None
            }
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        payload = {
            "query": {
                "kind": "HogQLQuery",
                "query": f"""
                    SELECT 
                        timestamp,
                        distinct_id,
                        properties.$current_url as url
                    FROM events 
                    WHERE event = '{event_name}'
                    AND timestamp >= '{start_date}'
                    AND timestamp < now()
                    ORDER BY timestamp DESC
                """
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Events retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch events: {str(e)}",
                "data": None
            }


    def fetch_events(self, start_date, event_name=''):
        """
        Fetch PostHog events data showing last login times and URLs accessed.
    
        Args:
            start_date (str): Start date in YYYY-MM-DD format
        """
        url = f"{self.client.base_url}/api/projects/{self.client.project_id}/query"
        headers = {
            "Authorization": f"Bearer {self.client. api_key}",
            "Content-Type": "application/json"
        }

        if not start_date:
            return {
                "status": "error",
                "message": "Start date is required",
                "data": None
            }
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        payload = {
            "query": {
                "kind": "HogQLQuery",
                "query": f"""
                    SELECT 
                        timestamp,
                        distinct_id,
                        properties.$current_url as url
                    FROM events 
                    WHERE event = '{event_name}'
                    AND timestamp >= '{start_date}'
                    AND timestamp < now()
                    ORDER BY timestamp DESC
                """
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Events retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch events: {str(e)}",
                "data": None
            }



