# Seismos Python Package

### Structlog
Structlog is a powerful logging library for structured, context-aware logging.
More details can be found in the [structlog](https://www.structlog.org/en/stable/).

#### Example, basic structlog configuration

instead of `logger = logging.getLogger(__name__)` it is `logger = structlog.get_logger(__name__)`

```python
    from seismos_package.logging import LoggingConfigurator
    from seismos_package.config import SeismosConfig
    import structlog

    config = SeismosConfig()

    LoggingConfigurator(
        service_name=config.APP_NAME,
        log_level='INFO',
        setup_logging_dict=True
    ).configure_structlog(
        formatter='plain_console',
        formatter_std_lib='plain_console'
    )

    logger = structlog.get_logger(__name__)
    logger.debug("This is a DEBUG log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.info("This is an INFO log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.warning("This is a WARNING log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.error("This is an ERROR log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.critical("This is a CRITICAL log message", key_1="value_1", key_2="value_2", key_n="value_n")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("An EXCEPTION log with stack trace occurred", key_1="value_1", key_2="value_2")


```
![basic example](images/plain_console_logger.png)


In production, you should aim for structured, machine-readable logs that can be easily ingested by log aggregation and monitoring tools like ELK (Elasticsearch, Logstash, Kibana), Datadog, or Prometheus:

```python
    from seismos_package.logging import LoggingConfigurator
    from seismos_package.config import SeismosConfig
    import structlog

    config = SeismosConfig()

    LoggingConfigurator(
        service_name=config.APP_NAME,
        log_level='INFO',
        setup_logging_dict=True
    ).configure_structlog(
        formatter='json_formatter',
        formatter_std_lib='json_formatter'
    )

    logger = structlog.get_logger(__name__)
    logger.debug("This is a DEBUG log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.info("This is an INFO log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.warning("This is a WARNING log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.error("This is an ERROR log message", key_1="value_1", key_2="value_2", key_n="value_n")
    logger.critical("This is a CRITICAL log message", key_1="value_1", key_2="value_2", key_n="value_n")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("An EXCEPTION log with stack trace occurred", key_1="value_1", key_2="value_2")
```

![logger with different keys](images/json_logger.png)


#### Using Middleware for Automatic Logging Context:

The middleware adds request_id, IP, and user_id to every log during a request/response cycle.
This middleware module provides logging context management for both Flask and FastAPI applications using structlog.

Flask Middleware (add_request_context_flask): Captures essential request data such as the request ID, method, and path, binding them to the structlog context for better traceability during the request lifecycle.

FastAPI Middleware (add_request_context_fastapi): Captures similar request metadata, ensuring a request ID is present, generating one if absent.
It binds the request context to structlog and clears it after the request completes.

Class-Based Middleware (FastAPIRequestContextMiddleware): A reusable FastAPI middleware class that integrates with the BaseHTTPMiddleware and delegates the logging setup to the add_request_context_fastapi function.

This setup ensures structured, consistent logging across both frameworks, improving traceability and debugging in distributed systems.


This guide explains how to set up and use structlog for structured logging in a Flask application. The goal is to have a consistent and centralized logging setup that can be reused across the application.
The logger is initialized once in the main application file (e.g., app.py).

```python
    import sys
    import uuid
    from flask import Flask, request
    from seismos_package.logging import LoggingConfigurator
    from seismos_package.logging.middlewares import add_request_context_flask
    from seismos_package.config import SeismosConfig
    import structlog

    config = SeismosConfig()

    LoggingConfigurator(
        service_name=config.APP_NAME,
        log_level="INFO",
        setup_logging_dict=True,
    ).configure_structlog(formatter='json_formatter', formatter_std_lib='json_formatter')

    logger = structlog.get_logger(__name__)

    app = Flask(__name__)

    @app.before_request
    def set_logging_context():
        """Bind context for each request using the middleware."""
        add_request_context_flask()
        logger.info("Context set for request")

    with app.test_client() as client:
        dynamic_request_id = str(uuid.uuid4())
        client.get("/", headers={"X-User-Name": "John Doe", "X-Request-ID": dynamic_request_id})
        logger.info("Test client request sent", request_id=dynamic_request_id)

```

![logger with context flask](images/flask_logger_with_context.png)

You can use the same logger instance across different modules by importing structlog directly.
Example (services.py):


```python
    import structlog

    logger = structlog.get_logger(__name__)
    logger.info("Processing data started", data_size=100)
```
Key Points:

- Centralized Configuration: The logger is initialized once in app.py.
- Consistent Usage: structlog.get_logger(__name__) is imported and used across all files.
- Context Management: Context is managed using structlog.contextvars.bind_contextvars().
- Structured Logging: The JSON formatter ensures logs are machine-readable.

FastAPI:

```python
    import uuid
    from fastapi import FastAPI, Request
    from seismos_package.logging.middlewares import FastAPIRequestContextMiddleware
    import structlog

    config = SeismosConfig()

    LoggingConfigurator(
        service_name=config.APP_NAME,
        log_level="INFO",
        setup_logging_dict=True,
    ).configure_structlog(formatter='json_formatter', formatter_std_lib='json_formatter')

    logger = structlog.get_logger(__name__)
    app = FastAPI()
    app.add_middleware(FastAPIRequestContextMiddleware)

```
![logger with context fastapi](images/fastapi_logger_with_context.png)


Automatic injection of:
-   user_id
-   IP
-   request_id
-  request_method


This a console view, in prod it will be json (using python json logging to have standard logging and structlog logging as close as possible)


### Why Use a Structured Logger?
-   Standard logging often outputs plain text logs, which can be challenging for log aggregation tools like EFK Stack or Grafana Loki to process effectively.
-   Structured logging outputs data in a machine-readable format (e.g., JSON), making it easier for log analysis tools to filter and process logs efficiently.
-   With structured logging, developers can filter logs by fields such as request_id, user_id, and transaction_id for better traceability across distributed systems.
-   The primary goal is to simplify debugging, enable better error tracking, and improve observability with enhanced log analysis capabilities.
-   Structured logs are designed to be consumed primarily by machines for monitoring and analytics, while still being readable for developers when needed.
-   This package leverages structlog, a library that enhances Python's standard logging by providing better context management and a flexible structure for log messages.


# Development of this project

Please install [poetry](https://python-poetry.org/docs/#installation) as this is the tool we use for releasing and development.

    poetry install && poetry run pytest -rs --cov=seismos_package -s

To run tests inside docker:

    poetry install --with dev && poetry run pytest -rs --cov=seismos_package

To run pre-commit:
    poetry run pre-commit run --all-files
