<template>
  <div id="app">
    <span class="app-border"></span>
    <span class="app-border"></span>
    <span class="app-border"></span>
    <span class="app-border"></span>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'electron-vue'
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html,
body {
  height: 100vh;
  border-radius: 5px;
}

#app {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
#app .app-border {
  opacity: 0;
}
#app .app-border:nth-child(1) {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, transparent, #717274);
  animation: toRight 4s linear 0s infinite;
}
@keyframes toRight {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

#app .app-border:nth-child(2) {
  position: absolute;
  right: 0;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, transparent, #1779ff);
  animation: toBottom 4s linear 2s infinite;
}
@keyframes toBottom {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(100%);
  }
}
#app .app-border:nth-child(3) {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to left, transparent, #1779ff);
  animation: toLeft 4s linear 0s infinite;
}
@keyframes toLeft {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

#app .app-border:nth-child(4) {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to top, transparent, #1779ff);
  animation: toTop 4s linear 2s infinite;
}
@keyframes toTop {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(-100%);
  }
}
</style>
