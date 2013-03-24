
# returns a list of needed input with default values
# (key, description, default)
def neededVars():
  vars = (("DATABASE_PATH", "where will the sqlite database be saved", "../database/lenses.db"),)
  return vars


  
def about():
  return "sqlite3 database module"



