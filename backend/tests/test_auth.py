import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.core.config import settings
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.models.user import UserRole


@pytest.mark.asyncio
async def test_login(client: AsyncClient, db: AsyncSession):
    """Test user login"""
    # Create test user
    user_in = UserCreate(
        email="test@example.com",
        password="testpassword",
        full_name="Test User",
        role=UserRole.STUDENT
    )
    await UserService.create_user(db, user_in)
    
    # Test login
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_incorrect_password(client: AsyncClient, db: AsyncSession):
    """Test login with incorrect password"""
    # Create test user
    user_in = UserCreate(
        email="test2@example.com",
        password="testpassword",
        full_name="Test User",
        role=UserRole.STUDENT
    )
    await UserService.create_user(db, user_in)
    
    # Test login with wrong password
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test2@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, db: AsyncSession):
    """Test getting current user info"""
    # Create and login user
    user_in = UserCreate(
        email="test3@example.com",
        password="testpassword",
        full_name="Test User",
        role=UserRole.STUDENT
    )
    await UserService.create_user(db, user_in)
    
    # Login
    login_response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test3@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "test3@example.com"
    assert user_data["full_name"] == "Test User"