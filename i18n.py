TEXTS: dict[str, dict[str, str]] = {
    "start_welcome": {
        "ru": "👋 Привет, <b>{name}</b>!\nЭто бот канала <b>Gnom world</b>.\n/help — список команд\n🌐 Сменить язык → /lang.\n/rules — список правил сервера, обязательно к прочтению",
        "en": "👋 Hi, <b>{name}</b>!\nThis is the <b>Gnom world</b> bot.\n/help — commands\n🌐 Change language → /lang.\n/rules — rules, must read",
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
            "/admin — админ-панель\n"
            "/rules — правила сервера"
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
            "/admin — admin panel\n"
            "/rules — server rules"
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

    # ── Кнопки Да / Нет ──
    "btn_yes": {"ru": "Да", "en": "Yes"},
    "btn_no":  {"ru": "Нет", "en": "No"},

    # ══════════════════════════════════════════════════
    #   ВОПРОСЫ (50 штук) — text_key для ALL_QUESTIONS
    # ══════════════════════════════════════════════════

    # --- 1–5: Базовые (оригинальные) ---
    "q_human": {
        "ru": "Ты человек?",
        "en": "Are you human?",
    },
    "q_minecraft": {
        "ru": "Ты играешь в Minecraft?",
        "en": "Do you play Minecraft?",
    },
    "q_cheats": {
        "ru": "Ты используешь читы?",
        "en": "Do you use cheats?",
    },
    "q_gnomes": {
        "ru": "Ты уважаешь гномов?",
        "en": "Do you respect gnomes?",
    },
    "q_rules": {
        "ru": "Ты соблюдаешь правила сервера?",
        "en": "Do you follow server rules?",
    },

    # --- 6–10 ---
    "q_respect_players": {
        "ru": "Нужно ли уважать других игроков?",
        "en": "Should you respect other players?",
    },
    "q_grief_ok": {
        "ru": "Можно ли гриферить на сервере?",
        "en": "Is griefing allowed on the server?",
    },
    "q_steal_items": {
        "ru": "Можно ли воровать у других игроков?",
        "en": "Can you steal from other players?",
    },
    "q_listen_admins": {
        "ru": "Нужно ли слушать админов?",
        "en": "Should you listen to admins?",
    },
    "q_spam_chat": {
        "ru": "Можно ли спамить в чате?",
        "en": "Is spamming in chat allowed?",
    },

    # --- 11–15 ---
    "q_build_perm": {
        "ru": "Нужно ли спрашивать разрешение перед тем, как трогать чужие постройки?",
        "en": "Should you ask permission before touching others' builds?",
    },
    "q_mega_project": {
        "ru": "Нужно ли согласовывать мега-проекты с админами?",
        "en": "Should you coordinate mega-projects with admins?",
    },
    "q_caps_ok": {
        "ru": "Приветствуется ли постоянное использование капса в чате?",
        "en": "Is constant caps lock usage encouraged in chat?",
    },
    "q_optimize_builds": {
        "ru": "Нужно ли оптимизировать механизмы, чтобы не нагружать сервер?",
        "en": "Should you optimize mechanisms to reduce server load?",
    },
    "q_play_fair": {
        "ru": "Нужно ли играть честно?",
        "en": "Should you play fair?",
    },

    # --- 16–20 ---
    "q_xray_allowed": {
        "ru": "Разрешён ли X-ray на сервере?",
        "en": "Is X-ray allowed on the server?",
    },
    "q_help_newbies": {
        "ru": "Стоит ли помогать новичкам на сервере?",
        "en": "Should you help newbies on the server?",
    },
    "q_pvp_no_consent": {
        "ru": "Можно ли атаковать игроков без их согласия?",
        "en": "Can you attack players without their consent?",
    },
    "q_follow_host": {
        "ru": "Нужно ли слушать хоста?",
        "en": "Should you listen to the host?",
    },
    "q_bug_exploit": {
        "ru": "Можно ли использовать баги и эксплойты в свою пользу?",
        "en": "Can you exploit bugs for your benefit?",
    },

    # --- 21–25 ---
    "q_share_coords": {
        "ru": "Стоит ли делиться координатами интересных мест с другими?",
        "en": "Should you share coords of interesting places with others?",
    },
    "q_destroy_spawn": {
        "ru": "Можно ли разрушать спаун?",
        "en": "Can you destroy the spawn?",
    },
    "q_afk_machines": {
        "ru": "Разрешены ли AFK-машины без ограничений?",
        "en": "Are unlimited AFK machines allowed?",
    },
    "q_report_bugs": {
        "ru": "Стоит ли сообщать админам о найденных багах?",
        "en": "Should you report bugs to admins?",
    },
    "q_hate_speech": {
        "ru": "Допустима ли речь ненависти на сервере?",
        "en": "Is hate speech acceptable on the server?",
    },

    # --- 26–30 ---
    "q_teamwork": {
        "ru": "Приветствуется ли командная работа на сервере?",
        "en": "Is teamwork encouraged on the server?",
    },
    "q_lava_grief": {
        "ru": "Можно ли заливать чужие постройки лавой?",
        "en": "Can you pour lava on others' builds?",
    },
    "q_respect_builds": {
        "ru": "Нужно ли уважать чужие постройки?",
        "en": "Should you respect others' builds?",
    },
    "q_mod_approval": {
        "ru": "Нужно ли одобрение модераторов для крупных проектов?",
        "en": "Do large projects need moderator approval?",
    },
    "q_tnt_everywhere": {
        "ru": "Можно ли ставить TNT где угодно на сервере?",
        "en": "Can you place TNT anywhere on the server?",
    },

    # --- 31–35 ---
    "q_be_kind": {
        "ru": "Нужно ли быть добрым к другим игрокам?",
        "en": "Should you be kind to other players?",
    },
    "q_trade_fair": {
        "ru": "Нужно ли торговать честно с другими игроками?",
        "en": "Should you trade fairly with other players?",
    },
    "q_impersonate": {
        "ru": "Можно ли выдавать себя за админа?",
        "en": "Can you impersonate an admin?",
    },
    "q_protect_env": {
        "ru": "Стоит ли беречь окружающий мир на сервере?",
        "en": "Should you protect the server environment?",
    },
    "q_duplication": {
        "ru": "Разрешён ли дюп (дублирование) предметов?",
        "en": "Is item duplication allowed?",
    },

    # --- 36–40 ---
    "q_community_event": {
        "ru": "Стоит ли участвовать в событиях сообщества?",
        "en": "Should you participate in community events?",
    },
    "q_block_entrance": {
        "ru": "Можно ли блокировать вход в чужие базы?",
        "en": "Can you block entrances to others' bases?",
    },
    "q_ask_before_take": {
        "ru": "Нужно ли спрашивать, прежде чем брать чужие вещи?",
        "en": "Should you ask before taking others' stuff?",
    },
    "q_swear_ok": {
        "ru": "Приветствуется ли ругань и мат в чате?",
        "en": "Is swearing in chat encouraged?",
    },
    "q_redstone_lag": {
        "ru": "Можно ли строить редстоун-механизмы, которые вызывают сильные лаги?",
        "en": "Can you build redstone mechanisms that cause heavy lag?",
    },

    # --- 41–45 ---
    "q_welcome_new": {
        "ru": "Стоит ли приветствовать новых игроков?",
        "en": "Should you welcome new players?",
    },
    "q_fly_hack": {
        "ru": "Можно ли использовать хак на полёт?",
        "en": "Can you use fly hacks?",
    },
    "q_base_claim": {
        "ru": "Нужно ли отмечать границы своей территории?",
        "en": "Should you mark your territory borders?",
    },
    "q_kill_pets": {
        "ru": "Можно ли убивать питомцев других игроков?",
        "en": "Can you kill other players' pets?",
    },
    "q_share_food": {
        "ru": "Стоит ли делиться едой с голодными игроками?",
        "en": "Should you share food with hungry players?",
    },

    # --- 46–50 ---
    "q_server_lag": {
        "ru": "Можно ли намеренно лагать сервер?",
        "en": "Can you intentionally lag the server?",
    },
    "q_mini_game": {
        "ru": "Приветствуются ли мини-игры на сервере?",
        "en": "Are mini-games welcomed on the server?",
    },
    "q_respect_border": {
        "ru": "Нужно ли уважать границы чужих территорий?",
        "en": "Should you respect others' territory borders?",
    },
    "q_use_common": {
        "ru": "Можно ли пользоваться общими ресурсами сервера?",
        "en": "Can you use the server's common resources?",
    },
    "q_autoclick": {
        "ru": "Разрешены ли автокликеры на сервере?",
        "en": "Are auto-clickers allowed on the server?",
    },
}


def t(key: str, lang: str = "ru", **kw) -> str:
    entry = TEXTS.get(key, {})
    text = entry.get(lang, entry.get("ru", f"[{key}]"))
    if kw:
        text = text.format(**kw)
    return text
