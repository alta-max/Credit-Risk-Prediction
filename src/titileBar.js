const {ipcRenderer} = require('electron');
const closeApp = document.getElementById('close');
const minmizeApp = document.getElementById('min');

closeApp.addEventListener('click', () => {
    ipcRenderer.send('close-me')
});


minmizeApp.addEventListener('click', () => {
    ipcRenderer.send('minimize')
});


