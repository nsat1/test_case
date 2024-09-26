from logging import getLogger
from pytracelog.base import  PyTraceLog
from opentelemetry import trace


PyTraceLog.init_root_logger(level='DEBUG')
PyTraceLog.init_logstash_logger(level='DEBUG')

PyTraceLog.init_tracer(service='my_service')

logger = getLogger(__name__)
tracer = trace.get_tracer(__name__)

def main():
    logger.info("**Тестовое сообщение**")

    with tracer.start_as_current_span("test_span") as span:
        logger.info("**Тест трассировка**")
        span.set_attribute("test_attribute", "test_value")

    logger.warning("**Тестовое сообщение уровня WARNING**")

if __name__ == "__main__":
    main()
