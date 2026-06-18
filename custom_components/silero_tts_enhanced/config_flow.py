import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.config_entries import OptionsFlowWithReload

DOMAIN = "silero_tts_enhanced"
_LOGGER = logging.getLogger(__name__)

def get_schema(data: dict):
    """Генератор схемы настроек (используется и при установке, и при редактировании)."""
    return vol.Schema({
        vol.Required("host", default=data.get("host", "http://192.168.1.114:8014")): str,
        vol.Required("language", default=data.get("language", "ru")): selector.SelectSelector(
            selector.SelectSelectorConfig(options=["ru", "en", "de", "es", "fr", "tt", "uz", "ua"], custom_value=True)
        ),
        vol.Required("model_id", default=data.get("model_id", "v5_ru")): selector.SelectSelector(
            selector.SelectSelectorConfig(options=["v5_ru", "v4_ru", "v3_1_ru", "v4_en", "v3_en", "v4_de"], custom_value=True)
        ),
        vol.Required("speaker", default=data.get("speaker", "aidar")): str,
        
        # --- ИСПРАВЛЕННЫЙ БЛОК ЧАСТОТЫ ДИСКРЕТИЗАЦИИ ---
        vol.Required("sample_rate", default=str(data.get("sample_rate", "48000"))): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "8000", "label": "8000 Hz"},
                    {"value": "24000", "label": "24000 Hz"},
                    {"value": "48000", "label": "48000 Hz"}
                ]
            )
        ),
        # ------------------------------------------------
        
        vol.Required("put_accent", default=data.get("put_accent", True)): bool,
        vol.Required("put_yo", default=data.get("put_yo", True)): bool,
    })

class SileroTTSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Первый шаг установки интеграции."""
        if user_input is not None:
            # Конвертируем обратно в число перед сохранением
            user_input["sample_rate"] = int(user_input["sample_rate"])
            return self.async_create_entry(title="Silero TTS", data=user_input)
        return self.async_show_form(step_id="user", data_schema=get_schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Вернуть обработчик опций (кнопка «Настроить»)."""
        return SileroTTSOptionsFlowHandler()


class SileroTTSOptionsFlowHandler(OptionsFlowWithReload):
    """Обработчик изменения настроек (шестерёнка). Наследуемся от OptionsFlowWithReload,
    чтобы автоматически перезагружать интеграцию после сохранения."""

    async def async_step_init(self, user_input=None):
        """Форма редактирования настроек."""
        if user_input is not None:
            # Конвертируем обратно в число перед сохранением
            user_input["sample_rate"] = int(user_input["sample_rate"])
            # Сохраняем новые опции; перезагрузка произойдёт автоматически благодаря OptionsFlowWithReload
            return self.async_create_entry(title="", data=user_input)

        # Берём текущие значения и переводим в стандартный словарь
        current = dict(self.config_entry.options or self.config_entry.data)
        
        # Конвертируем сохраненное число в строку для безопасной подстановки в выпадающий список
        current["sample_rate"] = str(current.get("sample_rate", 48000))

        # Подставляем текущие значения в схему
        schema = self.add_suggested_values_to_schema(get_schema(current), current)
        return self.async_show_form(step_id="init", data_schema=schema)
