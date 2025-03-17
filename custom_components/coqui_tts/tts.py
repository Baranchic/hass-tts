import requests
from homeassistant.components.tts import Provider, Voice

SUPPORT_LANGUAGES = ["sk"]
SUPPORTED_OPTIONS = ["voice"]

def get_engine(hass, config, discovery_info=None):
    return CoquiTTSProvider(hass, config)

class CoquiTTSProvider(Provider):
    def __init__(self, hass, config):
        self.hass = hass
        self.name = "Coqui TTS"
        self._url = "http://192.168.88.13:5002/api/tts"
        # Fetch speakers dynamically (example, adjust based on server API)
        self._speakers = self._fetch_speakers()

    def _fetch_speakers(self):
        try:
            response = requests.get("http://192.168.88.13:5002/api/list_speakers", timeout=30)
            response.raise_for_status()
            return response.json().get("speakers", ["p234", "p316", "p376"])  # Adjust based on API
        except Exception as e:
            print(f"Error fetching speakers: {e}")
            return ["p234", "p316", "p376"]  # Fallback list

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def default_language(self):
        return "en"

    @property
    def default_options(self):
        return {"voice": self._speakers[0] if self._speakers else "p316"}

    @property
    def supported_options(self):
        return SUPPORTED_OPTIONS

    @property
    def voice_info(self):
        return {speaker: Voice(speaker, f"Speaker {speaker}", {"language": "en"}) for speaker in self._speakers}

    def get_tts_audio(self, message, language, options=None):
        if not message or not message.strip():
            print("No valid text provided for synthesis")
            raise ValueError("No valid text provided for synthesis")
        print(f"Sending TTS request: text={message}, language={language}, options={options}")
        try:
            voice = options.get("voice", self._speakers[0] if self._speakers else "p316")
            params = {
                "text": message,
                "speaker_id": voice,
                "language_id": "en",
                "style_wav": ""
            }
            print(f"TTS request params: {params}")
            response = requests.get(self._url, params=params, timeout=30)
            response.raise_for_status()
            return "wav", response.content
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None
