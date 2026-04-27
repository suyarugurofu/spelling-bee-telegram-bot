from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from bot.database import execute, fetch_val, fetch_all, fetch_one
from bot.services.tts import get_voice_path
import random
from bot.keyboards import main_menu, training_actions
from bot.i18n import PHRASES

router = Router()
CURRENT_WORDS = {}
CURRENT_SESSIONS = {}

@router.message(F.text == PHRASES["menu_start"])
async def start_training(message: Message):
    user_id = message.from_user.id
    
    user_level = await fetch_val("SELECT training_level FROM users WHERE id = $1", user_id) or 1

    if user_id not in CURRENT_SESSIONS:
        session_id = await fetch_val(
            "INSERT INTO training_sessions (user_id) VALUES ($1) RETURNING id",
            user_id
        )
        CURRENT_SESSIONS[user_id] = session_id
    else:
        session_id = CURRENT_SESSIONS[user_id]

    new_words = await fetch_all(
        """
        SELECT w.id, w.word
        FROM words w
        LEFT JOIN word_progress wp ON w.id = wp.word_id AND wp.user_id = $1
        WHERE w.initial_level = $2 AND wp.word_id IS NULL
        ORDER BY RANDOM() LIMIT 10
        """,
        user_id, user_level
    )

    review_words = await fetch_all(
        """
        SELECT w.id, w.word
        FROM words w
        JOIN word_progress wp ON w.id = wp.word_id
        WHERE 
            wp.user_id = $1 
            AND wp.is_learned = FALSE 
            AND w.initial_level = $2
        ORDER BY RANDOM() LIMIT 10
        """,
        user_id, user_level
    )

    candidates = new_words + review_words
    if not candidates:
        candidates = await fetch_all(
            "SELECT id, word FROM words WHERE initial_level = $1 ORDER BY RANDOM() LIMIT 5",
            user_level
        )

    if not candidates:
        await message.answer(PHRASES["no_words_for_level"], reply_markup=main_menu())
        return

    chosen = random.choice(candidates)
    word = chosen["word"]
    word_id = chosen["id"]

    CURRENT_WORDS[user_id] = {
        "word": word,
        "word_id": word_id,
        "session_id": session_id,
        "attempts": 0
    }

    accent = await fetch_val("SELECT tts_accent FROM users WHERE id = $1", user_id) or 'com'
    voice_path = get_voice_path(word, accent=accent)
    voice = FSInputFile(voice_path)
    await message.answer_voice(
        voice,
        caption=PHRASES["voice_caption"],
        parse_mode="Markdown"
    )

@router.message(F.text == PHRASES["menu_next_word"])
async def next_word(message: Message):
    await start_training(message)

@router.message(F.text == PHRASES["menu_finish_training"])
async def finish_training(message: Message):
    user_id = message.from_user.id
    
    if user_id in CURRENT_WORDS:
        del CURRENT_WORDS[user_id]
    
    session_id = None
    if user_id in CURRENT_SESSIONS:
        session_id = CURRENT_SESSIONS.get(user_id)
        del CURRENT_SESSIONS[user_id]

    stats_row = None
    if session_id:
        stats_row = await fetch_one(
            """
            SELECT 
                COUNT(DISTINCT word_id) AS total_words,
                COUNT(DISTINCT CASE WHEN is_correct THEN word_id END) AS correct_words
            FROM word_attempts
            WHERE session_id = $1
            """,
            session_id
        )

    learned_in_session = 0
    if session_id:
        learned_in_session = await fetch_val(
            """
            SELECT COUNT(*)
            FROM word_progress
            WHERE user_id = $1 
              AND is_learned = TRUE 
              AND last_seen_session_id = $2
            """,
            user_id, session_id
        ) or 0

    parts = []
    if stats_row:
        total = stats_row.get("total_words", 0)
        correct = stats_row.get("correct_words", 0)
        accuracy = int(100 * correct / total) if total > 0 else 0
        parts.append(PHRASES["words_practiced"].format(total=total))
        parts.append(PHRASES["guessed_correctly"].format(correct=correct))
        parts.append(PHRASES["accuracy_percent"].format(accuracy=accuracy))

    if learned_in_session > 0:
        parts.insert(0, PHRASES["learned_in_session"].format(count=learned_in_session))

    if parts:
        response = f"{PHRASES['session_summary_title']}\n" + "\n".join(parts)
        await message.answer(response)

    await message.answer(PHRASES["training_finished"], reply_markup=main_menu())

@router.message(F.text)
async def handle_word_input(message: Message):
    text = message.text.strip()

    user_id = message.from_user.id
    if user_id not in CURRENT_WORDS:
        await message.answer(PHRASES["menu_start"], reply_markup=main_menu())
        return

    data = CURRENT_WORDS[user_id]
    correct_word = data["word"]
    word_id = data["word_id"]
    attempts = data.get("attempts", 0) + 1
    session_id = data["session_id"]

    is_correct = (text.lower().strip() == correct_word.lower())

    await execute(
        "INSERT INTO word_attempts (user_id, word_id, is_correct, session_id) VALUES ($1, $2, $3, $4)",
        user_id, word_id, is_correct, session_id
    )

    progress = await fetch_one(
        """
        SELECT correct_count, is_learned, last_seen_session_id
        FROM word_progress
        WHERE user_id = $1 AND word_id = $2
        """,
        user_id, word_id
    )

    if is_correct:
        if progress and progress["is_learned"]:
            await message.answer(PHRASES["already_learned"], reply_markup=training_actions())
            del CURRENT_WORDS[user_id]
            return

        current_count = progress["correct_count"] if progress else 0
        new_count = current_count + 1 

        is_now_learned = new_count >= 3

        if progress:
            await execute(
                """
                UPDATE word_progress
                SET correct_count = $1, is_learned = $2, last_seen_session_id = $3
                WHERE user_id = $4 AND word_id = $5
                """,
                new_count, is_now_learned, session_id, user_id, word_id
            )
        else:
            await execute(
                """
                INSERT INTO word_progress (user_id, word_id, correct_count, is_learned, last_seen_session_id)
                VALUES ($1, $2, $3, $4, $5)
                """,
                user_id, word_id, new_count, is_now_learned, session_id
            )

        if is_now_learned:
            await message.answer(PHRASES["word_learned"].format(word=correct_word), parse_mode="Markdown")
        elif new_count > 0:
            await message.answer(PHRASES["correct_progress"].format(count=new_count))
        else:
            await message.answer("✅ Correct!")

        await message.answer(PHRASES["what_next"], reply_markup=training_actions())
        del CURRENT_WORDS[user_id]

    else:
        was_learned_before = progress and progress.get("is_learned", False)

        if progress:
            await execute(
                """
                UPDATE word_progress
                SET correct_count = 0, is_learned = FALSE, last_seen_session_id = $1
                WHERE user_id = $2 AND word_id = $3
                """,
                session_id, user_id, word_id
            )

        if was_learned_before:
            await message.answer(f"⚠️ {PHRASES['word_learned'].format(word=correct_word)}", parse_mode="Markdown")

        if attempts >= 3:
            await message.answer(PHRASES["show_correct"].format(word=data['word']), parse_mode="Markdown")
            await message.answer(PHRASES["what_next"], reply_markup=training_actions())
            del CURRENT_WORDS[user_id]
        else:
            data["attempts"] = attempts
            await message.answer(PHRASES["wrong_attempt"].format(attempt=attempts))