import logging
import os
import sys

LOGS_DIR = "logs"
LOG_FILE = "running_logs.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)


os.makedirs(LOGS_DIR, exist_ok=True)

if not os.path.exists(os.path.join(LOGS_DIR, ".gitkeep")):
    with open(os.path.join(LOGS_DIR, ".gitkeep"), "w") as f:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(module)s %(name)s -  %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler(sys.stdout)],
)

PROJECT_NAME = "cnn_classifier"

logger = logging.getLogger(PROJECT_NAME)
