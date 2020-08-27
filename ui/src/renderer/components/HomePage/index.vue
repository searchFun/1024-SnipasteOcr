<template>
  <div class="home-page">
    <div class="header">
      <icon-content icon-name='setting' content="设置" @click.native="setting" />
      <span>Snipaste OCR</span>
      <div>
        <icon-content icon-name='zuixiaohua' content="最小化" @click.native="minimize" />
        <icon-content icon-name='tuichu' content="退出" @click.native="quit" />
      </div>
    </div>
    <div class="body">
      <div class="aside">
        <div class="histories">
          <div :class="historyItem(index)" v-for="(history,index) in histories" :key='index' @click="selectHistory(index)">
            <h3>{{datetime(history.date,history.time)}}</h3>
            <p>{{simpleWord(history.ocrResult)}}</p>
            <icon-content icon-name='delete'></icon-content>
          </div>
        </div>
        <button id="ocr-btn" @click="ocr">OCR一下</button>
      </div>
      <div class="main">
        <div class="resultHeader">
          <h2>{{ datetime(histories[selectIndex].date,histories[selectIndex].time)}}</h2>
          <div class="underline"></div>
        </div>
        <div class="resultBody">
          <h4>OCR识别结果:</h4>
          <p class="ocrResult">{{ histories[selectIndex].ocrResult }}</p>
          <h4>原图:</h4>
          <div class="img">
            <img :src="histories[selectIndex].ocrImgUrl" alt="">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import IconContent from '@/components/common/IconContent/index'

const {ipcRenderer: ipc} = require('electron')
export default {
  name: 'HomePage',
  components: {IconContent},
  data() {
    return {
      histories: [
        {
          date: '2020-08-25',
          time: '12:05:06',
          ocrResult:
            'hadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkadhadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkadhadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkadhadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkadhadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkadhadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkad',
          ocrImgUrl:
            'https://tse4-mm.cn.bing.net/th/id/OIP.hF9OteN_EnKpABZl1aHGIwHaDP?w=334&h=153&c=7&o=5&dpr=1.5&pid=1.7'
        },
        {
          date: '2020-08-25',
          time: '12:05:06',
          ocrResult:
            'hadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkad',
          ocrImgUrl: 'file:///D:/Documents/OneDrive/图片/壁纸/星树.jpg'
        }
      ],
      selectIndex: 0
    }
  },
  computed: {
    datetime(date, time) {
      return (date, time) => {
        return date + '\t' + time
      }
    },
    simpleWord(word) {
      return (word) => {
        return word.slice(0, 20) + '...'
      }
    }
  },
  methods: {
    setting() {
      console.log('设置')
    },
    minimize() {
      ipc.send('min')
    },
    quit() {
      ipc.send('quit')
    },
    selectHistory(index) {
      this.selectIndex = index
    },
    ocr() {
      console.log('ocr一下')
    },
    historyItem(index) {
      if (this.selectIndex === index) {
        return 'history-item selected'
      } else {
        return 'history-item'
      }
    }
  },
  created() {
    console.log(this)
  }
}
</script>
<style scoped>
@import './style';
</style>
