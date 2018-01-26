import neovim

@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command("Tc", range='', nargs='*')
    def testcommand(self, args, range):
        self.nvim.command('split TC_Explorer')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        # self.nvim.current.line = ('Hej %s' % args[1])

    @neovim.autocmd("TextChangedI", pattern='TC_Explorer', sync=True)
    def on_insert_enter(self):
        self.nvim.current.line = ("Hej")

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.nvim.command('echo "hello from DoItPython %s %s"')

