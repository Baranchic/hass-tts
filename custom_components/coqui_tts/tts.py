import requests
from homeassistant.components.tts import Provider, Voice

SUPPORT_LANGUAGES = ["en"]
SUPPORTED_OPTIONS = ["voice"]

def get_engine(hass, config, discovery_info=None):
    return CoquiTTSProvider(hass, config)

class CoquiTTSProvider(Provider):
    def __init__(self, hass, config):
        self.hass = hass
        self.name = "Coqui TTS"
        self._url = "http://192.168.88.13:5002/api/tts"
        self._speakers = ["p234", "p316", "p376"]  # Add more as needed

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def default_language(self):
        return "en"

    @property
    def default_options(self):
        return {"voice": "p316"}

    @property
    def supported_options(self):
        return SUPPORTED_OPTIONS

    @property
    def voice_info(self):
        return {speaker: Voice(speaker, speaker, {"language": "en"}) for speaker in self._speakers}

    def get_tts_audio(self, message, language, options=None):
        message = message.strip() if message else "Default message"
        print(f"Sending TTS request: text='{message}', language={language}, options={options}")
        try:
            voice = options.get("voice", "p316") if options else "p316"
            params = {
                "text": message,
                "speaker_id": voice,
                "language_id": "en"
            }
            print(f"TTS request params: {params}")
            response = requests.get(self._url, params=params, timeout=30)
            response.raise_for_status()
            return "wav", response.content
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None
