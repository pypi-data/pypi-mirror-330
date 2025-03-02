import random
import time
import logging


def setup_logger_behaviour(name: str) -> logging.Logger:
    root_handlers = logging.getLogger().handlers # gets root logger
    current_logger = logging.getLogger(name)   # gets current logger
    if not root_handlers:  # if root logger has no handlers then create streaming handeler only
        new_handler = logging.StreamHandler()
        new_handler.terminator = ""
        new_handler.setFormatter(logging.Formatter("%(message)s"))
        current_logger.addHandler(new_handler)
        current_logger.propagate = False
        current_logger.setLevel(logging.INFO)
        return current_logger

    # Remove  exixting Handlers from the current logger
    for handler in current_logger.handlers[:]:
        current_logger.removeHandler(handler)

    for handler_r in root_handlers:  # if root logger has handlers
        if type(handler_r) is logging.StreamHandler:  # if root logger has streaming handler
            new_handler = logging.StreamHandler() 
            new_handler.terminator = ""   # This will stop the printing in new line
            new_handler.setFormatter(logging.Formatter("%(message)s")) # This will set the format
            current_logger.addHandler(new_handler)
        elif type(handler_r) is logging.FileHandler:  # if root logger has file handler
            new_handler = logging.FileHandler( # create new file handler
                handler_r.baseFilename,        # with same filename and other properties
                handler_r.mode,
                handler_r.encoding,
                handler_r.delay,
                handler_r.errors,
            )
            new_handler.terminator = ""  # This will stop the printing in new line
            new_handler.setFormatter(logging.Formatter("%(message)s")) # This will set the format
            current_logger.addHandler(new_handler)
        else:
            continue
    current_logger.propagate = False  # Don't propagate to root logger
    return current_logger

# Configure the logger
logger =logging.getLogger(__name__)
class FakeStreamingDataGenerator:

    def stream_data(self):
        while True:
            data = random.randint(0, 100)
            yield data
            time.sleep(0.5)

# Example usage:
generator = FakeStreamingDataGenerator()
stream = generator.stream_data()

logger = setup_logger_behaviour(__name__) # call you set up function here
while True:
    chunk = next(stream)
    # Replacing print with logger
    logger.info(chunk)  # Best practice now