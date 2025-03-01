from typing import List, Optional
from pydantic import BaseModel

class Call(BaseModel):
    id: str
    title: Optional[str]
    byline: Optional[str]
    customer_name: str
    customer_domain: str
    host_email: str
    video_url: str

class TranscriptChunk(BaseModel):
    speaker_name: str
    text: str

class Transcript(BaseModel):
    complete_transcript: List[TranscriptChunk]
