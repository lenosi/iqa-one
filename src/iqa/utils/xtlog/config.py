import logging
import autologging
import sys

import iqa.utils.xtlog.config_handlers as config_handlers
import iqa.utils.xtlog.formats as formats
import iqa.utils.xtlog.levels as levels

levels.init()

#########################################
# Configuration

xtlog_config_default = {
    'console': {
        'filename': sys.stdout,
        'level': logging.DEBUG,
        'fmt': formats.fmt_console,
        'fmt_color': formats.fmt_console_color,
        'datefmt': formats.datefmt_time,
    },
    'test_file': {
        'filename': 'logs/%s.test.log',
        'level': logging.INFO,
        'fmt': formats.fmt_file_test,
        'datefmt': None,
    },
    'debug_file': {
        'filename': 'logs/%s.debug.log',
        'level': logging.DEBUG,
        'fmt': formats.fmt_file_debug,
        'datefmt': None,
    },
    'trace_file': {
        'filename': 'logs/%s.trace.log',
        'level': autologging.TRACE,
        'fmt': formats.fmt_file_trace,
        'datefmt': None,
    },

    'doc_file': {
        'filename': 'logs/%s.doc.log',
        'level': logging.TEST_DOC,
        'fmt': formats.fmt_file_doc,
        'datefmt': None,
    },
}

xtlog_cfg_function_map = {
    'console': config_handlers.config_console_logger,
    'test_file': config_handlers.config_test_file_logger,
    'debug_file': config_handlers.config_debug_file_logger,
    'trace_file': config_handlers.config_trace_file_logger,
    'doc_file': config_handlers.config_doc_file_logger,
}


def config_by_dictionary(cfg_data):
    """ function configure predefined handles by supplied dict
    @type cfg_data: dict
    @param cfg_data: configuration in format of dict, to initialize handlers
    @return: None
    """
    for handler in cfg_data.keys():
        args = cfg_data.get(handler)
        func = xtlog_cfg_function_map.get(handler)
        if func is not None:
            func(**args)


def config_all_default():
    """ Configure all defaults
    @return: None
    """
    config_by_dictionary(xtlog_config_default)


# setting root logger global log level to max, particular handlers will limit their log levels accordingly
logging.getLogger().setLevel(logging.DEBUG)
