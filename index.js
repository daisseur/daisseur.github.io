const darkModeButton = document.querySelector('#dark-mode-button');
const body = document.querySelector('body');
const projectLinks = document.querySelectorAll('.project-links');

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
    console.log("element", element)
    const tutos = element.parentNode.querySelectorAll('#tuto');
    tutos.forEach((tuto) => {
        tuto.style.display = 'block';
        tuto.style.visibility = 'visible';
        tuto.style.width = '100%';
        tuto.style.height = '100%';
    });
}

function switchMode(dark) {
    console.log(`set to ${dark}`);
    body.classList.toggle('dark-mode');
    document.documentElement.style.setProperty('--main-color', '#f2f2f2');
    document.documentElement.style.setProperty('--sub-color', 'rgba(0, 0, 0, 0.5)');
    document.cookie = localStorage.setItem('darkMode', dark);
}

// AU LANCEMENT DE LA PAGE

let dark = false;
if (localStorage.getItem('darkMode') !== null) {
    dark = Boolean(localStorage.getItem('darkMode'));
    console.log("dark localStorage :", dark);
    switchMode(dark);
} else {
    dark = false;
    switchMode(dark);
}


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