import aiomysql
from modules.config import db
async def _init():
    global pool

pool = None

async def sql_exec(statement: str) -> None:
    if not pool:
        pool = await aiomysql.create_pool(
            host = db.host, port = db.port,
            db = db.name,
            user = db.user,
            password = db.password,
            autocommit=True
        )

    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(statement)
            return await cursor.fetchall()