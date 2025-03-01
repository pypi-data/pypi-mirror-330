from pydantic import BaseModel, Field
from typing import Optional, List

class SlackCredentials(BaseModel):
    slack_bot_token: str

class SlackMessage(BaseModel):
    channel_id: str
    text: str

class SlackHistoryRequest(BaseModel):
    channel: str
    limit: Optional[int]
    oldest: Optional[str] 
    latest: Optional[str]
    inclusive: Optional[bool]

class SlackMessageResponse(BaseModel):
    ok: bool
    ts: str
    message: dict
    channel: str

class SlackHistoryResponse(BaseModel):
    ok: bool
    messages: List[dict] 
    has_more: bool