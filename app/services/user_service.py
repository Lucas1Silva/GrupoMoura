from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, auth

async def create_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    db_user = result.scalars().first()
    if db_user:
        return None
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
