# AITradingMT5

Project AI Trading untuk MetaTrader 5 dengan bridge Python, AI agent, dan aplikasi Android.

## Struktur Project

```
AITradingMT5/
├── .github/workflows/build-apk.yml      <- GitHub Actions: build APK otomatis
├── .gitignore
├── README.md
├── config.example.env                   <- Konfigurasi (salin ke .env)
├── mt5_bridge/
│   ├── bridge_server.py                 <- Server bridge MT5 (Flask)
│   ├── mt5_connector.py                 <- Koneksi ke MT5 Terminal
│   ├── signals.py                       <- Analisis swing high/low & sinyal
│   ├── telegram_notifier.py             <- Notifikasi ke Telegram
│   └── requirements.txt                 <- Dependensi Python
├── ai_agent/
│   ├── config.py
│   ├── market_analyzer.py
│   └── opportunity_finder.py            <- AI cari peluang trading terbaik
└── android_app/
    ├── build.gradle.kts
    ├── settings.gradle.kts
    └── app/
        ├── build.gradle.kts
        ├── src/main/AndroidManifest.xml
        ├── src/main/java/com/mausbot/aitradingmt5/
        │   ├── MainActivity.kt
        │   ├── TradingViewModel.kt
        │   ├── MT5Service.kt
        │   ├── models/ (Asset, TradeSignal, Portfolio)
        │   └── ui/AssetAdapter.kt
        └── src/main/res/                <- layout, values, drawable
```

## Setup

1. Salin `config.example.env` ke `.env` dan isi nilai yang diperlukan.
2. Jalankan `mt5_bridge/bridge_server.py` di desktop tempat MT5 berjalan.
3. Edit `BRIDGE_URL` di `MT5Service.kt` agar mengarah ke IP desktop Anda.
4. Unggah ke GitHub dan aktifkan GitHub Actions untuk build APK otomatis.

## Konfigurasi .env

```
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=Headway-Real
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=8000471218
OPENAI_API_KEY=your_openai_key
BRIDGE_URL=http://your-desktop-ip:5000
```