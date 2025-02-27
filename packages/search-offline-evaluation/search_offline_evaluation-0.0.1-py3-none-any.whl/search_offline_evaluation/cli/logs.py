import logging
import litellm
from search_offline_evaluation.utils.logging_config import setup_logging


def _deactivate_liteLLM_logs():
    litellm.suppress_debug_info = True
    logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)


def _setup_root_logger():
    logger = setup_logging()
    logger.setLevel(logging.WARNING)
    ch = logging.FileHandler("my_app.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(ch)


def cli_log_setup():
    _setup_root_logger()
    _deactivate_liteLLM_logs()
