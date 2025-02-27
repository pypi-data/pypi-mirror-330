import logging

def setup_logging():
    """Configures logging for API interactions."""
    logging.basicConfig(
        filename="sjm_api.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("SjmAPI")

