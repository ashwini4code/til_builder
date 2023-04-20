from datetime import date
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class YoutubeTranscribe:

    def __init__(self, id):
        self.id = id
        self.til = "Date: "
        self.vid_link =  "\n https://www.youtube.com/watch?v=" + id

    def fetch_transcription(self):
        transcript = YouTubeTranscriptApi.get_transcript(
            self.id, preserve_formatting=True)
        tformatter = TextFormatter()
        self.til = self.til + "\n" + tformatter.format_transcript(transcript)

    def prepare_til(self):
        today = date.today()
        datestr = today.strftime("%m/%d/%y")
        self.til = self.til + datestr + self.vid_link 
        self.fetch_transcription()
        self.check_til_length_compliance()
        return self.til

    # Check lengeth of message and truncate if required.
    def check_til_length_compliance(self):
        til_len = len(self.til.encode('utf-8'))
        # Devrev limits posts to 16 KB
        if til_len > 16383:
            print("Size of text in bytes ", til_len)
            print("Truncating string, since Devrev limits posts to 16KB")
            self.til.encode('utf-8')[:16383].decode('utf-8', 'ignore')
