from database.database import engine, Base

class Manage_ORM():
    @staticmethod
    async def create_table_anketa():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @staticmethod
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)        