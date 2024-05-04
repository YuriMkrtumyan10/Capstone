document.addEventListener("DOMContentLoaded", function() {
  if (!sessionStorage.getItem('consoleTextCalled')) {
    runConsoleText();
    sessionStorage.setItem('consoleTextCalled', 'true');
  }
});

function runConsoleText() {
  consoleText(['CyberGPT'], 'text');
}

function consoleText(words, id) {
  var con = document.getElementById('console');
  var target = document.getElementById(id);
  target.setAttribute('style', 'color: #fff'); // Set color to white
  var letterCount = 1;
  var x = 1;
  var waiting = false;
  var visible = true;
  
  var interval = window.setInterval(function() {
    if (letterCount === 0 && waiting === false) {
      waiting = true;
      target.innerHTML = words[0].substring(0, letterCount);
      window.setTimeout(function() {
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (letterCount === words[0].length + 1 && waiting === false) {
      waiting = true;
      window.setTimeout(function() {
        x = -1;
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (waiting === false) {
      target.innerHTML = words[0].substring(0, letterCount);
      letterCount += x;
    }
  }, 120);
  
  window.setTimeout(function() {
    clearInterval(interval);
    con.className = 'console-underscore hidden';
  }, words[0].length * 120);
}
