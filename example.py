import os
import logging
from pytracelog.base import PyTraceLog

os.environ['LOGSTASH_HOST'] = 'localhost'
os.environ['LOGSTASH_PORT'] = '6000'
os.environ['OTEL_EXPORTER_JAEGER_AGENT_HOST'] = 'localhost'

PyTraceLog.init_root_logger(level='DEBUG')
PyTraceLog.init_logstash_logger(level='DEBUG', message_type='python', index_name='python')
PyTraceLog.init_tracer(service='test_service')
PyTraceLog.init_tracer_logger(level='DEBUG')

logger = logging.getLogger(__name__)

def main():
    logger.info("INFO")
    logger.warning("WARNING")
    logger.error("ERROR")

if __name__ == "__main__":
    main()