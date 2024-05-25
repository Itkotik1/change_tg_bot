import asyncio
import aiosqlite

async def db_start():
    async with aiosqlite.connect('new.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                age TEXT,
                phone_number TEXT
            )
        """)
        await db.commit()

async def create_profile(user_id):
    async with aiosqlite.connect('new.db') as db:
        cursor = await db.cursor()
        user = await cursor.execute("SELECT 1 FROM profile WHERE user_id=?", (user_id,))
        result = await user.fetchone()
        if not result:
            await cursor.execute("INSERT INTO profile VALUES (?,?,?,?)",
                                 (user_id, '', '', ''))
            await db.commit()

async def save_to_db(data):
    async with aiosqlite.connect('new.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name TEXT, age INTEGER, phone_number TEXT)''')
        await db.execute('''INSERT INTO users (name, age, phone_number) VALUES (?,?,?)''',
                          (data['name'], data['age'], data['phone_number']))
        await db.commit()