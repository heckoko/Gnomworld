import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
    BotCommand, ErrorEvent, LabeledPrice, PreCheckoutQuery,
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
)
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from INF import (
    TOKEN, PHOTO, CHANNEL_LINK, CHANNEL_ID,
    PASS_THRESHOLD, COOLDOWN_MINUTES, DB_PATH,
    WELCOME_PHOTO, WELCOME_VIDEO,
    PAYMENT_PROVIDER_TOKEN, ADMIN_PASSWORD,
)
import database as db
from database import ACHIEVEMENT_DEFS
from i18n import t

# ────────── Логирование ──────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ────────── Бот и диспетчер ──────────

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())

# ────────── Изменяемые настройки ──────────

config = {
    "PHOTO": PHOTO,
    "CHANNEL_LINK": CHANNEL_LINK,
    "CHANNEL_ID": CHANNEL_ID,
    "PASS_THRESHOLD": PASS_THRESHOLD,
    "COOLDOWN_MINUTES": COOLDOWN_MINUTES,
    "WELCOME_PHOTO": WELCOME_PHOTO,
    "WELCOME_VIDEO": WELCOME_VIDEO,
}

authorized_admins: set[int] = set()

# ────────── Вопросы ──────────

QUESTIONS = [
    {"text_key": "q_human",     "correct": "yes", "block": True},
    {"text_key": "q_minecraft", "correct": "yes", "block": False},
    {"text_key": "q_cheats",    "correct": "no",  "block": True},
    {"text_key": "q_gnomes",    "correct": "yes", "block": False},
    {"text_key": "q_rules",     "correct": "yes", "block": False},
]
TOTAL = len(QUESTIONS)

# ────────── FSM ──────────

class Quiz(StatesGroup):
    answering = State()

class Admin(StatesGroup):
    password          = State()
    panel             = State()
    edit_link         = State()
    edit_photo        = State()
    edit_threshold    = State()
    edit_cooldown     = State()
    confirm_reset_reg = State()
    confirm_reset_cd  = State()

class Ticket(StatesGroup):
    writing = State()

# ────────── Клавиатуры ──────────

def yn_kb(la: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_yes", la))],
            [KeyboardButton(text=t("btn_no", la))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

lang_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
    InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
]])

donate_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⭐ 10",  callback_data="don:10"),
        InlineKeyboardButton(text="⭐ 20",  callback_data="don:20"),
        InlineKeyboardButton(text="⭐ 50",  callback_data="don:50"),
        InlineKeyboardButton(text="⭐ 100", callback_data="don:100"),
        InlineKeyboardButton(text="⭐ 250", callback_data="don:250"),
    ],
    [
        InlineKeyboardButton(text="⭐ 500",  callback_data="don:500"),
        InlineKeyboardButton(text="⭐ 1000", callback_data="don:1000"),
    ],
])

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Настройки")],
        [KeyboardButton(text="🔗 Ссылка канала")],
        [KeyboardButton(text="🖼 Фото блокировки")],
        [KeyboardButton(text="✅ Порог"), KeyboardButton(text="⏱ Кулдаун")],
        [KeyboardButton(text="👥 Статистика"), KeyboardButton(text="💰 Донаты")],
        [KeyboardButton(text="📩 Тикеты")],
        [KeyboardButton(text="🗑 Сброс регистраций"), KeyboardButton(text="🗑 Сброс кулдаунов")],
        [KeyboardButton(text="🚪 Выйти")],
    ],
    resize_keyboard=True,
)

confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Да, сбросить")],
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True,
)

# ────────── Утилиты ──────────

async def get_lang(uid: int) -> str:
    return await db.get_user_language(uid)


async def send_welcome(message: Message, text: str):
    vid = config["WELCOME_VIDEO"]
    pho = config["WELCOME_PHOTO"]
    if vid:
        await message.answer_video(vid, caption=text)
    elif pho:
        await message.answer_photo(pho, caption=text)
    else:
        await message.answer(text)


