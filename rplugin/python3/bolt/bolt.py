# ============================================================================
# FILE: bolt.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from bolt.explorer import explorer
from bolt.searcher import searcher


class bolt(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self):
        # Start in CWD
        cwd = os.path.abspath(os.getcwd())
        self.commanders = {}
        # Create explorers
        self.commanders['exp1'] = explorer(cwd)
        self.commanders['exp2'] = explorer(cwd)
        # Create searchers
        self.commanders['sea1'] = searcher()
        self.commanders['sea2'] = searcher()

# ============================================================================
# Bolt Commands
# ============================================================================
    # commander is used to lookup which object to use from the dict;
    # exp1, exp2, sea1, sea2

    # ==========================================
    # Generic (explorer or searcher) commands
    # ==========================================
    def updateListing(self, pattern, commander):
        self.commanders[commander].updateListing(pattern)

    def getSelectedFile(self, commander):
        return self.commanders[commander].getSelected()

    def changeSelection(self, offset, commander):
        self.commanders[commander].changeSelection(offset)

    def getListing(self, commander):
        return self.commanders[commander].getListing()

    # ==========================================
    # Searcher exclusive commands
    # ==========================================
    def search(self, filePattern, inputPattern,
               fromCommander, commander):
        pass

    # ==========================================
    # Explorer exclusive commands
    # ==========================================
    def move(self, dest, commander):
        self.commanders[commander].move(dest)

    def delete(self, commander):
        self.commanders[commander].delete()

    def rename(self, newName, commander):
        self.commanders[commander].rename(newName)

    def copy(self, dest, commander):
        self.commanders[commander].copy(dest)

    def mkdir(self, name, commander):
        self.commanders[commander].mkdir(name)

    def createFile(self, name, commander):
        self.commanders[commander].createFile(name)

    # ==========================================
    # Explorer to explorer commands
    # ==========================================
    # TBD
    def eToe_copy(self, commander):
        pass

    # TBD
    def eToe_Move(self, commander):
        pass

# ============================================================================
# Helpers
# ============================================================================
