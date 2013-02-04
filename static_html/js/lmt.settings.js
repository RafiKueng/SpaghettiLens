
// debug flag
debug = true;

//developper mode (are wo local?)
local = false;


if (local) {
  LMT.com.serverUrl = "http://localhost:8000";
}

else {
  LMT.com.serverUrl = ""; //in production setup those are locally (nginx redirects)
}
