# ============================================================================
# FILE: searcher.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from bolt.filter import filter
# In order to call ripgrep from python instead of vim
from subprocess import check_output


class resultGroup(object):
    def __init__(self, fileName):
        self.lines = []
        self.matches = 0
        self.fileName = fileName


class searcher(object):
    def __init__(self):
        self.filter = filter()
        # Attribute to distinguish from explorer
        self.isSearcher = True
        self.selected = 0
        self.fileredFiles = []
        self.expanded = False
        # Header takes up 6 rows
        self.headerLength = 6
        self.matches = []

    def createResultStructure(self):
        self.results = {}
        self.resultFiles = []
        for line in self.matches[1:len(self.matches)]:
            # Process each line
            f = line.split(':')
            if(f is not None):
                if(not f[0] in self.results):
                    self.results[f[0]] = resultGroup(f[0])
                    self.resultFiles.append(f[0])
                self.results[f[0]].lines.append(line)
                self.results[f[0]].matches += 1

    def getFileListFromResults(self):
        self.fileList = []
        self.rawFileList = []
        for res in self.fileredFiles:
            # Add the file
            self.rawFileList.append(res)
            self.fileList.append('+'+res + ' | ' +
                                 str(self.results[res].matches) + ' matches')
            if self.expanded:
                for l in self.results[res].lines:
                    self.fileList.append('  -'+l)
                    self.rawFileList.append(l)

    def search(self, dir, filePattern, inputPattern):
        # Temporarily change system cwd
        ogCwd = os.getcwd()
        os.chdir(dir)
        # Perform the search
        rawoutput = check_output(['rg', '--vimgrep', '--type',
                                  filePattern, inputPattern])
        # Parse raw output
        rawoutput = rawoutput.decode()
        self.matches = rawoutput.splitlines()
        # Jump back
        os.chdir(ogCwd)
        self.createResultStructure()
        self.getFileListFromResults()

    def updateListing(self, pattern):
        self.filter.filter(self.resultFiles, pattern, self.fileredFiles)
        self.getFileListFromResults()
        self.changeSelection(0)

    def changeSelection(self, offset):
        # Selection is this time based on fileList
        self.selected += offset
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.fileList):
            self.selected = len(self.fileList)-1

    def toggle(self):
        self.expanded = not self.expanded
        self.getFileListFromResults()

    def getListing(self):
        files = []
        for f in self.fileredFiles:
            files.append(f)
        # Searcher only returns files
        return [None, files]

    def getSelected(self):
        lineNum = None
        currLine = self.rawFileList[self.selected]
        if(':' in currLine):
            # This is a match in a file
            lineParts = currLine.split(':')
            self.matches[:] = lineParts
            pathToFile = os.path.join(self.cwd, lineParts[0])
            lineNum = int(lineParts[1])
        else:
            pathToFile = os.path.join(self.cwd, currLine)
        return pathToFile, lineNum
