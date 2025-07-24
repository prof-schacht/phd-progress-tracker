import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.models.user import UserRole


async def create_first_superuser(db: AsyncSession) -> None:
    """Create the first superuser if it doesn't exist"""
    # Check if superuser exists
    existing_user = await UserService.get_user_by_email(
        db, email=settings.FIRST_SUPERUSER
    )
    
    if not existing_user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="System Administrator",
            role=UserRole.SYSTEM_ADMIN
        )
        await UserService.create_user(db, user_in)
        print(f"Created superuser: {settings.FIRST_SUPERUSER}")
    else:
        print(f"Superuser already exists: {settings.FIRST_SUPERUSER}")


async def init_db() -> None:
    """Initialize database with initial data"""
    async with AsyncSessionLocal() as db:
        await create_first_superuser(db)


if __name__ == "__main__":
    asyncio.run(init_db())