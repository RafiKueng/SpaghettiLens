
def getPackagesToInstall():
  return ('http://www.lfd.uci.edu/~gohlke/pythonlibs/zybnfyan/pip-1.3.1.win-amd64-py2.7.exe',)

#to download and start the install / setup.exe on win, use a python script
def getInstallCommand():
  return lambda nameList: "\n".join(['python dl_and_run.py '+_ for _ in nameList])