import neovim
import os
import re

@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def draw(self):
        explorer = self.nvim.buffers[self.explorerBufferNumber]
        explorer[:] = ['==== TC explorer (alpha) ===']
        explorer.append(self.fileredFiles)

    def updateFilter(self):
        self.fileredFiles = []
        for entry in self.currentFiles:
            res = re.search(self.currentInput, entry)
            if res != None:
                self.fileredFiles.append(entry)

    @neovim.command("Tc", range='', nargs='*', sync=True)
    def tc_explore(self, args, range):
        """ Initialize the plugin """
        # Create the input buffer
        self.nvim.command('e TC_Input')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_input')
        # Might be wrong bcz ref
        self.inputBufferNumber = self.nvim.current.buffer.number

        # Create the explorer buffer
        self.nvim.command('split TC_Explorer')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumber = self.nvim.current.buffer.number
        self.explorer = self.nvim.current.buffer
        # Go back to the input buffer window
        self.nvim.command('wincmd j')
        self.nvim.current.window.height = 1
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        # Need to remap more
        self.nvim.command("inoremap <buffer> <CR> $")

        # The the current files
        self.currentFiles = os.listdir()
        self.fileredFiles = self.currentFiles
        # Draw first frame
        self.draw()

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def on_insert_enter(self):
        """ Process incoming string """
        # self.nvim.current.line = (self.nvim.current.buffer.name)
        # self.nvim.command('normal! 0')
        inputLine = self.nvim.current.line
        self.currentInput = '.*'
        # Add regular expression
        for c in inputLine:
            self.currentInput += c + '.*'
        # Update filtered files
        self.updateFilter()
        # Draw
        self.draw()

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.nvim.command('echo "hello from DoItPython %s %s"')

