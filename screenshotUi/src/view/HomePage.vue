<template>
  <div class="home-page">
    <!-- <div class="header">
            <icon-content icon-name='setting1' content="设置" @click.native="setting" />
            <span>Snipaste OCR</span>
            <div>
                <icon-content icon-name='zuixiaohua' content="最小化" @click.native="minimize" />
                <icon-content icon-name='tuichu' content="退出" @click.native="quit" />
            </div>
        </div> -->
    <div class="body">
      <div class="aside">
        <div class="histories" v-if="histories.length!=0">
          <div :class="historyItem(index)" v-for="(history,index) in histories" :key='index' @click="selectHistory(index)">
            <h3>{{datetime(history.date,history.time)}}</h3>
            <p>{{simpleWord(history.ocrResult)}}</p>
            <icon-content icon-name='delete' class="history-delete" @click.native="removeOne(history.id)"></icon-content>
          </div>
        </div>

        <button class="ocr-btn" @click="ocr">
          <icon-content icon-name='jieping' class="ocr-icon"></icon-content>
          OCR一下
        </button>
      </div>
      <div class="main" v-if="histories.length!=0">
        <div class="resultHeader">
          <h2>{{ datetime(histories[selectIndex].date,histories[selectIndex].time)}}</h2>
          <div class="underline"></div>
        </div>
        <div class="resultBody">
          <div class="result">
            <h4>OCR识别结果:</h4>
            <!-- <icon-content icon-name='lujing182' class="copy" content="复制" position='right' @click.native="copyResult(histories[selectIndex].ocrResult)"></icon-content> -->
            <el-button type="primary" class="copy" icon="el-icon-document-copy" @click="copyResult(histories[selectIndex].ocrResult)" size="mini">点我复制</el-button>
            <p class=" ocrResult">{{ histories[selectIndex].ocrResult }}</p>
          </div>
          <div class="source">
            <h4>原图:</h4>
            <div class="img">
              <!-- <img :src="histories[selectIndex].ocrImgUrl" alt=""> -->
              <el-image style="width: 100%;" :src="histories[selectIndex].ocrImgUrl" :preview-src-list="[histories[selectIndex].ocrImgUrl]">
              </el-image>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import IconContent from '@/components/common/IconContent/index'
import {str2Date, date2Str} from '@/util/dateUtil.js'
export default {
  name: 'HomePage',
  components: {IconContent},
  data() {
    return {
      histories: [
        // {
        //   id: 34,
        //   date: '2020-12-11',
        //   time: '19:27:26',
        //   ocrResult: 'heloo',
        //   ocrImgUrl: 'file:///C:/ProgramData/SnipasteOcr/20201009173007.png',
        // },
        // {
        //   id: 35,
        //   date: '2020-12-11',
        //   time: '19:30:26',
        //   ocrResult: 'heloffdadadfao',
        //   ocrImgUrl: 'file:///C:/ProgramData/SnipasteOcr/20201012090207.png',
        // },
      ],
      selectIndex: 0,
      timeInterval: null,
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
        return word.slice(0, 10) + '...'
      }
    },
  },
  methods: {
    setting() {
      console.log('设置')
    },
    minimize() {
      window.getBackend.then((backend) => {
        backend.mini()
      })
    },
    quit() {
      window.getBackend.then((backend) => {
        backend.quit()
      })
    },
    ocr() {
      let self = this
      window.getBackend.then((backend) => {
        backend.ocr('', (rsp) => {
          self.timeInterval = window.setInterval(this.ocr_result, 3000)
        })
      })
    },
    ocr_result() {
      let self = this
      window.getBackend.then((backend) => {
        backend.ocr_result('', (rsp) => {
          if (rsp) {
            windos.clearInterval(self.timeInterval)
            this.get_all()
            self.$notify({
              message: '识别完成',
              type: 'success',
              duration: '700',
            })
          } else {
            console.log('next')
          }
        })
      })
    },
    get_all() {
      window.getBackend.then((backend) => {
        backend.get_all_history('', (rsp) => {
          let data = JSON.parse(rsp)
          let result = data.map((item) => {
            let date = str2Date(item[2], 'yyyyMMddHHmmss')
            return {
              id: item[0],
              date: date2Str(date, 'yyyy-MM-dd'),
              time: date2Str(date, 'HH:mm:ss'),
              ocrResult: item[1],
              ocrImgUrl: 'file:///' + item[3],
            }
          })
          this.histories = result
          this.selectIndex = 0
        })
      })
    },
    removeOne(id) {
      let self = this
      window.getBackend.then((backend) => {
        backend.removeOne(id, (rsp) => {
          let data = JSON.parse(rsp)
          if (data.code === 200) {
            self.$notify({
              message: '删除成功',
              type: 'success',
              duration: '700',
            })
            self.get_all()
          }
        })
      })
    },
    copyResult(str) {
      let self = this
      window.getBackend.then((backend) => {
        backend.copyResult(str, (rsp) => {
          let data = JSON.parse(rsp)
          if (data.code === 200) {
            self.$notify({
              message: '已复制到剪切板',
              type: 'success',
              duration: '700',
            })
          }
        })
      })
    },
    selectHistory(index) {
      this.selectIndex = index
    },
    historyItem(index) {
      if (this.selectIndex === index) {
        return 'history-item selected'
      } else {
        return 'history-item'
      }
    },
  },
  created() {
    this.get_all()
  },
}
</script>
<style scoped>
@import '../assets/css/home-page.css';
</style>
