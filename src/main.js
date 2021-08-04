const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const {ipcMain} = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 1130,
    height: 700,
    frame: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
    }
  })
  win.loadFile('src/index.html');
  ipcMain.on('minimize', () => {
    win.isMinimized() ? win.restore() : win.minimize()
    // or depending you could do: win.hide()
  })
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// Closed the entire app 
ipcMain.on('close-me', (evt, arg) => {
  app.quit()
})