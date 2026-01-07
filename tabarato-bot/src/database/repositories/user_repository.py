"""
Repository for user operations.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.models import User
from src.utils.logger import get_logger

logger = get_logger(__name__)


class UserRepository:
    """
    Repository for User database operations.
    """
    
    @staticmethod
    def get_or_create(
        session: Session,
        telegram_id: str,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """
        Get existing user or create new one.
        
        Args:
            session: Database session
            telegram_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            User: User object
        """
        # Try to find existing user
        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()
        
        if user:
            # Update last seen
            user.last_seen = datetime.utcnow()
            
            # Update user info if changed
            if username and user.username != username:
                user.username = username
            if first_name and user.first_name != first_name:
                user.first_name = first_name
            if last_name and user.last_name != last_name:
                user.last_name = last_name
            
            session.commit()
            logger.debug(f"Updated existing user: {telegram_id}")
        else:
            # Create new user
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
            session.commit()
            logger.info(f"Created new user: {telegram_id}")
        
        return user
    
    @staticmethod
    def get_by_telegram_id(session: Session, telegram_id: str) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            session: Database session
            telegram_id: Telegram user ID
            
        Returns:
            Optional[User]: User or None
        """
        return session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()
    
    @staticmethod
    def get_active_users_count(session: Session) -> int:
        """
        Get count of active users.
        
        Args:
            session: Database session
            
        Returns:
            int: Number of active users
        """
        return session.query(User).filter(
            User.is_active == True
        ).count()
    
    @staticmethod
    def deactivate_user(session: Session, telegram_id: str) -> bool:
        """
        Deactivate a user.
        
        Args:
            session: Database session
            telegram_id: Telegram user ID
            
        Returns:
            bool: True if user was deactivated
        """
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        
        if user:
            user.is_active = False
            session.commit()
            logger.info(f"Deactivated user: {telegram_id}")
            return True
        
        return False
