import logging

def configure_logger(log_file):
    # Set up the logger using basicConfig
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",  # Set filemode to "w" to overwrite the log file
        filename=log_file
    )

    # Get the logger
    logger = logging.getLogger(__name__)

    return logger

# Function to format the duration in seconds, minutes, or hours
def format_duration(duration):
    if duration < 60:
        return f"{duration:.2f} seconds"
    elif duration < 3600:
        return f"{duration / 60:.2f} minutes"
    else:
        return f"{duration / 3600:.2f} hours"