import sqlite3
import os
from contextlib import contextmanager
from threading import Lock
from typing import Generator, Optional
import atexit

class DatabaseManager:
    """Thread-safe database connection manager with connection pooling."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection_lock = Lock()
        self._connection: Optional[sqlite3.Connection] = None
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
        
        # Register cleanup
        atexit.register(self.cleanup)

    def _init_db(self) -> None:
        """Initialize database and create necessary tables."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_table (
                    k TEXT PRIMARY KEY,
                    v TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection in a thread-safe way."""
        with self._connection_lock:
            if self._connection is None:
                self._connection = sqlite3.connect(self.db_path)
                self._connection.row_factory = sqlite3.Row
            
            try:
                yield self._connection
            except Exception as e:
                self._connection.rollback()
                raise e

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Get a database cursor in a thread-safe way."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    def cleanup(self) -> None:
        """Clean up database connections."""
        with self._connection_lock:
            if self._connection:
                self._connection.close()
                self._connection = None

# Initialize database manager
db_manager = DatabaseManager(os.path.join('db', 'artifacts.db'))
