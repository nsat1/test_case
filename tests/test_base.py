from os import environ
from logging import root, WARNING

import unittest
from unittest.mock import patch

from pytracelog.base import PyTraceLog, LOGSTASH_HOST, LOGSTASH_PORT, OTEL_EXPORTER_JAEGER_AGENT_HOST
from pytracelog.logging.handlers import StdoutHandler, StderrHandler, TracerHandler

from logstash_async.handler import AsynchronousLogstashHandler


class TestPyTraceLog(unittest.TestCase):
    """
    Класс для тестирования подсистем логирования и трассировки.
    """

    def setUp(self):
        #  Сброс настроек перед каждым тестом.
        PyTraceLog.reset()

    def test_init_root_logger(self):
        """
        Тест на корректную инициализацию корневого логера и добавления обработчиков
        для вывода логов в стандартные потоки.
         * Инициализируем корневой логер;
         * Проверяем, что список _handlers содержит 2 обработчика.
        """
        PyTraceLog.init_root_logger(level=WARNING)
        self.assertEqual(len(root.handlers), 2)
        self.assertTrue(all(isinstance(h, (StdoutHandler, StderrHandler)) for h in root.handlers))

    def test_extend_log_record(self):
        """
        Проверяем, что метод корректно добавляет пользовательские атрибуты к записям логов.
         * Вызываем метод с пользовательским атрибутом test_attr и значением "test_value".
         * Создаем тестовую запись лога.
         * Проверяем, что атрибут test_attr в записи лога равен "test_value".
        """
        PyTraceLog.extend_log_record(test_attr="test_value")
        record = root.makeRecord("test", WARNING, "test", 0, "test", (), None)
        self.assertEqual(record.test_attr, "test_value")

    @patch.dict(environ, {LOGSTASH_HOST: "localhost", LOGSTASH_PORT: "5959"})
    def test_init_logstash_logger(self):
        """
        Проверяем, что метод init_logstash_logger корректно добавляет обработчик AsynchronousLogstashHandler,
        если переменная окружения LOGSTASH_HOST задана.
         * Используем моки для переменных окружения, чтобы задать LOGSTASH_HOST и LOGSTASH_PORT.
         * Вызываем метод init_logstash_logger.
         * Проверяем, что количество обработчиков в корневом логере равно 1.
         * Проверяем, что обработчик является экземпляром класса AsynchronousLogstashHandler.
        """
        PyTraceLog.init_logstash_logger()
        self.assertEqual(len(root.handlers), 1)
        self.assertIsInstance(root.handlers[0], AsynchronousLogstashHandler)

    @patch.dict(environ, {OTEL_EXPORTER_JAEGER_AGENT_HOST: "localhost"})
    def test_init_tracer(self):
        """
        Проверяем, что метод корректно инициализирует трассировку, если переменная окружения
        OTEL_EXPORTER_JAEGER_AGENT_HOST задана.
         * Используем моки для переменных окружения, чтобы задать OTEL_EXPORTER_JAEGER_AGENT_HOST.
         * Вызываем метод init_tracer с именем сервиса "test_service".
         * Проверяем, что трассировка инициализирована корректно.
        """
        PyTraceLog.init_tracer(service="test_service")

    def test_init_tracer_logger(self):
        """
        Проверяем, что метод корректно добавляет обработчик TracerHandler к корневому логеру.
         * Вызываем метод init_tracer_logger.
         * Проверяем, что количество обработчиков в корневом логгере равно 1.
         * Проверяем, что обработчик является экземпляром класса TracerHandler.
        """
        PyTraceLog.init_tracer_logger()
        self.assertEqual(len(root.handlers), 1)
        self.assertIsInstance(root.handlers[0], TracerHandler)

    def test_reset(self):
        """
        Проверяем, что метод корректно сбрасывает все настройки.
         * Вызываем метод init_root_logger для инициализации обработчиков.
         * Вызываем метод reset.
         * Проверяем, что уровень логирования корневого логера равен WARNING.
         * Проверяем, что количество обработчиков в корневом логере равно 0.
         * Проверяем, что фабрика записей логов сброшена
         * Проверяем, что список обработчиков пуст.
        """
        PyTraceLog.init_root_logger(level=WARNING)
        PyTraceLog.reset()
        self.assertEqual(root.level, WARNING)
        self.assertEqual(len(root.handlers), 0)
        self.assertIsNone(PyTraceLog._old_factory)
        self.assertEqual(PyTraceLog._handlers, [])


if __name__ == '__main__':
    unittest.main()
