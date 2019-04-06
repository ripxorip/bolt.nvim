# ============================================================================
# FILE: __init__.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

import neovim
import vim_tc_explorer.logger
from vim_tc_explorer.vim_tc_explorer import vim_tc_explorer


@neovim.plugin
class VimTcExplorerHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim
        # Enable logging
        logger.init_log(True)
        self.TcExplorer = vim_tc_explorer(nvim)
        logger.log('Plugin Initialized')

    @neovim.command("Bolt", range='', nargs='*', sync=True)
    def tc_explore(self, args, range):
        self.TcExplorer.tc_explore(args, range)
        logger.log('Explorer Spawned')

    @neovim.command("BoltCwd", range='', nargs='*', sync=True)
    def tc_explore_cwd(self, args, range):
        self.TcExplorer.tc_explore_cwd(args, range)

    @neovim.command("Boltd", range='', nargs='*', sync=True)
    def tc_explore_dual(self, args, range):
        self.TcExplorer.tc_explore_dual(args, range)

    @neovim.command("BoltExpEnter", range='', nargs='*', sync=True)
    def tc_enter(self, args, range):
        self.TcExplorer.tc_enter(args, range)

    @neovim.command("BoltExpUp", range='', nargs='*', sync=True)
    def tc_up(self, args, range):
        self.TcExplorer.tc_up(args, range)

    @neovim.command("BoltExpDown", range='', nargs='*', sync=True)
    def tc_down(self, args, range):
        self.TcExplorer.tc_down(args, range)

    @neovim.command("BoltPgUp", range='', nargs='*', sync=True)
    def pg_up(self, args, range):
        self.TcExplorer.pg_up(args, range)

    @neovim.command("BoltPgDown", range='', nargs='*', sync=True)
    def pg_down(self, args, range):
        self.TcExplorer.pg_down(args, range)

    @neovim.command("BoltExpClose", range='', nargs='*', sync=True)
    def tc_close(self, args, range):
        self.TcExplorer.tc_close(args, range)

    @neovim.command("BoltExpTab", range='', nargs='*', sync=True)
    def tc_tab(self, args, range):
        self.TcExplorer.tc_tab(args, range)

    @neovim.command("BoltSetCwd", range='', nargs='*', sync=True)
    def tc_set_cwd(self, args, range):
        self.TcExplorer.tc_set_cwd(args, range)

    @neovim.command("BoltMove", range='', nargs='*', sync=True)
    def bolt_move(self, args, range):
        self.TcExplorer.move(args, range)

    @neovim.command("BoltRename", range='', nargs='*', sync=True)
    def bolt_rename(self, args, range):
        self.TcExplorer.rename(args, range)

    @neovim.command("BoltCopy", range='', nargs='*', sync=True)
    def bolt_copy(self, args, range):
        self.TcExplorer.copy(args, range)

    @neovim.command("BoltPaste", range='', nargs='*', sync=True)
    def bolt_paste(self, args, range):
        self.TcExplorer.paste(args, range)

    @neovim.command("BoltMkdir", range='', nargs='*', sync=True)
    def bolt_mkdir(self, args, range):
        self.TcExplorer.mkdir(args, range)

    @neovim.command("BoltCreateFile", range='', nargs='*', sync=True)
    def bolt_createFile(self, args, range):
        self.TcExplorer.createFile(args, range)

    @neovim.command("BoltDelete", range='', nargs='*', sync=True)
    def bolt_delete(self, args, range):
        self.TcExplorer.delete(args, range)

    @neovim.command("BoltToggleMark", range='', nargs='*', sync=True)
    def bolt_toggle_mark(self, args, range):
        self.TcExplorer.toggleMark(args, range)

    @neovim.command("BoltDisplayLog", range='', nargs='*', sync=True)
    def bolt_display_log(self, args, range):
        logger.display(self.nvim)

    @neovim.command("BoltGitStatus", range='', nargs='*', sync=True)
    def bolt_git_status(self, args, range):
        self.TcExplorer.gitStatus(args, range)

    @neovim.command("BoltSearch", range='', nargs='*', sync=True)
    def tc_search(self, args, range):
        self.TcExplorer.tc_search(args, range)

    @neovim.command("BoltFind", range='', nargs='*', sync=True)
    def tc_find(self, args, range):
        self.TcExplorer.tc_find(args, range)

    @neovim.command("BoltGrep", range='', nargs='*', sync=True)
    def tc_grep(self, args, range):
        self.TcExplorer.tc_grep(args, range)

    @neovim.command("BoltAbortFilter", range='', nargs='*', sync=True)
    def tc_abort_filter(self, args, range):
        self.TcExplorer.abortFilter(args, range)

    @neovim.command("BoltSearchToggle", range='', nargs='*', sync=True)
    def tc_search_toggle(self, args, range):
        self.TcExplorer.tc_search_toggle(args, range)

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def insert_changed(self):
        self.TcExplorer.handle_input()
