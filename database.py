import aiosqlite
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)
DB_PATH: str = "bot_database.db"


async def init_db(path: str | None = None):
    global DB_PATH
    if path:
        DB_PATH = path

    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id       INTEGER PRIMARY KEY,
                username      TEXT    DEFAULT '',
                full_name     TEXT    DEFAULT '',
                language      TEXT    DEFAULT 'ru',
                registered    INTEGER DEFAULT 0,
                attempts      INTEGER DEFAULT 0,
                created_at    TEXT,
                registered_at TEXT
            );

            CREATE TABLE IF NOT EXISTS cooldowns (
                user_id    INTEGER PRIMARY KEY,
                expires_at TEXT
            );

            CREATE TABLE IF NOT EXISTS achievements (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                achievement_key TEXT    NOT NULL,
                earned_at       TEXT,
                UNIQUE(user_id, achievement_key)
            );

            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                username    TEXT    DEFAULT '',
                full_name   TEXT    DEFAULT '',
                message     TEXT    NOT NULL,
                status      TEXT    DEFAULT 'open',
                admin_reply TEXT    DEFAULT '',
                created_at  TEXT,
                resolved_at TEXT
            );

            CREATE TABLE IF NOT EXISTS donations (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER NOT NULL,
                amount              INTEGER NOT NULL,
                currency            TEXT    DEFAULT 'XTR',
                provider_payment_id TEXT    DEFAULT '',
                created_at          TEXT
            );
        """)
        await conn.commit()
    logger.info("БД инициализирована: %s", DB_PATH)


# ═══════════ Пользователи ═══════════

async def ensure_user(user_id: int, username: str = "", full_name: str = ""):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            """INSERT INTO users (user_id, username, full_name, created_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET
                   username  = excluded.username,
                   full_name = excluded.full_name""",
            (user_id, username, full_name, datetime.now().isoformat()),
        )
        await conn.commit()


async def is_registered(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        row = await (await conn.execute(
            "SELECT registered FROM users WHERE user_id=?", (user_id,)
        )).fetchone()
        return bool(row and row[0])


async def set_registered(user_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE users SET registered=1, registered_at=? WHERE user_id=?",
            (datetime.now().isoformat(), user_id),
        )
        await conn.commit()


async def increment_attempts(user_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE users SET attempts=attempts+1 WHERE user_id=?", (user_id,)
        )
        await conn.commit()


async def get_attempts(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        row = await (await conn.execute(
            "SELECT attempts FROM users WHERE user_id=?", (user_id,)
        )).fetchone()
        return row[0] if row else 0


async def get_user_language(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as conn:
        row = await (await conn.execute(
            "SELECT language FROM users WHERE user_id=?", (user_id,)
        )).fetchone()
        return row[0] if row else "ru"


async def set_user_language(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE users SET language=? WHERE user_id=?", (lang, user_id)
        )
        await conn.commit()


async def get_user_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as conn:
        total = (await (await conn.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        reged = (await (await conn.execute("SELECT COUNT(*) FROM users WHERE registered=1")).fetchone())[0]
        return {"total": total, "registered": reged}


async def reset_all_registrations() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        count = (await (await conn.execute("SELECT COUNT(*) FROM users WHERE registered=1")).fetchone())[0]
        await conn.execute("UPDATE users SET registered=0, registered_at=NULL")
        await conn.commit()
        return count


# ═══════════ Кулдауны ═══════════

async def set_cooldown(user_id: int, minutes: int):
    expires = (datetime.now() + timedelta(minutes=minutes)).isoformat()
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT OR REPLACE INTO cooldowns (user_id, expires_at) VALUES (?,?)",
            (user_id, expires),
        )
        await conn.commit()


async def get_remaining_cooldown(user_id: int) -> Optional[timedelta]:
    async with aiosqlite.connect(DB_PATH) as conn:
        row = await (await conn.execute(
            "SELECT expires_at FROM cooldowns WHERE user_id=?", (user_id,)
        )).fetchone()
    if row is None:
        return None
    expires = datetime.fromisoformat(row[0])
    now = datetime.now()
    return (expires - now) if now < expires else None


async def reset_all_cooldowns() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        count = (await (await conn.execute("SELECT COUNT(*) FROM cooldowns")).fetchone())[0]
        await conn.execute("DELETE FROM cooldowns")
        await conn.commit()
        return count


async def count_active_cooldowns() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        row = await (await conn.execute(
            "SELECT COUNT(*) FROM cooldowns WHERE expires_at > ?",
            (datetime.now().isoformat(),),
        )).fetchone()
        return row[0]


# ═══════════ Достижения ═══════════

ACHIEVEMENT_DEFS = {
    "first_try": {"ru": "🥇 Прошёл с первой попытки", "en": "🥇 Passed on first try"},
    "perfect":   {"ru": "💎 Все ответы верны",        "en": "💎 Perfect score"},
    "donor":     {"ru": "💰 Меценат",                 "en": "💰 Donor"},
}


async def grant_achievement(user_id: int, key: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        try:
            await conn.execute(
                "INSERT INTO achievements (user_id, achievement_key, earned_at) VALUES (?,?,?)",
                (user_id, key, datetime.now().isoformat()),
            )
            await conn.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def get_achievements(user_id: int) -> list[str]:
    async with aiosqlite.connect(DB_PATH) as conn:
        rows = await (await conn.execute(
            "SELECT achievement_key FROM achievements WHERE user_id=? ORDER BY earned_at",
            (user_id,),
        )).fetchall()
        return [r[0] for r in rows]


# ═══════════ Тикеты ═══════════

async def create_ticket(user_id: int, username: str, full_name: str, message: str) -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute(
            "INSERT INTO tickets (user_id, username, full_name, message, created_at) VALUES (?,?,?,?,?)",
            (user_id, username, full_name, message, datetime.now().isoformat()),
        )
        await conn.commit()
        return cur.lastrowid


async def get_open_tickets() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        rows = await (await conn.execute(
            "SELECT * FROM tickets WHERE status='open' ORDER BY created_at DESC"
        )).fetchall()
        return [dict(r) for r in rows]


async def get_ticket_by_id(ticket_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        row = await (await conn.execute(
            "SELECT * FROM tickets WHERE id=?", (ticket_id,)
        )).fetchone()
        return dict(row) if row else None


async def resolve_ticket(ticket_id: int, admin_reply: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE tickets SET status='resolved', admin_reply=?, resolved_at=? WHERE id=?",
            (admin_reply, datetime.now().isoformat(), ticket_id),
        )
        await conn.commit()


async def get_user_tickets(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        rows = await (await conn.execute(
            "SELECT * FROM tickets WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
            (user_id,),
        )).fetchall()
        return [dict(r) for r in rows]


# ═══════════ Донаты ═══════════

async def save_donation(user_id: int, amount: int, currency: str, provider_id: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO donations (user_id, amount, currency, provider_payment_id, created_at) VALUES (?,?,?,?,?)",
            (user_id, amount, currency, provider_id, datetime.now().isoformat()),
        )
        await conn.commit()


async def get_donation_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as conn:
        total = (await (await conn.execute("SELECT COALESCE(SUM(amount),0) FROM donations")).fetchone())[0]
        count = (await (await conn.execute("SELECT COUNT(*) FROM donations")).fetchone())[0]
        return {"total_amount": total, "count": count}