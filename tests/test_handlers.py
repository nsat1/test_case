import unittest
from unittest.mock import patch, MagicMock

from io import StringIO
from logging import LogRecord, ERROR, INFO, WARNING, DEBUG, CRITICAL

from pytracelog.pytracelog_logging.handlers import StdoutHandler, StderrHandler, TracerHandler


class TestStdoutHandler(unittest.TestCase):
    """
    Класс для тестирования StdoutHandler
    """

    def test_error_record_filter_below_error(self):
        """
        Проверяем, что фильтр возвращает True для записей с уровнем ниже ERROR (INFO, WARNING, DEBUG).
        """
        record = LogRecord(name='test', level=INFO, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertTrue(StdoutHandler.error_record_filter(record))

        record = LogRecord(name='test', level=WARNING, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertTrue(StdoutHandler.error_record_filter(record))

        record = LogRecord(name='test', level=DEBUG, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertTrue(StdoutHandler.error_record_filter(record))

    def test_error_record_filter_at_or_above_error(self):
        """
        Проверяем, что фильтр возвращает False для записей с уровнем ERROR и выше (ERROR, CRITICAL).
        """
        record = LogRecord(name='test', level=ERROR, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertFalse(StdoutHandler.error_record_filter(record))

        record = LogRecord(name='test', level=CRITICAL, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertFalse(StdoutHandler.error_record_filter(record))

    @patch('sys.stdout', new_callable=StringIO)
    def test_emit_at_or_above_error(self, mock_stdout):
        """
        Проверяем, что записи с уровнем ERROR и выше (ERROR) не выводятся в stdout.
         * Используем мок для захвата вывода в stdout.
        """
        handler = StdoutHandler()
        record = LogRecord(name='test', level=ERROR, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        handler.emit(record)
        self.assertNotIn('test message', mock_stdout.getvalue())


class TestStderrHandler(unittest.TestCase):
    """
    Класс для тестирования StderrHandler
    """

    def test_error_record_filter_below_error(self):
        """
        Проверяем, что фильтр возвращает False для записей с уровнем ниже ERROR (INFO, WARNING, DEBUG).
        """
        record = LogRecord(name='test', level=INFO, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertFalse(StderrHandler.error_record_filter(record))

        record = LogRecord(name='test', level=WARNING, pathname='', lineno=0, msg='test message', args=(),
                           exc_info=None)
        self.assertFalse(StderrHandler.error_record_filter(record))

        record = LogRecord(name='test', level=DEBUG, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertFalse(StderrHandler.error_record_filter(record))

    def test_error_record_filter_at_or_above_error(self):
        """
        Проверяем, что фильтр возвращает True для записей с уровнем ERROR и выше (ERROR, CRITICAL).
        """
        record = LogRecord(name='test', level=ERROR, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        self.assertTrue(StderrHandler.error_record_filter(record))

        record = LogRecord(name='test', level=CRITICAL, pathname='', lineno=0, msg='test message', args=(),
                           exc_info=None)
        self.assertTrue(StderrHandler.error_record_filter(record))


class TestTracerHandler(unittest.TestCase):
    """
    Класс для тестирования TracerHandler
    """

    def test_get_record_attrs_remove_msg(self):
        """
        Проверяем, что метод get_record_attrs удаляет атрибут 'msg' при remove_msg=True.
        """
        record = LogRecord(name='test', level=INFO, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        attrs = TracerHandler.get_record_attrs(record)
        self.assertNotIn('msg', attrs)

    def test_get_record_attrs_keep_msg(self):
        """
        Проверяем, что метод get_record_attrs сохраняет атрибут 'msg' при remove_msg=False и переименовывает его в
        'original.message'.
        """
        record = LogRecord(name='test', level=INFO, pathname='', lineno=0, msg='test message', args=(), exc_info=None)
        attrs = TracerHandler.get_record_attrs(record, remove_msg=False)
        self.assertIn('original.message', attrs)
        self.assertEqual(attrs['original.message'], 'test message')


if __name__ == '__main__':
    unittest.main()
