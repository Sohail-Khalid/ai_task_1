import logging
import os

LOG_FILE = "development.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("logs", LOG_FILE)),
        logging.StreamHandler() 
    ]
)

logger = logging.getLogger("FastAPIApp")
