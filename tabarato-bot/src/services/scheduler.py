"""
Scheduler for automated tasks.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from typing import Optional

from src.services.search_service import get_search_service
from src.services.channel_service import get_channel_service
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TaskScheduler:
    """
    Scheduler for automated bot tasks.
    """
    
    def __init__(self):
        """Initialize task scheduler."""
        self.scheduler = AsyncIOScheduler()
        self._started = False
        
        logger.info("Task scheduler initialized")
    
    def start(self) -> None:
        """Start the scheduler."""
        if self._started:
            logger.warning("Scheduler already started")
            return
        
        # Schedule tasks
        self._schedule_tasks()
        
        # Start scheduler
        self.scheduler.start()
        self._started = True
        
        logger.info("Task scheduler started")
    
    def stop(self) -> None:
        """Stop the scheduler."""
        if not self._started:
            return
        
        self.scheduler.shutdown()
        self._started = False
        
        logger.info("Task scheduler stopped")
    
    def _schedule_tasks(self) -> None:
        """Schedule all automated tasks."""
        
        # Example: Search for deals every hour
        # Uncomment when ready to use
        """
        self.scheduler.add_job(
            self._search_and_post_deals,
            trigger=IntervalTrigger(hours=1),
            id='search_deals',
            name='Search and post deals',
            replace_existing=True
        )
        logger.info("Scheduled: Search deals every hour")
        """
        
        # Example: Cleanup old data daily
        """
        self.scheduler.add_job(
            self._cleanup_old_data,
            trigger=IntervalTrigger(days=1),
            id='cleanup',
            name='Cleanup old data',
            replace_existing=True
        )
        logger.info("Scheduled: Cleanup daily")
        """
        
        logger.info("All tasks scheduled")
    
    async def _search_and_post_deals(self) -> None:
        """
        Search for deals and post to channel.
        This is an example automated task.
        """
        try:
            logger.info("Running scheduled deal search...")
            
            # Popular search terms
            search_terms = [
                "notebook",
                "smartphone",
                "smart tv",
                "fone bluetooth",
                "mouse gamer"
            ]
            
            search_service = get_search_service()
            channel_service = get_channel_service()
            
            total_posted = 0
            
            for term in search_terms:
                # Search
                results = await search_service.search_all(term)
                
                if results.has_results:
                    # Post best deals
                    posted = await channel_service.post_best_deals(
                        results.products,
                        max_posts=1  # 1 per search term
                    )
                    total_posted += posted
            
            logger.info(f"Scheduled search complete: {total_posted} deals posted")
            
        except Exception as e:
            logger.error(f"Error in scheduled deal search: {e}", exc_info=True)
    
    async def _cleanup_old_data(self) -> None:
        """
        Cleanup old data from database.
        This is an example automated task.
        """
        try:
            logger.info("Running scheduled cleanup...")
            
            # Example: Delete searches older than 30 days
            # Implement cleanup logic here
            
            logger.info("Scheduled cleanup complete")
            
        except Exception as e:
            logger.error(f"Error in scheduled cleanup: {e}", exc_info=True)


# Global scheduler instance
_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """
    Get the global scheduler instance.
    
    Returns:
        TaskScheduler: Global scheduler
    """
    global _scheduler
    
    if _scheduler is None:
        _scheduler = TaskScheduler()
    
    return _scheduler
