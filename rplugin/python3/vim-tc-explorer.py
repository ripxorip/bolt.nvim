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
        # Draw current path 
        explorer.append(self.cwd)
        explorer.append('----------------------------')
        # FIXME: Draw selection using either color or arrow
        # starting with drawing arrow (works also for terminals)
        for idx, val in enumerate(self.fileredFiles):
            if idx == self.selected:
                token = "===> "
            else:
                token = "     "
            explorer.append(token + val) 

    def cd(self, path):
        self.cwd = os.path.abspath(os.path.join(self.cwd, path))
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles
        # FIXME - hack..
        self.changeSelection(0)

    def updateFilter(self):
        # TODO: Make the filtering smarter, providing the best match
        # first and perhaps add case insensitity
        self.fileredFiles = []
        for entry in self.currentFiles:
            res = re.search(self.currentInput, entry)
            if res != None:
                self.fileredFiles.append(entry)
        # FIXME - hack..
        self.changeSelection(0)

    def changeSelection(self, offset):
        self.selected += offset
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.fileredFiles):
            self.selected = len(self.fileredFiles)-1

    def close(self):
        # Method used to close the plugin
        # Delete both buffers
        self.nvim.command('stopinsert')
        self.nvim.command('bd %s' % self.explorerBufferNumber)
        self.nvim.command('bd %s' % self.inputBufferNumber)


    @neovim.command("TcExpEnter", range='', nargs='*', sync=True)
    def tc_enter(self, args, range):
        # Handle enter
        if os.path.isdir(os.path.join(self.cwd, self.fileredFiles[self.selected])):
            self.cd(self.fileredFiles[self.selected])
            self.draw()
            # Clear the line
            self.nvim.current.line = ''
            self.nvim.command('startinsert')
        else:
            # Need to solve this part to get syntax, something with the nested 
            # autocmds.... Cont. here...
            self.nvim.command('e %s' % os.path.abspath(os.path.join(self.cwd, self.fileredFiles[self.selected])))
            self.close()
            return


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
        # Remap keys for the input layer
        # Enter
        self.nvim.command("inoremap <buffer> <CR> <ESC>:TcExpEnter<CR>")
        # Backspace
        self.nvim.command("inoremap <buffer> <BS> %")
        # Up
        self.nvim.command("inoremap <buffer> <C-k> !")
        # Down
        self.nvim.command("inoremap <buffer> <C-j> @")
        # Close
        self.nvim.command("inoremap <buffer> <C-q> ?")

        # The the current files
        self.cwd = os.path.abspath(os.getcwd())
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles
        # Index that tracks which file that is selected
        self.selected = 0
        # Draw first frame
        self.draw()

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def on_insert_enter(self):
        """ Process incoming string """
        # self.nvim.current.line = (self.nvim.current.buffer.name)
        # self.nvim.command('normal! 0')
        inputLine = self.nvim.current.line
        # Check if backspace or enter (special keys)
        if inputLine.endswith('%') == True:
            inputLine = inputLine.replace("%", "")
            # Handle backspace
            if not inputLine:
                # Change directory to the parrent
                self.cd('..')
            inputLine = inputLine[:-1]
        elif inputLine.endswith('!') == True:
            inputLine = inputLine.replace("!", "")
            # Handle selection up
            self.changeSelection(-1)
        elif inputLine.endswith('@') == True:
            inputLine = inputLine.replace("@", "")
            # Handle selection down
            self.changeSelection(1)
        elif inputLine.endswith('$') == True:
            inputLine = inputLine.replace("$", "")
            # Handle enter
            if os.path.isdir(os.path.join(self.cwd, self.fileredFiles[self.selected])):
                self.cd(self.fileredFiles[self.selected])
            else:
                # Need to solve this part to get syntax, something with the nested 
                # autocmds.... Cont. here...
                self.nvim.command('e %s' % os.path.abspath(os.path.join(self.cwd, self.fileredFiles[self.selected])))
                self.close()
                return
            # Else, edit the file in a clever way
            # Clear the filter
            inputLine = ""
        elif inputLine.endswith('?') == True:
            # Close
            self.close()
            return
        self.nvim.current.line = inputLine
        self.currentInput = '.*'
        # Add regular expression
        for c in inputLine:
            self.currentInput += c + '.*'
        # Update filtered files
        self.updateFilter()
        # Draw
        self.draw()

