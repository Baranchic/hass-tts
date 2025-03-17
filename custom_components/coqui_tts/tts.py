import requests
from homeassistant.components.tts import Provider, Voice

SUPPORT_LANGUAGES = ["en"]

def get_engine(hass, config, discovery_info=None):
    return CoquiTTSProvider(hass, config)

class CoquiTTSProvider(Provider):
    def __init__(self, hass, config):
        self.hass = hass
        self.name = "Coqui TTS"
        self._url = "http://192.168.88.13:5002/api/tts"  # Changed to /api/tts

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
            response = requests.post(self._url, json={"text": message}, timeout=30)
            response.raise_for_status()
            return "wav", response.content
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None
