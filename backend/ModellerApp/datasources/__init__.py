import castles
import internet
import masterlens
import spacewarps

__mods = [castles, internet, masterlens, spacewarps]


members = [(_.getID(), _.getDesc(), _.__name__, _) for _ in __mods]
