

def getPackagesToInstall():
  return ('python-pip',)




def getInstallCommand():
  return lambda nameList: "sudo apt-get install "+" ".join(nameList)