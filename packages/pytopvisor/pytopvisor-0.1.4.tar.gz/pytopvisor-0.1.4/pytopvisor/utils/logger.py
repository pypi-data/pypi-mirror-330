import logging
from pathlib import Path


class Logger:
    _instance = None

    def __new__(cls, log_file="app.log"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger(log_file)
        return cls._instance

    def _setup_logger(self, log_file):
        """
        Logger setup.
        """
        self.logger = logging.getLogger("TopvisorLogger")
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        logs_dir = Path(__file__).resolve().parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)

        # Log format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File logging
        api_error_handler = logging.FileHandler(
            logs_dir / "api_errors.log", encoding="utf-8"
        )
        api_error_handler.setLevel(logging.ERROR)
        api_error_handler.setFormatter(formatter)
        self.logger.addHandler(api_error_handler)

        # Console logging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Returns the logger instance.
        """
        return self.logger


logger = Logger().get_logger()

