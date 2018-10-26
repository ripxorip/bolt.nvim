# ============================================================================
# FILE: copy.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import sys
import shutil
import os
from vim_tc_explorer.logger import log, log_list
from vim_tc_explorer.utils import python_input

class CopyUtilitiy(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.progBar = None
        self.lastProgTxt = ''

    # I N T E R F A C E
    # ====================
    def copy_list(self, li, dest):
        for idx, it in enumerate(li):
            if os.path.isfile(it):
                self.copy_file(it, dest)
    
    def move_list(self, li):
        pass
    # ====================

    def copy_file(self, src, dest):
        # dest is the dest path
        destFile = os.path.join(dest, os.path.basename(src))
        if os.path.isfile(destFile):
            resp = python_input(message='%s exists! Overwrite(o), AppendName(a), Skip(s)? Default=a' % destFile)
            # Overwrite
            if resp == 'o':
                os.remove(destFile)
            elif resp == 's':
                return
            # Append number to the name
            else:
                uname = self.uniquify(destFile)
                destFile = os.path.join(dest, uname)
        # Start the actual copy
        self.progBar = ProgressBar('Copying ' + os.path.basename(destFile) + ' ')
        self.ll_copyfile(src, destFile)

    def copy_folder(self, f):
        pass

    # H E L P E R S
    #====================
    def progCallback(self, copied, total):
        progTxt = self.progBar.calculateAndUpdate(copied, total)
        if(self.lastProgTxt != progTxt):
            self.nvim.command("redraw | echo '%s'" % progTxt)
            self.lastProgTxt = progTxt

    def uniquify(self, path):
        start = 0
        testPath = path
        if (os.path.isfile(testPath)):
            while os.path.isfile(testPath):
                bn = os.path.basename(testPath)
                sp = os.path.splitext(bn)
                if (sp[0].endswith(str(start))):
                    start += 1
                    nn = sp[0][:-1] + str(start)
                else:
                    nn = sp[0] + str(start)
                bn = nn + sp[1]
                testPath = os.path.join(os.path.dirname(testPath), bn)
        else:
            # TODO Folders | Untested!
            while os.path.isdir(testPath):
                bn = os.path.basename(testPath)
                if (bn.endswith(str(start))):
                    start += 1
                    nn = bn[:-1] + str(start)
                else:
                    nn = bn + str(start)
                bn = nn
                testPath = os.path.join(os.path.dirname(testPath), bn)
        return testPath

    def ll_copyfile(self, src, dst, *, follow_symlinks=True):
        """Copy data from src to dst.

        If follow_symlinks is not set and src is a symbolic link, a new
        symlink will be created instead of copying the file it points to.

        """
        if shutil._samefile(src, dst):
            raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

        for fn in [src, dst]:
            try:
                st = os.stat(fn)
            except OSError:
                # File most likely does not exist
                pass
            else:
                # XXX What about other special files? (sockets, devices...)
                if shutil.stat.S_ISFIFO(st.st_mode):
                    raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

        if not follow_symlinks and os.path.islink(src):
            os.symlink(os.readlink(src), dst)
        else:
            size = os.stat(src).st_size
            with open(src, 'rb') as fsrc:
                with open(dst, 'wb') as fdst:
                    self.copyfileobj(fsrc, fdst, total=size)
        return dst

    def copyfileobj(self, fsrc, fdst, total, length=16*1024):
        copied = 0
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            copied += len(buf)
            self.progCallback(copied, total=total)

class ProgressBar(object):
    def __init__(self, message, width=20, progressSymbol=u'█', emptySymbol=u'░'):
        self.width = width
 
        if self.width < 0:
            self.width = 0
 
        self.message = message
        self.progressSymbol = progressSymbol
        self.emptySymbol = emptySymbol

    def update(self, progress):
        totalBlocks = self.width
        filledBlocks = int(round(progress / (100 / float(totalBlocks)) ))
        emptyBlocks = totalBlocks - filledBlocks
 
        progressBar = self.progressSymbol * filledBlocks + \
                      self.emptySymbol * emptyBlocks
 
        if not self.message:
            self.message = u''
 
        progressMessage = u'\r{0} {1}  {2}%'.format(self.message,
                                                    progressBar,
                                                    progress)
        return progressMessage
 
    # This function will return the progressbar string
    def calculateAndUpdate(self, done, total):
        progress = int(round( (done / float(total)) * 100) )
        return self.update(progress)
