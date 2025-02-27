class SessionManagerRegistry:
    _sync_instance = None
    _async_instance = None

    @classmethod
    def get_sync_manager(cls):
        if cls._sync_instance is None:
            from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter

            cls._sync_instance = SessionManagerAdapter()
        return cls._sync_instance

    @classmethod
    def set_sync_manager(cls, manager):
        cls._sync_instance = manager

    @classmethod
    def get_async_manager(cls):
        if cls._async_instance is None:
            from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter

            cls._async_instance = AsyncSessionManagerAdapter()
        return cls._async_instance

    @classmethod
    def set_async_manager(cls, manager):
        cls._async_instance = manager

    @classmethod
    def reset(cls):
        """Reset the registry (useful for testing)"""
        cls._sync_instance = None
        cls._async_instance = None
