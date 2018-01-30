# ============================================================================
# FILE: __init__.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

import neovim
from vim_tc_explorer.vim_tc_explorer import vim_tc_explorer


@neovim.plugin
class VimTcExplorerHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.TcExplorer = vim_tc_explorer(nvim, log=False)

    @neovim.command("Tc", range='', nargs='*', sync=True)
    def tc_explore(self, args, range):
        self.TcExplorer.tc_explore(args, range)

    @neovim.command("Tcd", range='', nargs='*', sync=True)
    def tc_explore_dual(self, args, range):
        self.TcExplorer.tc_explore_dual(args, range)

    @neovim.command("TcExpEnter", range='', nargs='*', sync=True)
    def tc_enter(self, args, range):
        self.TcExplorer.tc_enter(args, range)

    @neovim.command("TcExpUp", range='', nargs='*', sync=True)
    def tc_up(self, args, range):
        self.TcExplorer.tc_up(args, range)

    @neovim.command("TcExpDown", range='', nargs='*', sync=True)
    def tc_down(self, args, range):
        self.TcExplorer.tc_down(args, range)

    @neovim.command("TcExpClose", range='', nargs='*', sync=True)
    def tc_close(self, args, range):
        self.TcExplorer.tc_close(args, range)

    @neovim.command("TcExpTab", range='', nargs='*', sync=True)
    def tc_tab(self, args, range):
        self.TcExplorer.tc_tab(args, range)

    @neovim.command("TcSetCwd", range='', nargs='*', sync=True)
    def tc_set_cwd(self, args, range):
        self.TcExplorer.tc_set_cwd(args, range)

    @neovim.command("TcSearch", range='', nargs='*', sync=True)
    def tc_search(self, args, range):
        self.TcExplorer.tc_search(args, range)

    @neovim.command("TcSearchToggle", range='', nargs='*', sync=True)
    def tc_search_toggle(self, args, range):
        self.TcExplorer.tc_search_toggle(args, range)

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def insert_changed(self):
        self.TcExplorer.handle_input()
