# Spelling Bee Telegram Bot

Telegram bot for learning English spelling through listening practice.

Hear a word → type it → get instant feedback. Perfect for students and language learners!

## Features

- Three difficulty levels: Easy (basic words), Medium (intermediate), Hard (challenging)

- Smart repetition:

  • New words prioritized
  
  • Learned words reappear for reinforcement
  
  • Progress resets on mistakes (spaced repetition)
  
- Multiple accents: US, UK, Australian, Canadian, Indian English

- Detailed statistics:

  • Words learned

  • Accuracy percentage
  
  • Session summaries
  
- Open-source & self-hosted: Full control over your data

## How to Use

### 1. Get Telegram Bot Token

   - Talk to @BotFather
  
   - Create new bot → copy token

### 2. Clone this repository

   git clone https://github.com/suyarugurofu/spelling-bee-telegram-bot.git
   
   cd spelling-bee-telegram-bot

### 3. Configure environment
   cp .env.example .env
   
   nano .env  # Paste your BOT_TOKEN and choose language

   Example .env:
   
   BOT_TOKEN= # your Telegram Bot token after =
   
   BOT_LANG=en  # en, ru, or your custom language code

### 4. Add custom words (optional)

   - Edit migrations/002_load_words.sql
     
   - Add your words in the format: ('word', level)
     
   - Use ON CONFLICT (word) DO NOTHING; to avoid duplicates

### 5. Run with Docker

   docker-compose up --build

### 6. Start in Telegram

   - Open your bot
     
   - Send /start
     
   - Choose difficulty level
     
   - Begin training!

## Localization

### The bot supports multiple languages:

- English (BOT_LANG=en)
  
- Russian (BOT_LANG=ru)

### To add a new language:

1. Create bot/locales/xx.json
   
3. Translate all phrases
   
5. Set BOT_LANG=xx in .env

## Technical Details

- Framework: Aiogram 3.x
- Database: PostgreSQL (included in Docker)
- TTS: Google Text-to-Speech (gTTS)
- Audio: Converted to OGG/Opus for Telegram compatibility
- Architecture: Modular handlers, i18n support, idempotent migrations

License: MIT License — feel free to use, modify, and distribute.

Made with ❤️ for language learners worldwide.
