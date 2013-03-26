




// this file WILL BE OVERWRITTEN if you do an automatic prod server isntall





// debug flag
debug = true;

//developper mode (are wo local?)
local = true;


if (local) {
  LMT.com.serverUrl = "http://localhost:8000";
}

else {
  LMT.com.serverUrl = ""; //in production setup those are locally (nginx redirects)
}
