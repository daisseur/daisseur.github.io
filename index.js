const darkModeButton = document.querySelector('#dark-mode-button');
const projectsContainer = document.querySelectorAll('.project-container');
const body = document.querySelector('body');
const projectLinks = document.querySelectorAll('.project-links');
const cookie = document.cookie;
let viewed = {};
let dark = false;

function hide(element) {
    console.log("element", element)
    const tutos = element.parentNode.querySelectorAll('#tuto');
    tutos.forEach((tuto) => {
        tuto.style.display = 'none';
        tuto.style.visibility = 'hidden';
        tuto.style.height = '0';
    });
}

function reveal(element) {
    addViewed(element);
    console.log("element", element)
    const tutos = element.parentNode.querySelectorAll('#tuto');
    tutos.forEach((tuto) => {
        tuto.style.display = 'block';
        tuto.style.visibility = 'visible';
        tuto.style.width = '100%';
        tuto.style.height = '100%';
    });
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
      let date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
  
function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999;';
}

function switchMode(dark) {
    dark = Boolean(dark);
    setCookie('darkMode', dark, 365);
    console.log(`set to ${dark}`);
    body.classList.toggle('dark-mode');

    projectsContainer.forEach((project) => {
        project.classList.toggle('dark-mode');
    });
}

function addViewed(element) {
    let name = element.parentNode.querySelector('.project-name').textContent;
    if (viewed instanceof Object) {
        if (!(name in viewed)) {
            viewed[name] = 0;
        }
        viewed[name]++;
        const viewer = element.parentNode.querySelector('#viewer');
        viewer.innerHTML = `Vu <strong>${viewed[name]}</strong> fois par vous `;
        setCookie(name, viewed[name], 365);
        console.log(viewed[name]);
    }
    
} 

function checkCookie(cookieName, defaultValue, func = null) {
    let cookieValue = getCookie(cookieName);
    type = typeof defaultValue;
    if (cookieValue === null) {
        return defaultValue;
    } else {
        console.log(`${cookieName} cookie :`, cookieValue);
        if (func) {
            return func(cookieValue);
        } else {
            return type === "boolean" ? Boolean(cookieValue) : type === "number" ? Number(cookieValue) : cookieValue;
        }
    }
}

function clearCookies() {
    eraseCookie('darkMode');
    projectsContainer.forEach((project) => {
        let name = project.querySelector('.project-name').textContent;
        eraseCookie(name);
    });
    location.reload();
}


// AU LANCEMENT DE LA PAGE

checkCookie('darkMode', dark, switchMode);

projectsContainer.forEach((project) => {
    let name = project.querySelector('.project-name').textContent
    viewed[name] = checkCookie(name, 0);
    if (viewed[name]) {
        viewed[name]--;
        addViewed(project);
    }
    console.log(name, viewed[name] );
});
console.log(viewed);

// Reveal quand il y a un clique sur un lien projet
projectLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
        reveal(event.target);
    });
});

// Dark mode button
darkModeButton.addEventListener('click', () => {
    dark = !dark;
    switchMode(dark);
});

