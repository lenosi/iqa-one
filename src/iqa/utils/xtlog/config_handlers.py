import logging
import autologging
import sys

import iqa.utils.xtlog.config_utils as config_utils
import iqa.utils.xtlog.formats as formats
import iqa.utils.xtlog.filters as filters


# defining selected handlers


def config_console_logger(filename=None, level=None, fmt=None, fmt_color=None, datefmt=None):
    """ configure console logger, if colorlog is installed it will use colorlog
    @param filename: stream to log into, default sys.stdout
    @param level: console log level
    @param fmt: console log format
    @param fmt_color: console color log format (only with colorlog)
    @param datefmt: formatter date format, default like ISO8601
    @return: None
    """
    import_error_msg = []
    # Windows compatibility section for colorama
    try:
        import colorama
        colorama.init()
    except ImportError:
        try:
            import colorlog
        except ImportError:
            import platform
            if platform.system() == "Windows":
                import_error_msg.append("Colorlog without colorama used, expect escape codes, please install colorama")

    filename = config_utils.substitute_main_filename(filename) or sys.stdout
    level = level or logging.DEBUG
    fmt = fmt or formats.fmt_console
    fmt_color = fmt_color or formats.fmt_console_color
    datefmt = datefmt or formats.datefmt_time

    # console handler
    # console_handler = logging.StreamHandler(stream=filename)  # Python 2.7
    console_handler = logging.StreamHandler(sys.stdout)  # Python 2.6
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(fmt, datefmt=datefmt)

    try:
        import colorlog
        console_formatter = colorlog.ColoredFormatter(
            fmt_color,
            log_colors={
                'CRITICAL': 'black,bg_red',
                'ERROR': 'red',
                'WARNING': 'yellow',
                'SKIP': 'blue',
                'FAIL': 'bold_red',
                'PASS': 'bold_green',
                'INFO': 'reset',
                'DOC': 'purple',
                'DEBUG': 'cyan',
            },
            datefmt=datefmt,
        )
    except ImportError:
        import_error_msg.append("cannot initialize colorlog, using boring streamhandler")
        pass
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)
    # log all above error messages
    if import_error_msg:
        for log_err in import_error_msg:
            logging.info(log_err)


def config_test_file_logger(filename=None, level=None, fmt=None, datefmt=None):
    """ Test file logger config
    @param filename: filename to log Test related messages into
    @param level: test log file level
    @param fmt: test log file format
    @param datefmt: formatter date format, default like ISO8601
    @return: None
    """
    filename = config_utils.substitute_main_filename(filename or '%s.test.log')
    level = level or logging.INFO
    fmt = fmt or formats.fmt_file_test

    config_utils.prepare_file_path(filename)
    test_file_handler = logging.FileHandler(filename, mode='w')
    test_file_handler.setLevel(level)
    test_file_formatter = logging.Formatter(fmt, datefmt=datefmt)
    test_file_handler.setFormatter(test_file_formatter)
    logging.getLogger().addHandler(test_file_handler)


def config_debug_file_logger(filename=None, level=None, fmt=None, datefmt=None):
    """ configure debug file logger, to log all debug related messages
    @param filename: debug log file name
    @param level: debug log file level
    @param fmt: debug log file format
    @param datefmt: formatter date format, default like ISO8601
    @return: None
    """
    filename = config_utils.substitute_main_filename(filename or '%s.debug.log')
    level = level or logging.DEBUG
    fmt = fmt or formats.fmt_file_debug

    config_utils.prepare_file_path(filename)
    debug_file_handler = logging.FileHandler(filename, mode='w')
    debug_file_handler.setLevel(level)
    debug_file_formatter = logging.Formatter(fmt, datefmt=datefmt)
    debug_file_handler.setFormatter(debug_file_formatter)
    logging.getLogger().addHandler(debug_file_handler)


def config_trace_file_logger(filename=None, level=None, fmt=None, datefmt=None):
    """ configure debug file logger, to log all debug related messages
    @param filename: debug log file name
    @param level: debug log file level
    @param fmt: debug log file format
    @param datefmt: formatter date format, default like ISO8601
    @return: None
    """
    filename = config_utils.substitute_main_filename(filename or '%s.trace.log')
    level = level or autologging.TRACE
    fmt = fmt or formats.fmt_file_trace

    config_utils.prepare_file_path(filename)
    debug_file_handler = logging.FileHandler(filename, mode='w')
    debug_file_handler.setLevel(level)
    debug_file_formatter = logging.Formatter(fmt, datefmt=datefmt)
    debug_file_handler.setFormatter(debug_file_formatter)
    logging.getLogger().addHandler(debug_file_handler)


def config_doc_file_logger(filename=None, level=None, fmt=None, datefmt=None):
    """ configure test doc file logger, to log all test documentation
    @param filename: test doc file log name
    @param level: test doc file level for filtering only those messages
    @param fmt: test doc file format
    @param datefmt: formatter date format, default like ISO8601
    @return: None
    """
    filename = config_utils.substitute_main_filename(filename or '%s.doc.log')
    level = level or logging.TEST_DOC
    fmt = fmt or formats.fmt_file_doc

    # doc file logger
    config_utils.prepare_file_path(filename)
    doc_file_handler = logging.FileHandler(filename, mode='w')
    doc_file_handler.setLevel(level)
    doc_file_handler.addFilter(filters.EqualsLevelFilter(level))
    doc_file_formatter = logging.Formatter(fmt, datefmt=datefmt)
    doc_file_handler.setFormatter(doc_file_formatter)
    logging.getLogger().addHandler(doc_file_handler)
