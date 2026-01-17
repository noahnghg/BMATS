"""
User service to store and manage user profiles in database
"""
from typing import Optional, List
from core.database import User, add_user, get_user, get_all_users
from fastapi import HTTPException

class UserService:

    @staticmethod
    def create_user(skills: str, experience: str, education: str) -> User:
        """Create a new user profile with extracted resume data."""
        user = User(
            skills=skills,
            experience=experience,
            education=education
        )
        return add_user(user)
