import logging
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

class GameLogger:
    """Enhanced logging system with both console and file output."""
    
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Console handler with colored output
        console_formatter = logging.Formatter(
            fmt="\33[34m[%(levelname)s] %(asctime)s - %(char)s:\33[0m %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        
        # File handler with detailed output
        file_formatter = logging.Formatter(
            fmt="[%(levelname)s] %(asctime)s - %(char)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler = RotatingFileHandler(
            filename=f'logs/game_{datetime.now().strftime("%Y%m%d")}.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, msg: str, char: Optional[str] = "Unknown") -> None:
        self.logger.debug(msg, extra={"char": char})
    
    def info(self, msg: str, char: Optional[str] = "Unknown") -> None:
        self.logger.info(msg, extra={"char": char})
    
    def warning(self, msg: str, char: Optional[str] = "Unknown") -> None:
        self.logger.warning(msg, extra={"char": char})
    
    def error(self, msg: str, char: Optional[str] = "Unknown") -> None:
        self.logger.error(msg, extra={"char": char})
    
    def critical(self, msg: str, char: Optional[str] = "Unknown") -> None:
        self.logger.critical(msg, extra={"char": char})

# Initialize logger
logger = GameLogger().logger

