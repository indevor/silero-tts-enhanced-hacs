# Silero TTS Enhanced - Home Assistant Integration

A modern, UI-configurable Home Assistant integration for Silero TTS. No more YAML editing!

This integration connects directly to the **Silero TTS Enhanced Engine Add-on** and exposes it as a native Media Player / Voice Assistant TTS provider in Home Assistant.

## Features
- ⚙️ **Config Flow (UI):** Set up IPs, languages, voices, and sample rates entirely via the Home Assistant UI.
- 🗣️ **Voice Assistant Ready:** Fully compatible with Home Assistant's "Assist" feature.
- 🚀 **Asynchronous & Fast:** Uses non-blocking HTTP requests. No system freezes.
- 🇷🇺🇺🇸 **Multi-language:** Supports `ru`, `en`, `de`, `es`, `fr`, and more.

## Installation via HACS
1. Ensure you have installed the companion [Silero Add-on](ССЫЛКА_НА_РЕПОЗИТОРИЙ_1) and it's running.
2. Open **HACS** -> **Integrations**.
3. Click the three dots (top right) -> **Custom repositories**.
4. Add this repository URL as an **Integration**.
5. Click **Download**, then **Restart Home Assistant**.

## Setup
1. Go to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for `Silero TTS Enhanced`.
3. Enter your Add-on Server IP (e.g., `http://192.168.1.114:8014`).
4. Select your preferred voice and model. Done!

## Usage in Automations
```yaml
service: tts.speak
target:
  entity_id: tts.silero_tts_enhanced
data:
  cache: true
  media_player_entity_id: media_player.living_room_speaker
  message: "Hello!"
