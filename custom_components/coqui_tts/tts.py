import requests
from homeassistant.components.tts import Provider, Voice

SUPPORT_LANGUAGES = ["sk"]

def get_engine(hass, config, discovery_info=None):
    return CoquiTTSProvider(hass, config)

class CoquiTTSProvider(Provider):
    def __init__(self, hass, config):
        self.hass = hass
        self.name = "Coqui TTS"
        self._url = "http://192.168.88.13:5002/api/tts"

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def default_language(self):
        return "en"

    @property
    def supported_options(self):
        return []

    def get_tts_audio(self, message, language, options=None):
        try:
            data = {
                "text": message,
                "speaker_id": "p316",  # Use the speaker ID that worked in the UI test
                "language_id": "en"    # Specify the language
            }
            response = requests.post(self._url, json=data, timeout=30)
            response.raise_for_status()
            return "wav", response.content
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None