# ══════════════════════════════════
#           КОМАНДЫ
# ══════════════════════════════════

@dp.message(CommandStart())
async def cmd_start(message: Message):
    uid = message.from_user.id
    await db.ensure_user(uid, message.from_user.username or "", message.from_user.full_name)
    la = await get_lang(uid)
    await send_welcome(message, t("start_welcome", la, name=message.from_user.full_name))


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(t("help_text", await get_lang(message.from_user.id)))


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    la = await get_lang(message.from_user.id)
    if await state.get_state() is None:
        await message.answer(t("cancel_nothing", la), reply_markup=ReplyKeyboardRemove())
        return
    await state.clear()
    await message.answer(t("cancel_done", la), reply_markup=ReplyKeyboardRemove())


@dp.message(Command("lang"))
async def cmd_lang(message: Message):
    await message.answer(t("lang_choose", await get_lang(message.from_user.id)), reply_markup=lang_kb)


@dp.callback_query(F.data.startswith("lang:"))
async def cb_lang(cb: CallbackQuery):
    la = cb.data.split(":")[1]
    await db.set_user_language(cb.from_user.id, la)
    await cb.message.edit_text(t("lang_set", la))
    await cb.answer()


# ══════════════════════════════════
#    РЕГИСТРАЦИЯ — СНАЧАЛА ТЕСТ
#    ССЫЛКА ТОЛЬКО ПОСЛЕ ПРОХОЖДЕНИЯ
# ══════════════════════════════════

