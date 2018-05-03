// this file WILL BE OVERWRITTEN if you do an automatic prod server isntall

LMT.version = 'DEBUG'
LMT.build = '[none]'
LMT.build_time = '000000000000'

// debug flag
debug = true;

//developper mode (are wo local?)
local = true;

// should we log stuff?
doLog = true;
// should we output the log to the console or to the page
logToConsole = true;


if (local) {
  LMT.com.serverUrl = "http://localhost:8000";
}

else {
  LMT.com.serverUrl = ""; //in production setup those are locally (nginx redirects)
}
