# Silero TTS Enhanced - Home Assistant Integration

A modern, UI-configurable Home Assistant integration for Silero TTS. No more YAML editing!

This integration connects directly to the **[Silero TTS Enhanced Engine Add-on](https://github.com/indevor/silero-tts-enhanced-addon)** and exposes it as a native Media Player / Voice Assistant TTS provider in Home Assistant.

## Features
- ⚙️ **Config Flow (UI):** Set up IPs, languages, voices, and sample rates entirely via the Home Assistant UI.
- 🗣️ **Voice Assistant Ready:** Fully compatible with Home Assistant's "Assist" feature.
- 🚀 **Asynchronous & Fast:** Uses non-blocking HTTP requests. No system freezes.
-  **Multi-language:** Supports `ru`, `en`, `de`, `es`, `fr`, and more.

## Installation via HACS
1. Ensure you have installed the companion [Silero Add-on](https://github.com/indevor/silero-tts-enhanced-addon) and it's running.
2. Open **HACS** -> **Integrations**.
3. Click the three dots (top right) -> **Custom repositories**.
4. Add this repository URL as an **Integration**.
5. Click **Download**, then **Restart Home Assistant**.

## Setup
1. Go to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for `Silero TTS Enhanced`.
3. Enter your Add-on Server IP (e.g., `http://192.168.1.114:8014`).
4. Select your preferred voice and model. Done!
5. You can select voices and models in the automation settings; see the example.
6. If a model or voice isn't available in the list, you can enter it manually (for example: v5_5_ru)

[Silero Models list](https://github.com/snakers4/silero-models/blob/master/models.yml#L144)

## Usage in Automations
```yaml
service: tts.speak
target:
  entity_id: tts.silero_tts_enhanced
data:
  media_player_entity_id: media_player.living_room
  message: "Hello world, the smart home is ready."
  language: "en"
  options:
    model_id: "v3_en"
    voice: "en_24"
```
## 📝 Acknowledgements & License
This project is an unofficial wrapper/integration. The core Text-to-Speech neural models are developed and owned by the [Silero Team](https://github.com/snakers4/silero-models).
The models are published under the **CC BY-NC** (Non-Commercial) license. Please respect the authors' rights and use this integration strictly for personal, non-commercial purposes.

-----------------------------------------------------------------------
# Silero TTS Enhanced — интеграция с Home Assistant

Современная интеграция Silero TTS с Home Assistant с возможностью настройки интерфейса. Больше не нужно редактировать YAML!

Эта интеграция подключается напрямую к **[дополнению Silero TTS Enhanced Engine](https://github.com/indevor/silero-tts-enhanced-addon)** и предоставляет его в качестве встроенного поставщика TTS для медиаплеера / голосового помощника в Home Assistant.

## Особенности
- ⚙️ **Настройка (интерфейс):** Настраивайте IP-адреса, языки, голоса и частоту дискретизации полностью через интерфейс Home Assistant.
- 🗣️ **Поддержка голосового помощника:** Полная совместимость с функцией «Assist» Home Assistant.
- 🚀 **Асинхронность и скорость:** Использует неблокирующие HTTP-запросы. Система не зависает.
-  **Многоязычность:** Поддерживает `ru`, `en`, `de`, `es`, `fr` и другие языки.

## Установка через HACS
1. Убедитесь, что вы установили сопутствующее [дополнение Silero](https://github.com/indevor/silero-tts-enhanced-addon) и оно запущено.
2. Откройте **HACS** -> **Интеграции**.
3. Нажмите на три точки (вверху справа) -> **Пользовательские репозитории**.
4. Добавьте URL этого репозитория в качестве **Интеграции**.
5. Нажмите **Скачать**, затем **Перезапустить Home Assistant**.

## Настройка
1. Перейдите в **Настройки** -> **Устройства и службы**.
2. Нажмите **+ Добавить интеграцию** и найдите `Silero TTS Enhanced`.
3. Введите IP-адрес вашего сервера дополнения (например, `http://192.168.1.114:8014`).
4. Выберите предпочтительный голос и модель. Готово!
5. Голоса и модели можно выбрать в автоматизации см. пример.
6. Модель и голос можно написать вручню, если он не доступны в списке (например: v5_5_ru)

[Список моделей Silero](https://github.com/snakers4/silero-models/blob/master/models.yml#L144)

```yaml
service: tts.speak
target:
  entity_id: tts.silero_tts_enhanced
data:
  media_player_entity_id: media_player.living_room
  message: "Внимание. Температура процессора достигла 80 градусов."
  options:
    model_id: "v5_ru"
    voice: "xenia"
    put_accent: true
```
## 📝 Лицензия и Авторы
Этот проект является неофициальной интеграцией-оберткой. Сами нейросетевые модели синтеза речи разработаны и принадлежат команде [Silero Team](https://github.com/snakers4/silero-models).
Модели распространяются под некоммерческой лицензией **CC BY-NC**. Пожалуйста, уважайте труд авторов и используйте этот проект только в некоммерческих и личных целях.
