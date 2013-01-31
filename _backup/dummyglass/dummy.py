from time import sleep
	
pref = "dummyglass  : "

def doSomeStuff(msg):
    print pref + "dummyglass being called with: "+msg
    if msg.startswith("g:"):    
        print pref + "got special command: "+msg[2:]
        try:
            ret = eval(msg[2:])
        except:
            print pref + "but no valid command"
            ret = "<b>" + msg[2:].upper() + "</b>"
        if ret is None:
            ret = "--none--"
        else:
            ret = str(ret)
    else:
        ret = "<b>" + msg.upper() + "</b>"
    print pref + "done, returning: " + ret
    return ret
