from aiogram import Router, F
from aiogram.types import Message
from bot.database import fetch_val, fetch_all, fetch_one
from bot.keyboards import main_menu
from bot.i18n import PHRASES

router = Router()

@router.message(F.text == PHRASES["menu_stats"])
async def show_general_stats(message: Message):
    user_id = message.from_user.id

    learned = await fetch_val(
        "SELECT COUNT(*) FROM word_progress WHERE user_id = $1 AND is_learned = TRUE",
        user_id
    ) or 0

    total_words = await fetch_val(
        "SELECT COUNT(*) FROM word_progress WHERE user_id = $1",
        user_id
    ) or 0

    accuracy_data = await fetch_one(
        """
        SELECT 
            COUNT(*) AS total_attempts,
            SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) AS correct_attempts
        FROM word_attempts
        WHERE user_id = $1
        """,
        user_id
    )

    if accuracy_data and accuracy_data["total_attempts"] > 0:
        total_att = accuracy_data["total_attempts"]
        correct_att = accuracy_data["correct_attempts"]
        accuracy = int(100 * correct_att / total_att)
    else:
        total_att = 0
        accuracy = 0

    words = await fetch_all(
        """
        SELECT w.word
        FROM word_progress wp
        JOIN words w ON wp.word_id = w.id
        WHERE wp.user_id = $1 AND wp.is_learned = TRUE
        ORDER BY w.initial_level, w.word
        LIMIT 30
        """,
        user_id
    )

    if words:
        words_list = "\n".join(f"• {w['word']}" for w in words)
        response = (
            f"{PHRASES['general_stats_title']}\n\n"
            f"{PHRASES['learned_words_count'].format(learned=learned)}\n"
            f"{PHRASES['words_practiced_total'].format(total_words=total_words)}\n"
            f"{PHRASES['total_attempts'].format(total_attempts=total_att)}\n"
            f"{PHRASES['accuracy_overall'].format(accuracy=accuracy)}\n\n"
            f"{PHRASES['learned_words_list']}\n{words_list}"
        )
    else:
        response = (
            f"{PHRASES['no_learned_words']}\n\n"
            f"{PHRASES['total_attempts'].format(total_attempts=total_att)}\n"
            f"{PHRASES['accuracy_overall'].format(accuracy=accuracy)}"
        )

    await message.answer(response, parse_mode="Markdown", reply_markup=main_menu())