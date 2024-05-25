import asyncio
import aiosqlite


async def db_start():
    async with aiosqlite.connect('new.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                phone_number TEXT
            )
        """)
        await db.commit()


async def register_or_update_user(user_id, name, age, phone_number):
    async with aiosqlite.connect('new.db') as db:
        cursor = await db.cursor()

        user_exists = await cursor.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
        result = await user_exists.fetchone()

        if not result:

            await cursor.execute("INSERT INTO users VALUES (?,?,?,?)", (user_id, name, int(age), phone_number))
        else:

            await cursor.execute("UPDATE users SET name=?, age=?, phone_number=? WHERE user_id=?",
                                 (name, int(age), phone_number, user_id))

        await db.commit()
