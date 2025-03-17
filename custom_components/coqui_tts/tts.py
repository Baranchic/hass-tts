import requests
from homeassistant.components.tts import Provider, Voice

SUPPORT_LANGUAGES = ["sk"]
SUPPORTED_OPTIONS = ["speaker_id"]

def get_engine(hass, config, discovery_info=None):
    return CoquiTTSProvider(hass, config)

class CoquiTTSProvider(Provider):
    def __init__(self, hass, config):
        self.hass = hass
        self.name = "Coqui TTS"
        self._url = "http://192.168.88.13:5002/api/tts"
        self._speakers = ["p234", "p316", "p376"]

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def default_language(self):
        return "en"

    @property
    def supported_options(self):
        return SUPPORTED_OPTIONS

    @property
    def voice_info(self):
        return {speaker: Voice(speaker, speaker) for speaker in self._speakers}

    def get_tts_audio(self, message, language, options=None):
        message = message.strip() if message else "Default message"
        print(f"Sending TTS request: text='{message}', language={language}, options={options}")
        try:
            speaker_id = options.get("speaker_id", "p316") if options else "p316"
            params = {
                "text": message,
                "speaker_id": speaker_id,
                "language_id": "en"
            }
            print(f"TTS request params: {params}")
            response = requests.get(self._url, params=params, timeout=30)
            response.raise_for_status()
            return "wav", response.content
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None
