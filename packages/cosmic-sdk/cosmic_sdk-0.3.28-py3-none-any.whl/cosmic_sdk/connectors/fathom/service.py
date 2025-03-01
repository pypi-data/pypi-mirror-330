import requests
import json
import sys
import os 
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
#from cosmic_sdk.connectors.fathom.models import Call, Transcript, TranscriptChunk
from .models import Call, Transcript, TranscriptChunk

class FathomService:
    def __init__(self, video_link: str):
        self.video_link = video_link
        self.sessions = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'X-Inertia-Partial-Component': 'page-call-detail',
            'X-Inertia-Partial-Data': 'call,bookmarks,cueSpans,noteClips,notes,transcriptCues',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.video_details = self.load_video_details()


    def load_video_details(self):
        try:
            initial_response = self.get_initial_response_and_headers()
        
            if not initial_response:
                return

            data_page = self.get_inertia_data_page()
            return json.loads(data_page).get('props')

        except Exception as e:
            print(f"Error loading video details: {e}")


    def get_initial_response_and_headers(self):
        try:
            initial_response = self.sessions.get(self.video_link, headers=self.headers)
            initial_response.raise_for_status()

            csrf_token = initial_response.text.split('csrf-token" content="')[1].split('"')[0]

            self.headers['X-CSRF-TOKEN'] = csrf_token
            self.headers['Referer'] = self.video_link

            return initial_response
        except Exception as e:
            print(f"Error loading initial response: {e}")
            return None
        

    def get_inertia_data_page(self):
        try:
            inertia_url = f"{self.video_link}?_inertia=1"
            inertia_response = self.sessions.get(inertia_url, headers=self.headers)

            data_page = inertia_response.text.split('data-page="')[1].split('"')[0].replace('&quot;', '"')
            return data_page
        except Exception as e:
            print(f"Error loading inertia video details: {e}")
            return None
        

    def get_call_details(self) -> Call:
        parsed_call_details = {}
        try:    
            self.call_details = self.video_details.get('call')
            customer = self.call_details.get('company')
            host = self.call_details.get("host")

            parsed_call_details['id'] = str(self.call_details.get('id'))

            parsed_call_details['title'] = self.call_details.get("title", '')
            parsed_call_details['byline'] = self.call_details.get('byline', '')

            parsed_call_details['customer_name'] = customer.get('name')
            parsed_call_details['customer_domain'] = customer.get('domain')
            parsed_call_details['host_email'] = host.get('email')

            parsed_call_details['video_url'] = self.call_details.get('video_url')
            return Call(**parsed_call_details)
        except Exception as e:
            print(f"Error getting call details: {e}")
            return None
        
    def get_call_transcripts(self) -> Transcript:
        parsed_transcripts = []
        try:
            transcript_cues = self.video_details.get('transcriptCues')
            for transcript_chunks in transcript_cues:
                for transcript_chunk in transcript_chunks:
                    try:
                        chunk = TranscriptChunk(
                            speaker_name=transcript_chunk.get('speaker_name'),
                            text=transcript_chunk.get('text').replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
                        )
                    except Exception as e:
                        print(f"Error parsing transcript chunk: {e}")
                    parsed_transcripts.append(chunk)
            return Transcript(complete_transcript=parsed_transcripts)
        except Exception as e:
            print(f"Error getting call transcripts: {e}")
            return None


if __name__ == "__main__":
    service = FathomService("https://fathom.video/share/yK8Ydkyq_xnWsm9y5Z6ur135G7zfy9KH")
    call_details = service.get_call_details()
    call_transcripts = service.get_call_transcripts()
    print(call_details)
    print(call_transcripts)
