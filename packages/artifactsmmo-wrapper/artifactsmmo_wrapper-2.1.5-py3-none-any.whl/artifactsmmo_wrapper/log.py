import logging

logger = logging.getLogger(__name__)

# Define the logging format you want to apply
formatter = logging.Formatter(
    fmt="\33[34m[%(levelname)s] %(asctime)s - %(char)s:\33[0m %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a handler (e.g., StreamHandler for console output) and set its format
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

