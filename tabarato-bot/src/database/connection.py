"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator

from src.database.models import Base
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """
    Database connection manager.
    """
    
    def __init__(self):
        """Initialize database connection."""
        self.engine = None
        self.SessionLocal = None
        self._initialized = False
    
    def initialize(self) -> None:
        """
        Initialize database engine and create tables.
        """
        if self._initialized:
            logger.warning("Database already initialized")
            return
        
        try:
            # Create engine
            self.engine = create_engine(
                Config.DATABASE_URL,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,  # Verify connections before using
                echo=False  # Set to True for SQL query logging
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            self._initialized = True
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            raise
    
    def get_session(self) -> Session:
        """
        Get a new database session.
        
        Returns:
            Session: SQLAlchemy session
        """
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope for database operations.
        
        Usage:
            with db.session_scope() as session:
                user = session.query(User).first()
        
        Yields:
            Session: Database session
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            session.close()
    
    def close(self) -> None:
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")
            self._initialized = False


# Global database instance
_database: Database = None


def get_database() -> Database:
    """
    Get the global database instance.
    
    Returns:
        Database: Global database instance
    """
    global _database
    
    if _database is None:
        _database = Database()
        _database.initialize()
    
    return _database


def init_database() -> None:
    """
    Initialize the database.
    Call this at application startup.
    """
    db = get_database()
    logger.info("Database ready")


def close_database() -> None:
    """
    Close database connections.
    Call this at application shutdown.
    """
    global _database
    
    if _database:
        _database.close()
        _database = None
