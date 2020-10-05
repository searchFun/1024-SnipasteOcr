"use strict";

import { app, BrowserWindow, Menu } from "electron";

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== "development") {
  global.__static = require("path")
    .join(__dirname, "/static")
    .replace(/\\/g, "\\\\");
}

const winURL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:9080"
    : `file://${__dirname}/index.html`;

// 主窗口(唯一)
let mainWindow;

// 创建窗口函数
function createWindow() {
  /* 隐藏electron创听的菜单栏 */
  Menu.setApplicationMenu(null);

  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 700,
    useContentSize: true,
    width: 680,
    frame: false
  });

  mainWindow.loadURL(winURL);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
  mainWindow.setIgnoreMouseEvents(false);
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// 添加最小化、退出功能
const { ipcMain } = require("electron");
// 添加最小化
ipcMain.on("min", () => {
  mainWindow.minimize();
});
// 添加关闭
ipcMain.on("quit", () => {
  mainWindow.close();
});

ipcMain.on("screen-shot", () => {

});
/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */
