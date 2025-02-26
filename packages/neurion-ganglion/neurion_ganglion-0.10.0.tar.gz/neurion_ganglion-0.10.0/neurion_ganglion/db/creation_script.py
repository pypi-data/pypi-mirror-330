import asyncio

from neurion_ganglion.db import engine
from neurion_ganglion.db.ion_usage import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

asyncio.run(init_db())