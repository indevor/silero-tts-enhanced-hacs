import logging
import aiohttp
from homeassistant.components.tts import TextToSpeechEntity, ATTR_VOICE
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([SileroTTSAPIEntity(hass, config_entry)])

class SileroTTSAPIEntity(TextToSpeechEntity):
    _attr_name = "Silero TTS Enhanced"
    _attr_has_entity_name = False

    def __init__(self, hass, config_entry):
        self.hass = hass
        
        # Получаем данные: приоритет у измененных (options), если их нет - берем стартовые (data)
        data = config_entry.options if config_entry.options else config_entry.data
        
        self._host = data.get("host").rstrip("/")
        self._lang = data.get("language")
        self._model_id = data.get("model_id", "v5_ru")
        self._sample_rate = data.get("sample_rate", 48000)
        self._speaker = data.get("speaker")
        self._put_accent = data.get("put_accent", True)
        self._put_yo = data.get("put_yo", True)
        
        self._attr_unique_id = f"{config_entry.entry_id}_tts"

    @property
    def supported_languages(self) -> list[str]:
        return ["ru", "en", "de", "es", "fr", "tt", "uz", "ua"]

    @property
    def default_language(self) -> str:
        return self._lang

    @property
    def supported_options(self) -> list[str]:
        # Разрешаем Home Assistant отправлять нам кастомные опции из скриптов
        return [ATTR_VOICE, "model_id", "put_accent", "put_yo", "sample_rate"]

    @property
    def default_options(self) -> dict:
        return {
            ATTR_VOICE: self._speaker,
            "model_id": self._model_id,
            "put_accent": self._put_accent,
            "put_yo": self._put_yo,
            "sample_rate": self._sample_rate
        }

    async def async_get_tts_audio(self, message: str, language: str, options: dict):
        # Если в автоматизации указали другой голос/настройки - берем их, иначе дефолтные
        payload = {
            "text": message, 
            "language": language,
            "voice": options.get(ATTR_VOICE, self._speaker),
            "model_id": options.get("model_id", self._model_id),
            "sample_rate": options.get("sample_rate", self._sample_rate),
            "put_accent": options.get("put_accent", self._put_accent),
            "put_yo": options.get("put_yo", self._put_yo)
        }
        
        session = async_get_clientsession(self.hass)
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with session.post(f"{self._host}/tts", json=payload, timeout=timeout) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    if not audio_data: return None, None
                    return "wav", audio_data
                else:
                    _LOGGER.error("Silero Error: %s", await response.text())
        except Exception as e:
            _LOGGER.error("Silero Connection Error: %s", e)
        return None, None