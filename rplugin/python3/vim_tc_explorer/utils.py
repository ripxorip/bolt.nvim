# ============================================================================
# FILE: utils.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

nvim = None

def init_utils(_nvim):
    global nvim
    nvim = _nvim

def python_input(message = 'input'):
    global nvim
    nvim.command('call inputsave()')
    nvim.command("let user_input = input('" + message + ": ')")
    nvim.command('call inputrestore()')
    return nvim.eval('user_input')
