import asyncpg

class DatabaseConfig:
    def __init__(self, user, password, db_name, port=5432, host='127.0.0.1'):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port
        self.host = host
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=self.user,
                password=self.password,
                database=self.db_name,
                port=self.port,
                host=self.host
            )
        except Exception as e:
            print('Error1:', e)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL 
                    );
                    CREATE TABLE IF NOT EXISTS todos (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        created_at DATE DEFAULT CURRENT_DATE,
                        user_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE                       
                    );
                """)
        except Exception as e:
            print('Create table error:', e)


async def get_db() -> DatabaseConfig:
    try:
        db = DatabaseConfig(
            user='postgres',
            password='aliakbar2008',
            db_name='todo'
        )
        await db.connect()
        await db.create_tables()
        return db
    except Exception as e:
        print('DB init error:', e)

