from .adapters.data_adapter import get_db_adapter

async def get_repository():
    """
    Dependency function to get the appropriate repository based on configuration.
    
    This function is used as a dependency in FastAPI route handlers to provide
    a dynamically selected repository instance.
    
    Yields:
        BaseRepository: A repository instance for the configured database type
    """
    db_adapter = get_db_adapter()
    async with db_adapter.get_repository() as repo:
        yield repo
