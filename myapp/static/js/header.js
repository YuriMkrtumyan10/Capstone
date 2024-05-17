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

const defaultTheme = {
  '--accent': '#3dffd6',
  '--blur-border': '#00d4b185',
  '--conversations': '#00d4b185',
  '--hover': '#1e686064',
  '--input-buttons': '#13af95f6'
};

const lightTheme = {
  '--accent': '#ff6347', // Tomato
  '--blur-border': '#ffa07a', // Light Salmon
  '--conversations': '#f25d27', // Orange Red
  '--hover': '#ff634764',
  '--input-buttons': '#ff4500f6' // Orange Red (with slight transparency)
};

const blueTheme = {
  '--accent': '#1e90ff', // Dodger Blue
  '--blur-border': '#87cefa', // Light Sky Blue
  '--conversations': '#4682b4', // Steel Blue
  '--hover': '#1e90ff64',
  '--input-buttons': '#1e90fff6' // Dodger Blue (with slight transparency)
};


function applyTheme(theme) {
  for (let key in theme) {
      document.documentElement.style.setProperty(key, theme[key]);
  }
}

function saveTheme(themeName) {
  localStorage.setItem('selectedTheme', themeName);
}

function loadTheme() {
  const selectedTheme = localStorage.getItem('selectedTheme');
  if (selectedTheme) {
      document.getElementById(selectedTheme).checked = true;
      switch (selectedTheme) {
          case 'light':
              applyTheme(lightTheme);
              break;
          case 'blue':
              applyTheme(blueTheme);
              break;
          default:
              applyTheme(defaultTheme);
              break;
      }
  } else {
      applyTheme(defaultTheme);
  }
}

document.getElementById('default').addEventListener('change', function() {
  if (this.checked) {
      applyTheme(defaultTheme);
      saveTheme('default');
  }
});

document.getElementById('light').addEventListener('change', function() {
  if (this.checked) {
      applyTheme(lightTheme);
      saveTheme('light');
  }
});

document.getElementById('blue').addEventListener('change', function() {
  if (this.checked) {
      applyTheme(blueTheme);
      saveTheme('blue');
  }
});

loadTheme();