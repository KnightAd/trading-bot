from loguru import logger
from pathlib import Path

# Ensure a logs directory exists relative to this file
LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    LOG_DIR / "bot.log",
    rotation="5 MB",  # Rotate after 5 MB
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
)

# Export logger for other modules
__all__ = ["logger"]
