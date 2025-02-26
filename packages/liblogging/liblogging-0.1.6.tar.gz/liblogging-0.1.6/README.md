# liblogging

Utilities for logging and sending logs.

# Usage

```python
from liblogging.logger import logger

# Log a simple message
logger.info("This is an info message")

# Log a message with context
logger.track_start("Starting process", message_type="process_start")
logger.track_end("Ending process", message_type="process_end")

# Log a request
@log_request("user_id", "session_id")
def process_request(user_id, session_id):
    logger.info("Processing request")

process_request(user_id=123, session_id="abc")
```

# Tips

1. If using Kafka to send messages, please use `kafka-python==2.0.2`.