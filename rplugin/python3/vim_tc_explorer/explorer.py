# ============================================================================
# FILE: explorer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
import shutil
from vim_tc_explorer.logger import log, log_list
from vim_tc_explorer.filter import filter
from vim_tc_explorer.utils import python_input


class explorer(object):
    """ Class for an explorer that is used in the panes """
    def __init__(self, cwd):
        self.isSearcher = False
        # Instance of the filter
        self.filter = filter()
        self.cwd = cwd
        # The the current files
        self.currentFiles = os.listdir(self.cwd)
        # Sort based on folders
        self.sortFiles()
        self.fileredFiles = self.currentFiles[:]
        # Index that tracks which file that is selected
        self.selected = 0
        self.active = True
        self.pattern = ''
        # The header takes up 9 rows
        self.headerLength = 9
        self.markers = []

    def getFirstFileInFolder(self, folder):
        log(folder)
        currentFiles = os.listdir(folder)
        for f in currentFiles:
            cf = os.path.abspath(os.path.join(folder, f))
            if os.path.isdir(os.path.abspath(cf)):
                return self.getFirstFileInFolder(cf)
            else:
                return f
        return None

    def getFirstFile(self):
        return self.getFirstFileInFolder(os.path.abspath(self.cwd))

    def sortFiles(self):
        ogFiles = []
        ogFiles[:] = self.currentFiles[:]
        self.currentFiles[:] = []
        # First folders
        for file in ogFiles:
            if(os.path.isdir(os.path.abspath(os.path.join(self.cwd, file)))):
                self.currentFiles.append(file)
        # Then files
        for file in ogFiles:
            if(not os.path.isdir(os.path.abspath(os.path.join(self.cwd,
                                                              file)))):
                self.currentFiles.append(file)

    def assignBuffer(self, buffer):
        self.buffer = buffer

    def draw(self):
        explorer = self.buffer
        # New way of getting the header
        explorer[:] = self.getUIHeader()
        for idx, val in enumerate(self.fileredFiles):
            if idx == self.selected and self.active:
                token = "-->"
            else:
                token = "   "
            baseStr = val
            if(os.path.isdir(os.path.abspath(os.path.join(self.cwd, val)))):
                # Folder
                lineStr = '+' + val + '/'
            else:
                lineStr = val
            if self.isMarked(val):
                baseStr = token + '<-{' + lineStr + '}->'
            else:
                baseStr = token + ' ' + lineStr
            explorer.append(baseStr)

    def rename(self, newName):
        os.rename(self.getSelected()[0], os.path.join(self.cwd, newName))
        self.cd('.')
        self.updateListing(self.pattern)

    def get_markers_as_string(self):
        # Add the files that shall be copied to clipboard
        # returns a string that constitutes the clipboard
        # which can be set in the host environment
        ret = ''
        for it in self.markers[:-1]:
            # If someone has this in their path its their problem :)
            ret += os.path.join(self.cwd, it) + '_{%boltSplitter%}_'
        if(len(self.markers) > 0):
            ret += os.path.join(self.cwd, self.markers[len(self.markers)-1])
        return ret

    def delete(self):
        yesno = python_input('Delete selection (y/n - default)?')
        if yesno == "y":
            for it in self.markers:
                selFile = os.path.join(self.cwd, it)
                if os.path.isdir(selFile):
                    shutil.rmtree(selFile)
                else:
                    os.remove(selFile)
            self.clearMarkers()
            self.cd('.')
            self.updateListing(self.pattern)

    def move(self, dest):
        os.rename(self.getSelected()[0], dest)
        self.cd('.')
        self.updateListing(self.pattern)

    def mkdir(self, name):
        os.makedirs(os.path.join(self.cwd, name))
        self.cd('.')
        self.updateListing(self.pattern)

    def createFile(self, name):
        open(os.path.join(self.cwd, name), 'a').close()
        self.cd('.')
        self.updateListing(self.pattern)

    def cd(self, path):
        self.cwd = os.path.abspath(os.path.join(self.cwd, path))
        self.currentFiles = os.listdir(self.cwd)
        self.sortFiles()
        self.fileredFiles = self.currentFiles[:]
        self.selected = 0
        self.changeSelection(0)
        self.clearMarkers()

    def refreshListing(self):
        self.currentFiles = os.listdir(self.cwd)

    def updateListing(self, pattern):
        ret = 0
        self.pattern = pattern
        filtCopy = []
        filtCopy[:] = self.fileredFiles[:]
        self.filter.filter(self.currentFiles, pattern, self.fileredFiles)
        if(len(self.fileredFiles) > 0):
            ret = 1
        else:
            self.fileredFiles[:] = filtCopy[:]
        self.changeSelection(0)
        return ret

    def clearMarkers(self):
        self.markers = []

    def addMarker(self, index):
        # Operate on file
        self.markers.append(self.fileredFiles[index])

    def removeMarker(self, index):
        # Operate on file instead of index
        self.markers.remove(self.fileredFiles[index])

    def isMarked(self, val):
        ret = False
        if val in self.markers:
            ret = True
        return ret

    def changeSelection(self, offset):
        self.selected += offset
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.fileredFiles):
            self.selected = len(self.fileredFiles)-1

    def setSelectionWithName(self, name):
        for counter, entry in enumerate(self.fileredFiles):
            if name == entry:
                self.selected = counter

    def getSelected(self):
        pathToFile = os.path.join(self.cwd, self.fileredFiles[self.selected])
        return pathToFile, None

    # Gui header
    def getUIHeader(self):
        bar = "==============================================================="
        if(self.active):
            leadingC = '# '
        else:
            leadingC = '" '
        ret = []
        ret.append(leadingC + bar)
        ret.append(leadingC + 'Bolt for Neovim (%d files)' %
                   len(self.fileredFiles))
        # Shall be highlighted
        ret.append(leadingC + '  $>' + self.cwd)
        qhStr = '  Quick Help: <Ret>:Open   <C-q>:Quit   <C-s>:Set CWD'
        ret.append(leadingC + qhStr)
        qhStr = '              <C-f>:Find   <C-g>:Grep   <C-p>:New File'
        ret.append(leadingC + qhStr)
        qhStr = '              <F2>:Rename  <F5>:Copy    <F6>:Move'
        ret.append(leadingC + qhStr)
        qhStr = '              <F7>:Mkdir   <F8>:Delete  <C-i>:Git Status'
        ret.append(leadingC + qhStr)
        ret.append(leadingC + bar)
        return ret
