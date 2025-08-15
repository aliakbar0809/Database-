from database  import DatabaseConfig

async def registration(db, user, password_hash):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (username, password)
                VALUES ($1, $2);
            """, user, password_hash)
    except Exception as e:
        print('Error:', e)


async def login(db: DatabaseConfig, username, password):
    try:
        async with db.pool.acquire() as conn:
            user = await conn.fetchrow("""
                SELECT id FROM users WHERE username = $1 and password = $2
            """, username, password)
            return user if user else None
    except Exception as e:
        print('Error:', e)


async def create_task(db: DatabaseConfig,
                      title: str,
                      description: str,
                      user_id: int):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO todos (title, description, user_id)
                VALUES ($1, $2, $3);
            """, title, description, user_id)
            print('Task added!')
    except Exception as e:
        print('Error:', e)


async def get_tasks(db, user_id):
    try:
        async with db.pool.acquire() as conn:
            tasks = await conn.fetch("""
                SELECT * FROM todos WHERE user_id = $1;
            """, user_id)
            return tasks
    except Exception as e:
        print('Error:', e)


async def update_task(db: DatabaseConfig,
                      task_id: int,
                      title: str,
                      description: str):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
                UPDATE todos SET title=$1, description=$2 WHERE id=$3;
            """, title, description, int(task_id))
            print('Task updated!')
    except Exception as e:
        print('Error:', e)
