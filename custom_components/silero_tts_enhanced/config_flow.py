import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.config_entries import OptionsFlowWithReload

DOMAIN = "silero_tts_enhanced"
_LOGGER = logging.getLogger(__name__)

def get_schema(data: dict, is_options: bool = False):
    """Генератор схемы настроек (с возможностью скрытия опций при установке)."""
    schema_dict = {
        vol.Required("host", default=data.get("host", "http://192.168.1.114:8014")): str,
        vol.Required("language", default=data.get("language", "ru")): selector.SelectSelector(
            selector.SelectSelectorConfig(options=["ru", "en", "de", "es", "fr", "tt", "uz", "ua"], custom_value=True)
        ),
        vol.Required("model_id", default=data.get("model_id", "v5_ru")): selector.SelectSelector(
            selector.SelectSelectorConfig(options=["v5_ru", "v4_ru", "v3_1_ru", "v4_en", "v3_en", "v4_de"], custom_value=True)
        ),
        vol.Required("speaker", default=data.get("speaker", "aidar")): str,
        
        vol.Required("sample_rate", default=str(data.get("sample_rate", "48000"))): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "8000", "label": "8000 Hz"},
                    {"value": "24000", "label": "24000 Hz"},
                    {"value": "48000", "label": "48000 Hz"}
                ]
            )
        ),
    }

    # Показываем эти чекбоксы только при редактировании
    if is_options:
        schema_dict.update({
            vol.Required("put_accent", default=data.get("put_accent", True)): bool,
            vol.Required("put_yo", default=data.get("put_yo", True)): bool,
        })

    return vol.Schema(schema_dict)

class SileroTTSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Первый шаг установки интеграции."""
        if user_input is not None:
            user_input["sample_rate"] = int(user_input["sample_rate"])
            # Убедимся, что дефолтные значения сохранятся, даже если полей не было на форме
            user_input.setdefault("put_accent", True)
            user_input.setdefault("put_yo", True)
            return self.async_create_entry(title="Silero TTS", data=user_input)
        
        # Вызываем с is_options=False
        return self.async_show_form(step_id="user", data_schema=get_schema({}, is_options=False))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SileroTTSOptionsFlowHandler()


class SileroTTSOptionsFlowHandler(OptionsFlowWithReload):
    async def async_step_init(self, user_input=None):
        """Форма редактирования настроек."""
        if user_input is not None:
            user_input["sample_rate"] = int(user_input["sample_rate"])
            return self.async_create_entry(title="", data=user_input)

        # --- ВАЖНОЕ ИСПРАВЛЕНИЕ БАГА СЛИЯНИЯ ---
        # Вместо конструкции 'or' безопасно объединяем словари, чтобы не потерять host при сохранении опций
        current = {**self.config_entry.data, **self.config_entry.options}
        
        current["sample_rate"] = str(current.get("sample_rate", 48000))

        # Вызываем с is_options=True
        schema = self.add_suggested_values_to_schema(get_schema(current, is_options=True), current)
        return self.async_show_form(step_id="init", data_schema=schema)
