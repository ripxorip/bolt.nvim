# ============================================================================
# FILE: logger.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import neovim
import datetime
import time

# Global variable that enables logging
logparam = False
logstr = []

def entry_with_ts(data):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st + " |  " + data

def init_log(_log):
    global logparam
    global logstr
    logstr.append('=== Bolt Log ===')
    logparam= _log

def display(nvim):
    global logstr
    nvim.command('e bolt_log')
    nvim.command('setlocal buftype=nofile')
    nvim.command('setlocal filetype=bolt_log')
    nvim.current.buffer.append(logstr)

def log(data):
    global logparam
    global logstr
    if logparam:
        logstr.append(entry_with_ts(data.strip('\n')))

def log_list(data):
    global logparam
    global logstr
    resStr = ''
    for it in data:
        resStr += str(it) + ' | '
    if logparam:
        logstr.append(entry_with_ts(resStr))
