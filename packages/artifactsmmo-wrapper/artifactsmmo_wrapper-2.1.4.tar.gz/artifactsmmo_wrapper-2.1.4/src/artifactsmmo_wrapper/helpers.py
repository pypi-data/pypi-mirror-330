from .database import cache_db_cursor, cache_db
import time
from datetime import timezone, datetime
from threading import Lock
from functools import wraps

# --- Helpers ---
def _re_cache(api, table):
    print(table)
    
    # Use parameterized query to avoid SQL injection
    cache_db_cursor.execute("SELECT v FROM cache_table WHERE k = ?", (table,))
    version = cache_db_cursor.fetchone()

    app_version = api._get_version()

    try:
        if version:
            if app_version != version[0]:
                cache_db_cursor.execute("INSERT or REPLACE INTO cache_table (k, v) VALUES (?, ?)", (table, app_version))
                cache_db.commit()
                return True

        else:  # No record exists
            cache_db_cursor.execute("INSERT or REPLACE INTO cache_table (k, v) VALUES (?, ?)", (table, app_version))
            cache_db.commit()
            return True

        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

class CooldownManager:
    """
    A class to manage cooldowns for different operations using an expiration timestamp.
    """
    def __init__(self):
        self.lock = Lock()
        self.cooldown_expiration_time = None
        self.logger = None

    def is_on_cooldown(self) -> bool:
        """Check if currently on cooldown based on expiration time."""
        with self.lock:
            if self.cooldown_expiration_time is None:
                return False  # No cooldown set
            # Check if current time is before the expiration time
            return datetime.now(timezone.utc) < self.cooldown_expiration_time

    def set_cooldown_from_expiration(self, expiration_time_str: str) -> None:
        """Set cooldown based on an ISO 8601 expiration time string."""
        with self.lock:
            # Parse the expiration time string
            self.cooldown_expiration_time = datetime.fromisoformat(expiration_time_str.replace("Z", "+00:00"))

    def wait_for_cooldown(self, logger=None, char=None) -> None:
        """Wait until the cooldown expires."""
        if self.is_on_cooldown():
            remaining = (self.cooldown_expiration_time - datetime.now(timezone.utc)).total_seconds()
            if logger:
                if char:
                    logger.debug(f"Waiting for cooldown... ({remaining:.1f} seconds)", extra={"char": char.name})
                else:
                    logger.debug(f"Waiting for cooldown... ({remaining:.1f} seconds)", extra={"char": "Unknown"})
            while self.is_on_cooldown():
                remaining = (self.cooldown_expiration_time - datetime.now(timezone.utc)).total_seconds()
                time.sleep(min(remaining, 0.1))  # Sleep in small intervals

def with_cooldown(func):
    """
    Decorator to apply cooldown management to a method.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_cooldown_manager'):
            self._cooldown_manager = CooldownManager()
        
        # Before executing the action, check if the character is on cooldown
        source = kwargs.get('source')
        method = kwargs.get('method')
        
        # Skip cooldown for "get_character" source to allow fetching character data without waiting
        if source != "get_character":
            # Ensure cooldown manager is up to date with the character's cooldown expiration time
            if hasattr(self, 'char') and hasattr(self.char, 'cooldown_expiration'):
                self._cooldown_manager.set_cooldown_from_expiration(self.char.cooldown_expiration)

            # Wait for the cooldown to finish before calling the function
            self._cooldown_manager.wait_for_cooldown(logger=self.logger, char=self.char)

        # Now execute the function after confirming cooldown is finished
        result = func(self, *args, **kwargs)

        # Update the cooldown after the action if needed (depending on your business logic)
        if method not in ["GET", None, "None"]:
            # Set cooldown after the operation, if the character has a cooldown expiration
            if hasattr(self, 'char') and hasattr(self.char, 'cooldown_expiration'):
                self._cooldown_manager.set_cooldown_from_expiration(self.char.cooldown_expiration)
        
        return result
    return wrapper

