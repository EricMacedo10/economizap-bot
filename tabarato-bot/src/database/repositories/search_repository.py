"""
Repository for search operations.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from src.database.models import Search, ProductCache, User
from src.models.product import Product, SearchResult
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SearchRepository:
    """
    Repository for Search database operations.
    """
    
    @staticmethod
    def create_search(
        session: Session,
        user: User,
        search_result: SearchResult
    ) -> Search:
        """
        Create a new search record.
        
        Args:
            session: Database session
            user: User who performed the search
            search_result: Search result to save
            
        Returns:
            Search: Created search record
        """
        # Get best price info
        best_product = search_result.best_price
        best_price = best_product.final_price if best_product else None
        best_marketplace = best_product.marketplace if best_product else None
        
        # Create search record
        search = Search(
            user_id=user.id,
            query=search_result.query,
            results_count=search_result.total_results,
            best_price=best_price,
            best_marketplace=best_marketplace,
            search_time=search_result.search_time
        )
        
        session.add(search)
        session.flush()  # Get search.id
        
        # Save products
        for product in search_result.products:
            product_cache = ProductCache(
                search_id=search.id,
                external_id=product.id,
                name=product.name,
                price=product.price,
                original_price=product.original_price,
                marketplace=product.marketplace,
                url=product.url,
                image_url=product.image_url,
                coupon_code=product.coupon_code,
                discount_percentage=product.discount_percentage
            )
            session.add(product_cache)
        
        session.commit()
        logger.info(f"Saved search: {search_result.query} with {len(search_result.products)} products")
        
        return search
    
    @staticmethod
    def get_user_searches(
        session: Session,
        user: User,
        limit: int = 10
    ) -> List[Search]:
        """
        Get recent searches for a user.
        
        Args:
            session: Database session
            user: User
            limit: Maximum number of searches to return
            
        Returns:
            List[Search]: Recent searches
        """
        return session.query(Search).filter(
            Search.user_id == user.id
        ).order_by(
            desc(Search.created_at)
        ).limit(limit).all()
    
    @staticmethod
    def get_popular_queries(
        session: Session,
        days: int = 7,
        limit: int = 10
    ) -> List[tuple]:
        """
        Get most popular search queries.
        
        Args:
            session: Database session
            days: Number of days to look back
            limit: Maximum number of queries to return
            
        Returns:
            List[tuple]: List of (query, count) tuples
        """
        since = datetime.utcnow() - timedelta(days=days)
        
        results = session.query(
            Search.query,
            func.count(Search.id).label('count')
        ).filter(
            Search.created_at >= since
        ).group_by(
            Search.query
        ).order_by(
            desc('count')
        ).limit(limit).all()
        
        return results
    
    @staticmethod
    def get_total_searches(session: Session) -> int:
        """
        Get total number of searches.
        
        Args:
            session: Database session
            
        Returns:
            int: Total searches
        """
        return session.query(Search).count()
    
    @staticmethod
    def get_searches_by_date(
        session: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[Search]:
        """
        Get searches within a date range.
        
        Args:
            session: Database session
            start_date: Start date
            end_date: End date
            
        Returns:
            List[Search]: Searches in date range
        """
        return session.query(Search).filter(
            Search.created_at >= start_date,
            Search.created_at <= end_date
        ).all()