@dp.message(Command("registration"))
async def cmd_reg(message: Message, state: FSMContext):
    uid = message.from_user.id
    await db.ensure_user(uid, message.from_user.username or "", message.from_user.full_name)
    la = await get_lang(uid)

    # Уже прошёл тест — сразу даём ссылку
    if await db.is_registered(uid):
        await message.answer(t("already_registered", la, link=config["CHANNEL_LINK"]))
        return

    # Кулдаун
    rem = await db.get_remaining_cooldown(uid)
    if rem:
        await message.answer(t("cooldown_wait", la, min=rem.seconds // 60, sec=rem.seconds % 60))
        return

    # Ставим кулдаун и считаем попытку
    await db.set_cooldown(uid, config["COOLDOWN_MINUTES"])
    await db.increment_attempts(uid)

    # Запускаем тест
    await state.update_data(score=0, idx=0, lang=la)
    await state.set_state(Quiz.answering)

    q = QUESTIONS[0]
    await message.answer(t("quiz_start", la))
    await message.answer(
        t("quiz_question", la, n=1, total=TOTAL, text=t(q["text_key"], la)),
        reply_markup=yn_kb(la),
    )
    logger.info("Пользователь %s начал тест", uid)


@dp.message(Quiz.answering)
async def quiz_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    la = data.get("lang", "ru")
    idx = data["idx"]
    score = data["score"]
    yes = t("btn_yes", la)
    no = t("btn_no", la)

    if message.text not in (yes, no):
        await message.answer(t("quiz_invalid", la), reply_markup=yn_kb(la))
        return

    q = QUESTIONS[idx]
    ans = "yes" if message.text == yes else "no"
    correct = ans == q["correct"]

    if correct:
        score += 1
    elif q["block"]:
        logger.info("Пользователь %s заблокирован на вопросе %d", message.from_user.id, idx + 1)
        photo = config["PHOTO"]
        txt = t("quiz_blocked", la)
        if photo:
            await message.answer_photo(photo, caption=txt, reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(txt, reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    idx += 1
    if idx < TOTAL:
        await state.update_data(score=score, idx=idx)
        nq = QUESTIONS[idx]
        await message.answer(
            t("quiz_question", la, n=idx + 1, total=TOTAL, text=t(nq["text_key"], la)),
            reply_markup=yn_kb(la),
        )
    else:
        await state.clear()
        await finish_quiz(message, score, la)


async def finish_quiz(message: Message, score: int, la: str):
    uid = message.from_user.id

    if score >= config["PASS_THRESHOLD"]:
        # ── Тест пройден — регистрируем и даём ссылку ──
        await db.set_registered(uid)
        logger.info("Пользователь %s прошёл тест (%d/%d)", uid, score, TOTAL)

        await message.answer(
            t("quiz_passed", la, score=score, total=TOTAL, link=config["CHANNEL_LINK"]),
            reply_markup=ReplyKeyboardRemove(),
        )

        # Достижения
        attempts = await db.get_attempts(uid)
        if attempts == 1 and await db.grant_achievement(uid, "first_try"):
            await message.answer(t("ach_earned", la, name=ACHIEVEMENT_DEFS["first_try"][la]))
        if score == TOTAL and await db.grant_achievement(uid, "perfect"):
            await message.answer(t("ach_earned", la, name=ACHIEVEMENT_DEFS["perfect"][la]))
    else:
        # ── Не прошёл — ссылка НЕ даётся ──
        logger.info("Пользователь %s не прошёл тест (%d/%d)", uid, score, TOTAL)
        await message.answer(
            t("quiz_failed", la, score=score, total=TOTAL),
            reply_markup=ReplyKeyboardRemove(),
        )


# ══════════════════════════════════
#           ДОСТИЖЕНИЯ
# ══════════════════════════════════

@dp.message(Command("achievements"))
async def cmd_ach(message: Message):
    uid = message.from_user.id
    la = await get_lang(uid)
    achs = await db.get_achievements(uid)
    if not achs:
        await message.answer(t("ach_empty", la))
        return
    lines = [ACHIEVEMENT_DEFS.get(k, {}).get(la, k) for k in achs]
    await message.answer(t("ach_title", la, list="\n".join(lines)))


# ══════════════════════════════════
#             ТИКЕТЫ
# ══════════════════════════════════

@dp.message(Command("ticket"))
async def cmd_ticket(message: Message, state: FSMContext):
    la = await get_lang(message.from_user.id)
    await state.set_state(Ticket.writing)
    await message.answer(t("ticket_prompt", la), reply_markup=ReplyKeyboardRemove())


@dp.message(Ticket.writing)
async def ticket_text(message: Message, state: FSMContext):
    la = await get_lang(message.from_user.id)
    if not message.text or len(message.text.strip()) < 5:
        await message.answer(t("ticket_short", la))
        return
    tid = await db.create_ticket(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name,
        message.text.strip(),
    )
    await state.clear()
    await message.answer(t("ticket_created", la, id=tid))


@dp.message(Command("mytickets"))
async def cmd_mytickets(message: Message):
    uid = message.from_user.id
    la = await get_lang(uid)
    tks = await db.get_user_tickets(uid)
    if not tks:
        await message.answer(t("my_tickets_empty", la))
        return
    txt = t("my_tickets_title", la)
    for tk in tks:
        icon = "🟢" if tk["status"] == "open" else "✅"
        txt += f"{icon} <b>#{tk['id']}</b>: {tk['message'][:50]}…\n"
        if tk["admin_reply"]:
            txt += f"   💬 {tk['admin_reply'][:50]}…\n"
    await message.answer(txt)


# ══════════════════════════════════
#             ДОНАТЫ
# ══════════════════════════════════

@dp.message(Command("donate"))
async def cmd_donate(message: Message):
    la = await get_lang(message.from_user.id)
    await message.answer(t("donate_prompt", la), reply_markup=donate_kb)


@dp.callback_query(F.data.startswith("don:"))
async def cb_donate(cb: CallbackQuery):
    amount = int(cb.data.split(":")[1])
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title="Funworld Donate",
        description=f"{amount} ⭐",
        payload=f"donate_{amount}",
        provider_token=PAYMENT_PROVIDER_TOKEN or "",
        currency="XTR",
        prices=[LabeledPrice(label="Donate", amount=amount)],
    )
    await cb.answer()


@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(F.successful_payment)
async def on_payment(message: Message):
    pay = message.successful_payment
    uid = message.from_user.id
    la = await get_lang(uid)

    await db.save_donation(uid, pay.total_amount, pay.currency, pay.provider_payment_charge_id or "")

    if await db.grant_achievement(uid, "donor"):
        await message.answer(t("ach_earned", la, name=ACHIEVEMENT_DEFS["donor"][la]))

    await message.answer(t("donate_thanks", la, amount=pay.total_amount))


# ══════════════════════════════════
#          ИНЛАЙН-РЕЖИМ
# ══════════════════════════════════

@dp.inline_query()
async def inline_share(query: InlineQuery):
    la = await get_lang(query.from_user.id)
    me = await bot.get_me()
    link = f"https://t.me/{me.username}"

    result = InlineQueryResultArticle(
        id="share",
        title=t("inline_title", la),
        description=t("inline_desc", la),
        input_message_content=InputTextMessageContent(
            message_text=t("inline_msg", la, link=link),
            parse_mode=ParseMode.HTML,
        ),
    )
    await query.answer(results=[result], cache_time=300, is_personal=True)

# ══════════════════════════════════
#           ПРАВИЛА
# ══════════════════════════════════

@dp.message(Command("rules"))
async def rule (message: Message):
    await message.answer("Вот все нынешние правила сервера:\n"
                         "1)Не быть мудаком \n"
                         "2) Слушать хоста \n"
                         "3) Не гриферить \n"
                         "4) Не красть \n"
                         "5) Не трогать постройки без разрешения \n"
                         "6) Мега проекты согласовать с админами \n"
                         "7) Слушать админов \n"
                         "8) Уважать гномов \n"
                         "9) Не спамить \n"
                         "10) Желательно не использовать капс \n"
                         "11) Не загружать сервер (оптимизировать механизмы) \n")

# ══════════════════════════════════
#          АДМИН-ПАНЕЛЬ
# ══════════════════════════════════

@dp.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id in authorized_admins:
        await state.set_state(Admin.panel)
        await message.answer("🔐 Админ-панель:", reply_markup=admin_kb)
        return
    await state.set_state(Admin.password)
    await message.answer("🔑 Пароль:", reply_markup=ReplyKeyboardRemove())


@dp.message(Admin.password)
async def admin_pwd(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        authorized_admins.add(message.from_user.id)
        await state.set_state(Admin.panel)
        await message.answer("✅ Добро пожаловать!", reply_markup=admin_kb)
    else:
        await state.clear()
        await message.answer("❌ Неверный пароль.", reply_markup=ReplyKeyboardRemove())


@dp.message(Admin.panel)
async def admin_panel(message: Message, state: FSMContext):
    txt = message.text

    if txt == "📊 Настройки":
        st = await db.get_user_stats()
        cd = await db.count_active_cooldowns()
        don = await db.get_donation_stats()
        await message.answer(
            f"⚙️ <b>Настройки:</b>\n\n"
            f"🔗 Канал: {config['CHANNEL_LINK']}\n"
            f"📡 ID: <code>{config['CHANNEL_ID']}</code>\n"
            f"🖼 Фото: <code>{config['PHOTO'] or '—'}</code>\n"
            f"✅ Порог: {config['PASS_THRESHOLD']}/{TOTAL}\n"
            f"⏱ Кулдаун: {config['COOLDOWN_MINUTES']} мин.\n\n"
            f"👥 Всего: {st['total']}\n"
            f"✅ Зарег: {st['registered']}\n"
            f"⏳ Кулдаун: {cd}\n"
            f"💰 Донаты: {don['count']} ({don['total_amount']} ⭐)"
        )

    elif txt == "🔗 Ссылка канала":
        await state.set_state(Admin.edit_link)
        await message.answer(f"Текущая: {config['CHANNEL_LINK']}\nНовая:", reply_markup=ReplyKeyboardRemove())

    elif txt == "🖼 Фото блокировки":
        await state.set_state(Admin.edit_photo)
        await message.answer("Отправь фото, file_id, URL\n<code>clear</code> — убрать.", reply_markup=ReplyKeyboardRemove())

    elif txt == "✅ Порог":
        await state.set_state(Admin.edit_threshold)
        await message.answer(f"Текущий: {config['PASS_THRESHOLD']}/{TOTAL}\nНовый (1–{TOTAL}):", reply_markup=ReplyKeyboardRemove())

    elif txt == "⏱ Кулдаун":
        await state.set_state(Admin.edit_cooldown)
        await message.answer(f"Текущий: {config['COOLDOWN_MINUTES']} мин.\nНовый:", reply_markup=ReplyKeyboardRemove())

    elif txt == "👥 Статистика":
        st = await db.get_user_stats()
        cd = await db.count_active_cooldowns()
        await message.answer(
            f"👥 Всего: {st['total']}\n"
            f"✅ Зарег: {st['registered']}\n"
            f"⏳ Кулдаунов: {cd}\n"
            f"🔑 Админов: {len(authorized_admins)}"
        )

    elif txt == "💰 Донаты":
        don = await db.get_donation_stats()
        await message.answer(f"💰 Донатов: {don['count']}\nСумма: {don['total_amount']} ⭐")

    elif txt == "📩 Тикеты":
        tks = await db.get_open_tickets()
        if not tks:
            await message.answer("📭 Открытых тикетов нет.")
        else:
            lines = ["📩 <b>Открытые тикеты:</b>\n"]
            for tk in tks[:20]:
                lines.append(
                    f"<b>#{tk['id']}</b> от {tk['full_name']} "
                    f"(@{tk['username'] or '—'})\n"
                    f"   {tk['message'][:80]}\n"
                    f"   📅 {tk['created_at'][:16]}\n"
                )
            lines.append("\nОтветить: <code>/reply НОМЕР текст</code>")
            await message.answer("\n".join(lines))

    elif txt == "🗑 Сброс регистраций":
        await state.set_state(Admin.confirm_reset_reg)
        await message.answer("⚠️ Сбросить ВСЕ регистрации?", reply_markup=confirm_kb)

    elif txt == "🗑 Сброс кулдаунов":
        await state.set_state(Admin.confirm_reset_cd)
        await message.answer("⚠️ Сбросить ВСЕ кулдауны?", reply_markup=confirm_kb)

    elif txt == "🚪 Выйти":
        authorized_admins.discard(message.from_user.id)
        await state.clear()
        await message.answer("🚪 Вышел.", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("⚠️ Используй кнопки.", reply_markup=admin_kb)


# ── Редактирование ──

@dp.message(Admin.edit_link)
async def set_link(message: Message, state: FSMContext):
    config["CHANNEL_LINK"] = message.text.strip()
    await state.set_state(Admin.panel)
    await message.answer(f"✅ Ссылка: {config['CHANNEL_LINK']}", reply_markup=admin_kb)


@dp.message(Admin.edit_photo)
async def set_photo(message: Message, state: FSMContext):
    if message.photo:
        config["PHOTO"] = message.photo[-1].file_id
    else:
        val = message.text.strip()
        config["PHOTO"] = "" if val.lower() == "clear" else val
    await state.set_state(Admin.panel)
    await message.answer(f"✅ Фото: <code>{config['PHOTO'] or '(убрано)'}</code>", reply_markup=admin_kb)


@dp.message(Admin.edit_threshold)
async def set_threshold(message: Message, state: FSMContext):
    try:
        v = int(message.text.strip())
        assert 1 <= v <= TOTAL
    except (ValueError, AssertionError):
        await message.answer(f"⚠️ Число от 1 до {TOTAL}.")
        return
    config["PASS_THRESHOLD"] = v
    await state.set_state(Admin.panel)
    await message.answer(f"✅ Порог: {v}/{TOTAL}", reply_markup=admin_kb)


@dp.message(Admin.edit_cooldown)
async def set_cooldown(message: Message, state: FSMContext):
    try:
        v = int(message.text.strip())
        assert v >= 0
    except (ValueError, AssertionError):
        await message.answer("⚠️ Неотрицательное число.")
        return
    config["COOLDOWN_MINUTES"] = v
    await state.set_state(Admin.panel)
    await message.answer(f"✅ Кулдаун: {v} мин.", reply_markup=admin_kb)


# ── Сброс ──

@dp.message(Admin.confirm_reset_reg)
async def reset_reg(message: Message, state: FSMContext):
    if message.text == "✅ Да, сбросить":
        count = await db.reset_all_registrations()
        await message.answer(f"🗑 Сброшено: {count} чел.", reply_markup=admin_kb)
    else:
        await message.answer("❌ Отменено.", reply_markup=admin_kb)
    await state.set_state(Admin.panel)


@dp.message(Admin.confirm_reset_cd)
async def reset_cd(message: Message, state: FSMContext):
    if message.text == "✅ Да, сбросить":
        count = await db.reset_all_cooldowns()
        await message.answer(f"🗑 Сброшено: {count} чел.", reply_markup=admin_kb)
    else:
        await message.answer("❌ Отменено.", reply_markup=admin_kb)
    await state.set_state(Admin.panel)


# ── /reply ──

@dp.message(Command("reply"))
async def cmd_reply(message: Message):
    if message.from_user.id not in authorized_admins:
        await message.answer("❌ Только для админов.")
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Формат: <code>/reply НОМЕР ответ</code>")
        return

    try:
        tid = int(parts[1])
    except ValueError:
        await message.answer("⚠️ Номер — число.")
        return

    reply_text = parts[2]
    tk = await db.get_ticket_by_id(tid)
    if not tk:
        await message.answer("⚠️ Тикет не найден.")
        return

    await db.resolve_ticket(tid, reply_text)
    await message.answer(f"✅ Тикет #{tid} закрыт.")

    la = await get_lang(tk["user_id"])
    try:
        await bot.send_message(tk["user_id"], t("ticket_reply", la, id=tid, reply=reply_text))
    except Exception:
        logger.warning("Не удалось уведомить %s", tk["user_id"])


# ══════════════════════════════════
#        ОШИБКИ / ПРОЧЕЕ
# ══════════════════════════════════

@dp.error()
async def on_error(event: ErrorEvent):
    logger.error("Ошибка: %s", event.exception, exc_info=True)
    try:
        if event.update.message:
            la = await get_lang(event.update.message.from_user.id)
            await event.update.message.answer(t("error", la))
    except Exception:
        pass


@dp.message()
async def unknown(message: Message, state: FSMContext):
    la = await get_lang(message.from_user.id)
    if await state.get_state():
        await message.answer(t("use_buttons", la))
    else:
        await message.answer(t("unknown", la))


# ══════════════════════════════════
#             ЗАПУСК
# ══════════════════════════════════

async def main():
    await db.init_db(DB_PATH)

    await bot.set_my_commands([
        BotCommand(command="start",        description="Запуск / Start"),
        BotCommand(command="help",         description="Команды / Help"),
        BotCommand(command="registration", description="Проверка / Verify"),
        BotCommand(command="donate",       description="Донат / Donate"),
        BotCommand(command="achievements", description="Достижения / Badges"),
        BotCommand(command="ticket",       description="Тикет / Ticket"),
        BotCommand(command="mytickets",    description="Мои тикеты / My tickets"),
        BotCommand(command="lang",         description="Язык / Language"),
        BotCommand(command="cancel",       description="Отмена / Cancel"),
        BotCommand(command="admin",        description="Админка / Admin"),
        BotCommand(command="rules",        description="Правила / Rules"),
    ])

    logger.info("Запуск бота (polling)...")
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
