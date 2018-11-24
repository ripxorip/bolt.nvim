# ============================================================================
# FILE: super_searcher.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from vim_tc_explorer.filter import filter

class super_searcher(object):
    def __init__(self, nvim, _buffer, cwd):
        self.filter = filter()
        self.nvim = nvim
        self.buffer = _buffer
        self.isSearcher = True
        self.fileredFiles = []
        self.cwd = cwd
        self.headerLength = 3
        self.pattern = ''

    def assignBuffer(self, _buffer):
        self.buffer = _buffer
        self.prevbuffer = self.nvim.current.buffer
        self.nvim.command('setlocal filetype=vim_tc_super_search_result')

    def draw(self):
        self.buffer[:] = self.getUIHeader()
        # Shall check if filter is applied, need more
        # than '2' chars in order to draw
        if len(self.pattern) > 2:
            for r in self.fileredFiles:
                self.buffer.append(r)

    def search(self, _dir):
        allFiles = []
        exclude = set(['.git'])
        for root, dirs, files in os.walk(_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for f in files:
                allFiles.append(os.path.join(root, f))
        self.currentFiles = allFiles

    def updateListing(self, pattern):
        self.pattern = pattern
        # Needs performance optimization
        # Could be done like 'if pattern is longer' use the shorter list
        # If it is less go back to filter with the og list
        # Also, needs more clever sorting
        # count the number of good matches?
        # Prioritize filenames over paths
        # FIXME: Contine here
        self.filter.filter(self.currentFiles, pattern, self.fileredFiles)

    def changeSelection(self, offset):
        pass

    def getUIHeader(self):
        bar = "==============================================================="
        leadingC = '#'
        ret = []
        ret.append(leadingC + bar)
        ret.append(leadingC + ' Bolt Super Search (Beta)')
        ret.append(leadingC + bar)
        return ret
