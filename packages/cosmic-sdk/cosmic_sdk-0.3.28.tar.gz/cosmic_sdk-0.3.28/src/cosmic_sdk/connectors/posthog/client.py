# posthog/client.py
# Purpose: Interacts with the PostHog API to fetch raw data.
import logging
from typing import List, Dict, Any
from cosmic_sdk.connectors.posthog.models import Group, User, Event
import requests
from datetime import datetime
class PostHogClient:
    def __init__(self, credentials: dict):
        try:
            self.api_key = credentials.get('apiKey') or credentials.get('api_key')
            self.base_url = credentials.get('baseUrl') or credentials.get('base_url')
            self.project_id = credentials.get('projectId') or credentials.get('project_id')
            
            if not self.api_key:
                raise ValueError("Missing required credential: 'apiKey' or 'api_key'")
            if not self.base_url:
                raise ValueError("Missing required credential: 'baseUrl' or 'base_url'")
            if not self.project_id:
                raise ValueError("Missing required credential: 'projectId' or 'project_id'")

            self.headers = {"Authorization": f"Bearer {self.api_key}"}
        except Exception as e:
            raise ValueError(f"Failed to initialize PostHog client: {str(e)}")
        

    """
    Section: Organization API
    url: https://posthog.com/docs/api/organizations
    """
    def get_organizations(self) -> Dict[str, Any]:
      """Get all organizations"""
      try:
            response = requests.get(
                f"{self.base_url}/api/organizations/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success", 
                "message": "Connected to PostHog",
                "data": response.json()
            }
      except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"PostHog connection failed: {str(e)}",
                "data": None
            }
    

    def get_project(self) -> Dict[str, Any]:
        """Get a project"""
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Project retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch project: {str(e)}",
                "data": None
            }

    """
    Section: Group API
    url: https://posthog.com/docs/api/groups
    """
    def get_groups(self) -> List[Group]:
        """
        Description: List all groups for a project
        url: https://posthog.com/docs/api/groups#get-api-projects-project_id-groups
        TODO: Add query params such as cursor, search, group_type
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/groups/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Group retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch group: {str(e)}",
                "data": None
            }
        
    def get_group_find(self) -> List[Group]:
        """
        Description: Find a group by key or group index
        url: https://posthog.com/docs/api/groups#get-api-projects-project_id-groups
        TODO: Add query params such as group_key, group_type_index
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/groups/find/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Group retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch group: {str(e)}",
                "data": None
            }

    def get_group_types(self) -> List[Group]:
        """
        Description: Get group types
        url: https://posthog.com/docs/api/groups-types
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/group-types/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Group types retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch group types: {str(e)}",
                "data": None
            }

    """
    Section: Events API
    url: https://posthog.com/docs/api/events
    """
    def get_events(self) -> List[Event]:
        """
        Description: Get all events for a project
        url: https://posthog.com/docs/api/events
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/events/",
                headers=self.headers,
                timeout=10
            )
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
        
    def get_event_by_id(self, event_id: str) -> Dict[str, Any]:
        """
        Description: Get an event by ID
        url: https://posthog.com/docs/api/events#get-api-projects-project_id-events-event_id
        """
        if not self.project_id or not event_id:
            return {
                "status": "error",
                "message": "Project ID and event ID are required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/events/{event_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Event retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch event: {str(e)}",
                "data": None
            }

    def get_event_by_values(self) -> Dict[str, Any]:
        """
        Description: Get an event by value
        url: https://posthog.com/docs/api/events#get-api-projects-project_id-events-values
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.project_id}/events/values/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Event values retrieved successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to fetch event values: {str(e)}",
                "data": None
            }

    
    def generate_test_data(self, organization_id: str) -> Dict[str, Any]:
        """
        Description: Generate test data
        url: https://posthog.com/docs/api/projects#get-api-organizations-organization_id-projects-id-is_generating_demo_data
        """
        if not self.project_id:
            return {
                "status": "error",
                "message": "Project ID is required",
                "data": None
            }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/organizations/{organization_id}/projects/{project_id}/is_generating_demo_data/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message": "Test data generated successfully",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to generate test data: {str(e)}",
                "data": None
            }