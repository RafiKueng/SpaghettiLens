import castles
import internet
import masterlens
import spacewarps

__mods = [castles, internet, masterlens, spacewarps]


members = [(_.__name__, _.getName(), _) for _ in __mods]
