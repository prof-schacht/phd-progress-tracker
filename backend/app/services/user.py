from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role=user_in.role,
            status=user_in.status
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        # Create user profile
        db_profile = UserProfile(user_id=db_user.id)
        db.add(db_profile)
        await db.commit()
        
        return db_user
    
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """Update user"""
        result = await db.execute(select(User).filter(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        update_data = user_in.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = await UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete user"""
        result = await db.execute(select(User).filter(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return False
        
        await db.delete(db_user)
        await db.commit()
        return True