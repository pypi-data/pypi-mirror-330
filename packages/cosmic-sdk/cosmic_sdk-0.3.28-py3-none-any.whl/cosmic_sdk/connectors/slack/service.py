import logging
#from cosmic_sdk.connectors.posthog.models import Group, User, Event
import requests
import sys
import os
#from .models import SlackCredentials, SlackMessage, SlackHistoryRequest, SlackMessageResponse, SlackHistoryResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Ref: https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/
# Configure logging at the top of the file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# TODO: Add recipe to 
class SlackService:
    def __init__(self, credentials: dict, channel_id: str):
        try:
            
            if 'slack_bot_token' not in credentials:
                raise ValueError("Missing required 'slack_bot_token' in credentials")
            
            token = credentials.get('slack_bot_token')
            if not token:
                raise ValueError("slack_bot_token cannot be empty")
            
            self.credentials = credentials
            self.client = WebClient(token=token)
            self.channel_id = channel_id
            # Fetch bot user ID during initialization
            self.bot_user_id = self._fetch_bot_user_id()
        except Exception as e:
            raise ValueError(f"Failed to initialize Slack client: {str(e)}")
        
        
    def _handle_error(self, response):
        if not response.get('ok'):  # Slack SDK responses have an 'ok' boolean
            error_message = response.get('error', 'Unknown error')
            logger.error(f"Slack API request failed: {error_message}")
            raise ValueError(f"Slack API request failed: {error_message}")


    def set_channel_id(self, channel_id: str):
        self.channel_id = channel_id

    def get_channel_id(self):
        return self.channel_id
    
    def _fetch_bot_user_id(self):
        """Internal method to fetch bot user ID during initialization"""
        try:
            logger.info(f"Fetching bot user ID")
            auth_response = self.client.auth_test()
            self._handle_error(auth_response)
            logger.info(f"Bot user ID: {auth_response}")
            return auth_response['user_id']
        except SlackApiError as e:
            raise ValueError(f"Failed to get bot user ID: {str(e)}")

    def get_bot_user_id(self):
        return self.bot_user_id

    def bot_join_channel(self):
        if self.client is None:
            raise ValueError("Slack client is not initialized. Please call initialize_client first.")
        
        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please call set_channel_id first.")

        try:
            # Just join the channel - no need to invite self
            join_response = self.client.conversations_join(
                channel=self.channel_id
            )
            self._handle_error(join_response)
            logger.info("Successfully joined the channel")
            return join_response
        except SlackApiError as e:
            raise ValueError(f"Failed to join channel: {str(e)}")

    
    def send_message(self, message: str):
        logger.info(f"Self type: {type(self)}")  # Debug print
        logger.info(f"Self dict: {self.__dict__}")  # Debug print

        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please call set_channel_id first.")
            
        if self.client is None:
            raise ValueError("Slack client is not initialized. Please call initialize_client first.")
        
        response = self.client.chat_postMessage(
            channel=self.channel_id,
            text=message
        )
        self._handle_error(response)
        return response
    
    def send_file(self, file_path: str, title: str, initial_comment: str):
        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please call set_channel_id first.")
        
        if self.client is None:
            raise ValueError("Slack client is not initialized. Please call initialize_client first.")
        
        response = self.client.files_upload_v2(
            channel=self.channel_id,
            file=file_path,
            title=title or "File uploaded from Cosmic SDK",
            initial_comment=initial_comment or "This is a file  uploaded from the Cosmic SDK"
            )
        self._handle_error(response)
        return response
        
    def get_channel_history(
            self, 
            limit: int = 1000,  # optional - number of messages to return
            oldest: str = None,  # optional - oldest message timestamp to include
            latest: str = None,  # optional - latest message timestamp to include
            inclusive: bool = True,  # optional - include messages from the channel
            cursor: str = None  # optional - pagination cursor
            ):
        try:
            logger.info(f"Getting channel history for channel: {self.channel_id}")

            if self.channel_id is None:
                raise ValueError("Channel ID is not set. Please call set_channel_id first.")
            
            if self.client is None:
                raise ValueError("Slack client is not initialized. Please call initialize_client first.")
            
            response = self.client.conversations_history(
                channel=self.channel_id,
                limit=limit,
                oldest=oldest,
                latest=latest,
                inclusive=inclusive,
                cursor=cursor
            )
            self._handle_error(response)
            return response
        except SlackApiError as e:
            raise ValueError(f"Failed to get channel history: {str(e)}")

"""    
if __name__ == "__main__":
    service = SlackService({'slack_bot_token': 'xoxb-7139431866391-8421170177953-1czCQ1lMTAXclFKfYXQXsN3z'}, "C08CFFFJAQ0")
    service.bot_join_channel()

    #Send message
    #service.send_message("Hi! I'm a bot that was invited to this channel.")

    #Get channel history
    #channel_history = service.get_channel_history()
    #print(channel_history)

    #Send file
    #service.send_file("provision_churn.csv", "Churn CSV", "This is the churn CSV file")
"""