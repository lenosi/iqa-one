fmt_basic = '[%(asctime)s] [%(levelname)s] %(name)s :: %(message)s'

fmt_console = '[%(asctime)s] [%(levelname)s] %(name)s :: %(message)s'
fmt_console_color = '[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] %(name)s :: %(message)s'
fmt_console_enhanced = '[%(asctime)s] [%(levelname)-8s] %(name)s :: %(message)s'
fmt_console_enhanced_color = '[%(asctime)s] [%(log_color)s%(levelname)-8s%(reset)s] %(name)s :: %(message)s'

fmt_file_test = fmt_basic
fmt_file_debug = '[%(asctime)s] [%(levelname)s] %(name)s::%(funcName)s()[%(lineno)s] :: %(message)s'
fmt_file_trace = '[%(asctime)s] [%(levelname)s] %(name)s::%(funcName)s()[%(lineno)s] :: %(message)s'
fmt_file_doc = '%(name)s: %(message)s'

datefmt_iso = '%Y-%m-%d %H:%M:%S,'
datefmt_time = '%H:%M:%S'
