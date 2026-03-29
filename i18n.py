TEXTS: dict[str, dict[str, str]] = {
    "start_welcome": {
        "ru": "👋 Привет, <b>{name}</b>!\nЭто бот канала <b>Funworld</b>.\n/help — список команд\n🌐 Сменить язык → /lang",
        "en": "👋 Hi, <b>{name}</b>!\nThis is the <b>Funworld</b> bot.\n/help — commands\n🌐 Change language → /lang",
    },
    "help_text": {
        "ru": (
            "📋 <b>Команды:</b>\n\n"
            "/start — приветствие\n"
            "/help — список команд\n"
            "/registration — проверка для входа\n"
            "/donate — поддержка сервера\n"
            "/achievements — достижения\n"
            "/ticket — написать жалобу\n"
            "/mytickets — мои тикеты\n"
            "/lang — сменить язык\n"
            "/cancel — отменить действие\n"
            "/admin — админ-панель"
        ),
        "en": (
            "📋 <b>Commands:</b>\n\n"
            "/start — greeting\n"
            "/help — command list\n"
            "/registration — verification\n"
            "/donate — support server\n"
            "/achievements — badges\n"
            "/ticket — submit a ticket\n"
            "/mytickets — my tickets\n"
            "/lang — change language\n"
            "/cancel — cancel action\n"
            "/admin — admin panel"
        ),
    },
    "cancel_nothing": {
        "ru": "Нечего отменять 🤷",
        "en": "Nothing to cancel 🤷",
    },
    "cancel_done": {
        "ru": "Действие отменено ✅",
        "en": "Action cancelled ✅",
    },
    "already_registered": {
        "ru": "Ты уже зарегистрирован ✅\n🔗 Ссылка: {link}",
        "en": "Already registered ✅\n🔗 Link: {link}",
    },
    "not_subscribed": {
        "ru": "⚠️ Сначала подпишись на канал:\n{link}\n\nПотом нажми /registration",
        "en": "⚠️ Subscribe to the channel first:\n{link}\n\nThen press /registration",
    },
    "cooldown_wait": {
        "ru": "⏳ Подожди {min} мин. {sec} сек.",
        "en": "⏳ Wait {min} min {sec} sec.",
    },
    "quiz_start": {
        "ru": "📝 Пройди проверку:",
        "en": "📝 Complete the verification:",
    },
    "quiz_question": {
        "ru": "Вопрос {n}/{total}: {text}",
        "en": "Question {n}/{total}: {text}",
    },
    "quiz_invalid": {
        "ru": "⚠️ Выбери <b>Да</b> или <b>Нет</b>.",
        "en": "⚠️ Choose <b>Yes</b> or <b>No</b>.",
    },
    "quiz_blocked": {
        "ru": "🚫 Доступ запрещён.\nПопробуй позже: /registration",
        "en": "🚫 Access denied.\nTry later: /registration",
    },
    "quiz_passed": {
        "ru": "🎉 <b>Поздравляю!</b>\nВерных: {score}/{total} ✅\n\n🔗 Ссылка:\n{link}",
        "en": "🎉 <b>Congrats!</b>\nCorrect: {score}/{total} ✅\n\n🔗 Link:\n{link}",
    },
    "quiz_failed": {
        "ru": "😔 Не прошёл.\nВерных: {score}/{total} ❌\n\nПопробуй: /registration",
        "en": "😔 Failed.\nCorrect: {score}/{total} ❌\n\nRetry: /registration",
    },
    "ach_title": {
        "ru": "🏆 <b>Достижения:</b>\n\n{list}",
        "en": "🏆 <b>Achievements:</b>\n\n{list}",
    },
    "ach_empty": {
        "ru": "Достижений пока нет 😢",
        "en": "No achievements yet 😢",
    },
    "ach_earned": {
        "ru": "🏆 Новое достижение: <b>{name}</b>",
        "en": "🏆 New achievement: <b>{name}</b>",
    },
    "ticket_prompt": {
        "ru": "📩 Опиши проблему (одним сообщением):",
        "en": "📩 Describe your issue (one message):",
    },
    "ticket_created": {
        "ru": "✅ Тикет #{id} создан.",
        "en": "✅ Ticket #{id} created.",
    },
    "ticket_short": {
        "ru": "⚠️ Слишком коротко. Напиши подробнее.",
        "en": "⚠️ Too short. Give more details.",
    },
    "my_tickets_title": {
        "ru": "📋 <b>Твои тикеты:</b>\n\n",
        "en": "📋 <b>Your tickets:</b>\n\n",
    },
    "my_tickets_empty": {
        "ru": "Тикетов нет. Создай: /ticket",
        "en": "No tickets. Create: /ticket",
    },
    "ticket_reply": {
        "ru": "💬 Ответ на тикет #{id}:\n\n{reply}",
        "en": "💬 Reply to ticket #{id}:\n\n{reply}",
    },
    "donate_prompt": {
        "ru": "💰 <b>Поддержи сервер!</b>\nВыбери сумму:",
        "en": "💰 <b>Support the server!</b>\nChoose amount:",
    },
    "donate_thanks": {
        "ru": "🎉 Спасибо за {amount} ⭐!",
        "en": "🎉 Thanks for {amount} ⭐!",
    },
    "lang_choose": {
        "ru": "🌐 Выбери язык:",
        "en": "🌐 Choose language:",
    },
    "lang_set": {
        "ru": "✅ Русский 🇷🇺",
        "en": "✅ English 🇬🇧",
    },
    "inline_title": {
        "ru": "Поделиться ботом Funworld",
        "en": "Share Funworld Bot",
    },
    "inline_desc": {
        "ru": "Отправить ссылку друзьям",
        "en": "Send link to friends",
    },
    "inline_msg": {
        "ru": "👋 Заходи в <b>Funworld</b>!\nБот: {link}",
        "en": "👋 Join <b>Funworld</b>!\nBot: {link}",
    },
    "unknown": {
        "ru": "🤔 Не понимаю. /help",
        "en": "🤔 Unknown. /help",
    },
    "use_buttons": {
        "ru": "⚠️ Используй кнопки или /cancel",
        "en": "⚠️ Use buttons or /cancel",
    },
    "error": {
        "ru": "⚙️ Ошибка. Попробуй позже.",
        "en": "⚙️ Error. Try later.",
    },
    "q_human":     {"ru": "Ты человек?",                   "en": "Are you human?"},
    "q_minecraft": {"ru": "Ты играешь в Minecraft?",       "en": "Do you play Minecraft?"},
    "q_cheats":    {"ru": "Ты используешь читы?",          "en": "Do you use cheats?"},
    "q_gnomes":    {"ru": "Ты уважаешь гномов?",           "en": "Do you respect gnomes?"},
    "q_rules":     {"ru": "Ты соблюдаешь правила сервера?", "en": "Do you follow server rules?"},
    "btn_yes":     {"ru": "Да",  "en": "Yes"},
    "btn_no":      {"ru": "Нет", "en": "No"},
}


def t(key: str, lang: str = "ru", **kw) -> str:
    entry = TEXTS.get(key, {})
    text = entry.get(lang, entry.get("ru", f"[{key}]"))
    if kw:
        text = text.format(**kw)
    return text