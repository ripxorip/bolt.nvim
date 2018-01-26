import neovim
import os

@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.currentInput = ''

    def draw(self):
        self.buffer[:] = ['==== TC explorer (alpha) ===']
        self.buffer.append(self.fileredFiles)
        # self.buffer.append('=============================')
        # self.buffer.append('Input: ')
        # Set cursor to the first entry of the list
        self.nvim.command('normal! gg')
        self.nvim.command('normal! j')

    @neovim.command("Tc", range='', nargs='*')
    def tc_explore(self, args, range):
        self.nvim.command('split TC_Explorer')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        # Reset the current input
        self.currentInput = ''
        # self.nvim.current.line = ('Hej %s' % args[1])
        self.buffer = self.nvim.current.buffer
        # The the current files
        self.currentFiles = os.listdir()
        self.fileredFiles = self.currentFiles
        # Draw first frame
        self.draw()

    @neovim.autocmd("TextChangedI", pattern='TC_Explorer', sync=True)
    def on_insert_enter(self):
        self.nvim.current.line = (self.nvim.current.buffer.name)

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.nvim.command('echo "hello from DoItPython %s %s"')

