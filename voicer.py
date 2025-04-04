import time
import os
import dashscope
import hashlib
from fish_audio_sdk import Session, TTSRequest, Prosody

VOICE_DIR = 'voices'
dashscope.api_key=os.getenv("DASHSCOPE_API_KEY")
session = Session(os.getenv('FISH_AUDIO_API_KEY'))

class Voicer:
    def __init__(self, match):
        self.match = match

    def make_voice(self):
        for comment in self.match.comments:
            self.make_text_voice(comment.text)

    def make_text_voice(self, text):
        # skip if voice already exists
        voice_path = self.get_voice(text)
        print(f"make voice for {text} at {voice_path}")
        if os.path.exists(voice_path):
            print(f"voice already exists for {text} at {voice_path}")
            return voice_path

        if not os.path.exists(VOICE_DIR):
            os.mkdir(VOICE_DIR)

        # generate and save voice
        time.sleep(1)
        print(f"generating voice for comment {text} with path {voice_path}")
        with open(voice_path, 'wb') as f:
            for chunk in session.tts(TTSRequest(
                reference_id=os.getenv('FISH_AUDIO_MODEL'),
                text=text
            )):
                f.write(chunk)

        return voice_path

    def get_voice(self, text):
        return os.path.join(VOICE_DIR, self.voice_name(text))

    def voice_name(self, text):
        return f"{hashlib.md5(text.encode('utf-8')).hexdigest()}.mp3"


if __name__ == '__main__':

    session = Session(os.getenv('FISH_AUDIO_API_KEY'))
    
    # Option 1: Using a reference_id
    with open("test.mp3", "wb") as f:
        for chunk in session.tts(TTSRequest(
            reference_id=os.getenv('FISH_AUDIO_MODEL'),
            text="目前场上状况依然紧张，银杏队以2:0领先。海棠队需要更有针对性的进攻策略，而银杏队则展现出强大的防守意图。期待双方更多精彩的对抗和机遇！"
        )):
            f.write(chunk)
    #synthesizer = SpeechSynthesizer(model="cosyvoice-v1", voice="longshuo")
    #audio = synthesizer.call("可惜！银杏队的10号\"沈子聿\"的射门打到了对方球员的腿上，未能形成威胁。")
    #with open('test.mp3', 'wb') as f:
    #    f.write(audio)

    import vlc
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('test.mp3')
    player.set_media(media)
    player.play()
    input()
    player.stop()