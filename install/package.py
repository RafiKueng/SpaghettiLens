import fabric.api

from utils import _r, _s

fabric.api.env["PKGS"] = []

def package_install(package):
  """ Installs packages via apt-get. """
  if type(package) in (list, tuple):
    fabric.api.env["PKGS"].extend(package)
  else:
    fabric.api.env["PKGS"].append(package)


def package_install_start(options = '', update = False):
  """ Installs packages via apt-get. """
  package = fabric.api.env["PKGS"]
  if update: package_update(package)
  if type(package) in (list, tuple): package = " ".join(package)
  _s('apt-get install %s --yes %s' % (options, package,))
 
def package_update(package = None):
  """ Update package on the server """
  if package:
    if type(package) in (list, tuple): package = " ".join(package)
    _s('apt-get update --yes %s' % package)
  else:
    _s('apt-get update --yes')
 
def package_upgrade(package = None):
  """ Upgrade packages on the server """
  if package:
    if type(package) in (list, tuple): package = " ".join(package)
    _s('apt-get upgrade --yes %s' % package)
  else:
    _s('apt-get upgrade --yes')
 
def package_add_repository(repo):
  _s('add-apt-repository %s' % repo)
  package_update()